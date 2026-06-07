"""Run the SAMBA classic Dynare model from a temporary working directory."""

from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_MODEL_FILES = (
    "samba_classic.mod",
    "calibration.m",
    "steady_state.m",
    "shocks.inc",
    "observables.inc",
    "priors.inc",
)
IRF_HORIZON = 20
IRF_EPSILON = 1e-10
MH_PILOT_ESTIMATED_PARAMETER_COUNT = 28
MH_PILOT_DYNARE_DEFAULT_JSCALE = round(
    2.38 / math.sqrt(MH_PILOT_ESTIMATED_PARAMETER_COUNT), 6
)
MH_PILOT_CONFIG = {
    "mh_replic": 2000,
    "chains": 2,
    "mh_nblocks": 2,
    "mh_drop": 0.5,
    "mh_jscale": None,
    "estimated_parameter_count": MH_PILOT_ESTIMATED_PARAMETER_COUNT,
    "dynare_default_mh_jscale": MH_PILOT_DYNARE_DEFAULT_JSCALE,
    "target_acceptance_central": 0.234,
    "target_acceptance_min": 0.20,
    "target_acceptance_max": 0.35,
    "rhat_policy": "warning_only",
}
FULL_MH_CONFIG = {
    "mh_replic": 20000,
    "chains": 4,
    "mh_nblocks": 4,
    "approved_blocks": 2,
    "mh_drop": 0.5,
    "mh_jscale": 0.337313,
    "target_acceptance_central": 0.234,
    "target_acceptance_min": 0.20,
    "target_acceptance_max": 0.35,
    "rhat_max": 1.1,
    "rhat_policy": "blocking_if_unavailable_or_above_threshold",
}
FULL_MH_ARTIFACT_FILENAMES = {
    "summary": "wbs073_full_mh_summary.json",
    "diagnostics": "wbs073_full_mh_diagnostics.md",
    "manifest": "wbs073_full_mh_manifest.json",
}
DEFAULT_EXTERNAL_RUN_ROOT = Path("D:/SAMBA_RUN")
DEFAULT_MIN_EXTERNAL_FREE_GB = 500.0
DEFAULT_MIN_C_FREE_GB = 30.0
DEFAULT_ABORT_D_FREE_GB = 50.0
DEFAULT_ABORT_C_FREE_GB = 30.0
DEFAULT_DISK_TELEMETRY_FILE = Path(
    "outputs/posterior/full/wbs073_disk_telemetry.jsonl"
)
DEFAULT_DISK_TELEMETRY_INTERVAL_SECONDS = 60.0
DISK_ABORT_RETURNCODE = 125
INTERRUPT_RETURNCODE = 130
RAW_ARTIFACT_HASH_MAX_BYTES = 256 * 1024 * 1024
LIKELIHOOD_DATA_FILE = "classic_mvp_dynare.csv"
LIKELIHOOD_OBSERVABLE_COLUMNS = ("y", "c", "i", "g", "q", "r_t")
LIKELIHOOD_COLUMN_MAP = {"r_t": "r"}
LOG_DIFF_DEMEAN_COLUMNS = ("y", "c", "i", "g")
LIKELIHOOD_MEASUREMENT_ERRORS = {
    "y": {
        "stderr": 0.08,
        "source": "BCB_WP239",
        "source_location": "WP239 Table 3 measurement errors, PDF page 99 printed page 98",
        "rationale": "GDP growth measurement error documented by WP239 and needed to avoid singular likelihood for y,c,i,g.",
    },
}
RUNTIME_PROCESS_NAMES = {
    "dynare.exe",
    "matlab.exe",
    "octave.exe",
    "octave-cli.exe",
    "octave-svgconvert.exe",
}


class DynareCommandAborted(RuntimeError):
    def __init__(
        self,
        reason: str,
        returncode: int,
        *,
        stdout: str = "",
        stderr: str = "",
        cleanup_records: list[dict[str, Any]] | None = None,
        telemetry_record: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(reason)
        self.reason = reason
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.cleanup_records = cleanup_records or []
        self.telemetry_record = telemetry_record or {}


def irf_targets_file(root: Path | None = None) -> Path:
    base = root if root is not None else repo_root()
    return base / "docs" / "wbs063_irf_targets.md"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def samba_model_dir(root: Path | None = None) -> Path:
    base = root if root is not None else repo_root()
    return base / "model" / "samba_classic"


def model_input_file(root: Path | None = None) -> Path:
    base = root if root is not None else repo_root()
    return base / "data" / "model_input" / "classic_mvp.csv"


def full_mh_output_dir(root: Path | None = None) -> Path:
    base = root if root is not None else repo_root()
    return base / "outputs" / "posterior" / "full"


def default_full_mh_storage_paths(root: Path | None = None) -> dict[str, Path]:
    base = root if root is not None else repo_root()
    return {
        "work_dir": DEFAULT_EXTERNAL_RUN_ROOT / "work",
        "tmp_dir": DEFAULT_EXTERNAL_RUN_ROOT / "tmp",
        "scratch_output_dir": DEFAULT_EXTERNAL_RUN_ROOT
        / "scratch_output"
        / "posterior"
        / "full",
        "repo_output_dir": full_mh_output_dir(base),
    }


def _resolve_repo_relative_path(path: str | Path | None, default: Path, root: Path) -> Path:
    if path is None:
        return default
    resolved = Path(path)
    if resolved.is_absolute():
        return resolved
    return root / resolved


def _drive_root(path: Path) -> Path:
    if path.anchor:
        return Path(path.anchor)
    resolved = path.resolve()
    return Path(resolved.anchor) if resolved.anchor else resolved


def _path_for_manifest(path: Path, root: Path | None = None) -> str:
    base = root if root is not None else repo_root()
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return str(path)


def _free_gb(path: Path, disk_usage_func: Any = shutil.disk_usage) -> float:
    return disk_usage_func(path).free / (1024 ** 3)


def runtime_process_ids() -> set[int]:
    if not sys.platform.startswith("win"):
        return set()
    try:
        completed = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError:
        return set()
    if completed.returncode != 0:
        return set()
    process_ids = set()
    for row in csv.reader(completed.stdout.splitlines()):
        if len(row) < 2:
            continue
        if row[0].lower() in RUNTIME_PROCESS_NAMES:
            try:
                process_ids.add(int(row[1]))
            except ValueError:
                continue
    return process_ids


def disk_telemetry_record(
    *,
    c_drive_root: Path,
    d_drive_root: Path,
    child_pid: int | None,
    elapsed_seconds: float,
    disk_usage_func: Any = shutil.disk_usage,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "c_drive": str(c_drive_root),
        "d_drive": str(d_drive_root),
        "child_pid": child_pid,
        "runtime_process_ids": sorted(runtime_process_ids()),
    }
    try:
        record["c_free_gb"] = round(_free_gb(c_drive_root, disk_usage_func), 3)
    except OSError as exc:
        record["c_free_gb"] = None
        record["c_free_error"] = str(exc)
    try:
        record["d_free_gb"] = round(_free_gb(d_drive_root, disk_usage_func), 3)
    except OSError as exc:
        record["d_free_gb"] = None
        record["d_free_error"] = str(exc)
    return record


def write_disk_telemetry_record(telemetry_file: Path, record: dict[str, Any]) -> None:
    telemetry_file.parent.mkdir(parents=True, exist_ok=True)
    with telemetry_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def disk_abort_reason(
    record: dict[str, Any],
    *,
    abort_d_free_gb: float = DEFAULT_ABORT_D_FREE_GB,
    abort_c_free_gb: float = DEFAULT_ABORT_C_FREE_GB,
) -> str | None:
    if record.get("d_free_error"):
        return f"Could not read D: free space during full-MH: {record['d_free_error']}"
    if record.get("c_free_error"):
        return f"Could not read C: free space during full-MH: {record['c_free_error']}"
    d_free_gb = record.get("d_free_gb")
    c_free_gb = record.get("c_free_gb")
    if d_free_gb is not None and d_free_gb < abort_d_free_gb:
        return (
            f"Full-MH disk guard abort: D: free space {d_free_gb:.3f} GB "
            f"is below hard threshold {abort_d_free_gb:.3f} GB."
        )
    if c_free_gb is not None and c_free_gb < abort_c_free_gb:
        return (
            f"Full-MH disk guard abort: C: free space {c_free_gb:.3f} GB "
            f"is below hard threshold {abort_c_free_gb:.3f} GB."
        )
    return None


def preflight_full_mh_storage(
    work_dir: Path,
    tmp_dir: Path,
    scratch_output_dir: Path,
    min_free_gb: float = DEFAULT_MIN_EXTERNAL_FREE_GB,
    min_c_free_gb: float = DEFAULT_MIN_C_FREE_GB,
    *,
    create_dirs: bool = True,
    disk_usage_func: Any = shutil.disk_usage,
    drive_exists_func: Any | None = None,
    c_drive_root: Path = Path("C:/"),
) -> dict[str, Any]:
    drive_exists = drive_exists_func if drive_exists_func is not None else Path.exists
    storage_root = _drive_root(scratch_output_dir)
    c_root = c_drive_root if c_drive_root.exists() else _drive_root(repo_root())
    errors: list[str] = []
    checked_dirs = [work_dir, tmp_dir, scratch_output_dir]

    if not drive_exists(storage_root):
        errors.append(f"External scratch drive does not exist: {storage_root}")
        return {
            "status": "failed",
            "external_drive": str(storage_root),
            "external_free_gb": None,
            "c_drive": str(c_root),
            "c_free_gb": None,
            "required_external_free_gb": min_free_gb,
            "required_c_free_gb": min_c_free_gb,
            "checked_directories": [str(path) for path in checked_dirs],
            "errors": errors,
        }

    if create_dirs:
        for directory in checked_dirs:
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                errors.append(f"Could not create directory {directory}: {exc}")

    for directory in checked_dirs:
        if not directory.exists():
            errors.append(f"Directory does not exist: {directory}")
            continue
        probe = directory / ".samba_write_probe"
        try:
            probe.write_text("ok\n", encoding="utf-8")
            probe.unlink(missing_ok=True)
        except OSError as exc:
            errors.append(f"Directory is not writable: {directory}: {exc}")

    external_free_gb = None
    c_free_gb = None
    try:
        external_free_gb = _free_gb(storage_root, disk_usage_func)
    except OSError as exc:
        errors.append(f"Could not read free space for {storage_root}: {exc}")
    try:
        c_free_gb = _free_gb(c_root, disk_usage_func)
    except OSError as exc:
        errors.append(f"Could not read free space for {c_root}: {exc}")

    if external_free_gb is not None and external_free_gb < min_free_gb:
        errors.append(
            f"External scratch drive has {external_free_gb:.3f} GB free; "
            f"requires at least {min_free_gb:.3f} GB."
        )
    if c_free_gb is not None and c_free_gb < min_c_free_gb:
        errors.append(
            f"C: safety margin has {c_free_gb:.3f} GB free; "
            f"requires at least {min_c_free_gb:.3f} GB."
        )

    return {
        "status": "failed" if errors else "passed",
        "external_drive": str(storage_root),
        "external_free_gb": round(external_free_gb, 3)
        if external_free_gb is not None
        else None,
        "c_drive": str(c_root),
        "c_free_gb": round(c_free_gb, 3) if c_free_gb is not None else None,
        "required_external_free_gb": min_free_gb,
        "required_c_free_gb": min_c_free_gb,
        "checked_directories": [str(path) for path in checked_dirs],
        "errors": errors,
    }


def build_dynare_command(dynare_executable: str) -> list[str]:
    return [dynare_executable, "samba_classic.mod", "noclearall", "nolog"]


def copy_model_inputs(source_dir: Path, target_dir: Path) -> None:
    missing = [name for name in REQUIRED_MODEL_FILES if not (source_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing required Dynare model inputs: " + ", ".join(missing)
        )

    for name in REQUIRED_MODEL_FILES:
        shutil.copy2(source_dir / name, target_dir / name)


def write_likelihood_data(root: Path, target_dir: Path) -> dict[str, Any]:
    source = model_input_file(root)
    if not source.is_file():
        raise FileNotFoundError(f"Missing approved model input data: {source}")

    with source.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    missing = [
        source_column
        for column in LIKELIHOOD_OBSERVABLE_COLUMNS
        for source_column in [LIKELIHOOD_COLUMN_MAP.get(column, column)]
        if rows and source_column not in rows[0]
    ]
    if missing:
        raise ValueError(
            "Missing required likelihood data columns: " + ", ".join(sorted(set(missing)))
        )

    numeric_rows = [
        {
            key: float(value)
            for key, value in row.items()
            if key != "quarter"
        }
        for row in rows
    ]
    transformed: dict[str, list[float]] = {}
    for column in LOG_DIFF_DEMEAN_COLUMNS:
        values = [
            math.log(numeric_rows[index][column])
            - math.log(numeric_rows[index - 1][column])
            for index in range(1, len(numeric_rows))
        ]
        mean_value = sum(values) / len(values)
        transformed[column] = [value - mean_value for value in values]

    q_values = [row["q"] for row in numeric_rows]
    q_mean = sum(q_values) / len(q_values)
    q_percent_deviation = [100.0 * (value / q_mean - 1.0) for value in q_values][1:]
    transformed["q"] = q_percent_deviation

    r_values = [row["r"] for row in numeric_rows]
    r_mean = sum(r_values) / len(r_values)
    transformed["r_t"] = [value - r_mean for value in r_values][1:]

    observation_count = len(next(iter(transformed.values())))
    target = target_dir / LIKELIHOOD_DATA_FILE
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LIKELIHOOD_OBSERVABLE_COLUMNS)
        writer.writeheader()
        for index in range(observation_count):
            writer.writerow(
                {
                    column: f"{transformed[column][index]:.15g}"
                    for column in LIKELIHOOD_OBSERVABLE_COLUMNS
                }
            )

    return {
        "likelihood_data_source": str(source),
        "likelihood_data_file": LIKELIHOOD_DATA_FILE,
        "likelihood_observable_columns": list(LIKELIHOOD_OBSERVABLE_COLUMNS),
        "likelihood_observation_count": observation_count,
        "likelihood_data_transformations": {
            "y_c_i_g": "first log-difference, demeaned",
            "q": "percent difference from sample mean",
            "r_t": "demeaned level, using source column r",
        },
    }


def _tail(text: str | bytes | None, max_lines: int = 25, max_chars: int = 4000) -> str:
    if text is None:
        return ""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    lines = text.splitlines()[-max_lines:]
    return "\n".join(lines)[-max_chars:]


def _decode_output(text: str | bytes | None) -> str:
    if text is None:
        return ""
    if isinstance(text, bytes):
        return text.decode("utf-8", errors="replace")
    return text


def terminate_process_tree(pid: int) -> dict[str, Any]:
    if sys.platform.startswith("win"):
        completed = subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "pid": pid,
            "method": "taskkill /T /F",
            "returncode": completed.returncode,
            "stdout_tail": _tail(completed.stdout, 5, 1000),
            "stderr_tail": _tail(completed.stderr, 5, 1000),
        }
    try:
        os.kill(pid, 9)
        return {"pid": pid, "method": "os.kill", "returncode": 0}
    except OSError as exc:
        return {
            "pid": pid,
            "method": "os.kill",
            "returncode": 1,
            "stderr_tail": str(exc),
        }


def _start_stream_reader(
    stream: Any,
) -> tuple[list[str], threading.Thread | None]:
    chunks: list[str] = []
    if stream is None:
        return chunks, None

    def _reader() -> None:
        try:
            for line in iter(stream.readline, ""):
                chunks.append(line)
        except ValueError:
            return

    thread = threading.Thread(target=_reader, daemon=True)
    thread.start()
    return chunks, thread


def _join_stream_readers(
    stdout_chunks: list[str],
    stderr_chunks: list[str],
    stdout_thread: threading.Thread | None,
    stderr_thread: threading.Thread | None,
    *,
    timeout_seconds: float = 30,
) -> tuple[str, str]:
    for thread in (stdout_thread, stderr_thread):
        if thread is not None:
            thread.join(timeout=timeout_seconds)
    return "".join(stdout_chunks), "".join(stderr_chunks)


def _collect_after_cleanup(
    process: subprocess.Popen[str],
    stdout_chunks: list[str],
    stderr_chunks: list[str],
    stdout_thread: threading.Thread | None,
    stderr_thread: threading.Thread | None,
) -> tuple[str, str]:
    try:
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    return _join_stream_readers(
        stdout_chunks,
        stderr_chunks,
        stdout_thread,
        stderr_thread,
    )


def _cleanup_runtime_process_tree(
    child_pid: int,
    runtime_pids_before: set[int],
) -> list[dict[str, Any]]:
    cleanup_records = [terminate_process_tree(child_pid)]
    for pid in runtime_process_ids() - runtime_pids_before:
        if pid == child_pid:
            continue
        cleanup_records.append(terminate_process_tree(pid))
    return cleanup_records


def _run_command(
    command: list[str],
    cwd: Path,
    timeout_seconds: int,
    env: dict[str, str] | None = None,
    disk_monitor: dict[str, Any] | None = None,
) -> subprocess.CompletedProcess[str]:
    use_shell = sys.platform.startswith("win") and Path(command[0]).suffix.lower() in {
        ".bat",
        ".cmd",
    }
    popen_command: str | list[str] = (
        subprocess.list2cmdline(command) if use_shell else command
    )
    runtime_pids_before = runtime_process_ids()
    process = subprocess.Popen(
        popen_command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=use_shell,
        env=env,
    )
    stdout_chunks, stdout_thread = _start_stream_reader(process.stdout)
    stderr_chunks, stderr_thread = _start_stream_reader(process.stderr)
    started = time.monotonic()
    deadline = started + timeout_seconds
    last_telemetry_at: float | None = None
    interval_seconds = float(
        (disk_monitor or {}).get(
            "interval_seconds",
            DEFAULT_DISK_TELEMETRY_INTERVAL_SECONDS,
        )
    )
    interval_seconds = max(interval_seconds, 0.1)

    try:
        while True:
            if process.poll() is not None:
                process.wait()
                stdout, stderr = _join_stream_readers(
                    stdout_chunks,
                    stderr_chunks,
                    stdout_thread,
                    stderr_thread,
                )
                return subprocess.CompletedProcess(
                    command,
                    process.returncode,
                    stdout,
                    stderr,
                )

            now = time.monotonic()
            if now >= deadline:
                cleanup_records = _cleanup_runtime_process_tree(
                    process.pid,
                    runtime_pids_before,
                )
                stdout, stderr = _collect_after_cleanup(
                    process,
                    stdout_chunks,
                    stderr_chunks,
                    stdout_thread,
                    stderr_thread,
                )
                timeout_error = subprocess.TimeoutExpired(
                    cmd=command,
                    timeout=timeout_seconds,
                    output=stdout,
                    stderr=stderr,
                )
                timeout_error.cleanup_records = cleanup_records  # type: ignore[attr-defined]
                raise timeout_error

            if disk_monitor is not None and (
                last_telemetry_at is None
                or now - last_telemetry_at >= interval_seconds
            ):
                record = disk_telemetry_record(
                    c_drive_root=disk_monitor["c_drive_root"],
                    d_drive_root=disk_monitor["d_drive_root"],
                    child_pid=process.pid,
                    elapsed_seconds=now - started,
                    disk_usage_func=disk_monitor.get("disk_usage_func", shutil.disk_usage),
                )
                telemetry_file = disk_monitor.get("telemetry_file")
                if telemetry_file is not None:
                    write_disk_telemetry_record(Path(telemetry_file), record)
                reason = disk_abort_reason(
                    record,
                    abort_d_free_gb=disk_monitor.get(
                        "abort_d_free_gb",
                        DEFAULT_ABORT_D_FREE_GB,
                    ),
                    abort_c_free_gb=disk_monitor.get(
                        "abort_c_free_gb",
                        DEFAULT_ABORT_C_FREE_GB,
                    ),
                )
                if reason is not None:
                    cleanup_records = _cleanup_runtime_process_tree(
                        process.pid,
                        runtime_pids_before,
                    )
                    stdout, stderr = _collect_after_cleanup(
                        process,
                        stdout_chunks,
                        stderr_chunks,
                        stdout_thread,
                        stderr_thread,
                    )
                    raise DynareCommandAborted(
                        reason,
                        DISK_ABORT_RETURNCODE,
                        stdout=stdout,
                        stderr=stderr,
                        cleanup_records=cleanup_records,
                        telemetry_record=record,
                    )
                last_telemetry_at = now

            sleep_seconds = min(1.0, max(0.1, deadline - now))
            time.sleep(sleep_seconds)
    except KeyboardInterrupt:
        cleanup_records = _cleanup_runtime_process_tree(
            process.pid,
            runtime_pids_before,
        )
        stdout, stderr = _collect_after_cleanup(
            process,
            stdout_chunks,
            stderr_chunks,
            stdout_thread,
            stderr_thread,
        )
        raise DynareCommandAborted(
            "Full-MH interrupted; Dynare/Octave process tree cleanup was requested.",
            INTERRUPT_RETURNCODE,
            stdout=stdout,
            stderr=stderr,
            cleanup_records=cleanup_records,
        ) from None
    except (DynareCommandAborted, subprocess.TimeoutExpired):
        raise
    except Exception:
        if process.poll() is None:
            _cleanup_runtime_process_tree(process.pid, runtime_pids_before)
        raise


RESIDUAL_RE = re.compile(
    r"Equation number\s+\d+:\s+.*?:\s+([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?|NaN|Inf|-Inf)\s*$"
)
BK_COUNT_RE = re.compile(
    r"There are\s+(\d+)\s+eigenvalue\(s\) larger than 1 in modulus for\s+(\d+)\s+forward-looking variable\(s\)\."
)


def _parse_residuals(stdout: str) -> dict[str, Any]:
    values = []
    nonfinite = 0
    for line in stdout.splitlines():
        match = RESIDUAL_RE.search(line)
        if not match:
            continue
        token = match.group(1)
        value = float(token)
        values.append(value)
        if not math.isfinite(value):
            nonfinite += 1

    finite_abs = [abs(value) for value in values if math.isfinite(value)]
    return {
        "residual_equation_count": len(values),
        "nonfinite_residual_count": nonfinite,
        "max_abs_residual": max(finite_abs) if finite_abs else None,
    }


def _parse_bk(stdout: str) -> dict[str, Any]:
    eigenvalues_larger_than_one = None
    forward_looking_variables = None
    for line in stdout.splitlines():
        match = BK_COUNT_RE.search(line)
        if match:
            eigenvalues_larger_than_one = int(match.group(1))
            forward_looking_variables = int(match.group(2))
            break

    combined_verified = "The order and rank conditions are verified." in stdout
    order_verified = combined_verified or "The order condition is verified." in stdout
    rank_verified = combined_verified or "The rank condition is verified." in stdout
    order_not_verified = "The order condition is NOT verified." in stdout
    indeterminacy = "indeterminacy" in stdout.lower()

    return {
        "eigenvalues_larger_than_one": eigenvalues_larger_than_one,
        "forward_looking_variables": forward_looking_variables,
        "bk_order_condition_verified": order_verified,
        "bk_rank_condition_verified": rank_verified,
        "bk_order_condition_not_verified": order_not_verified,
        "bk_indeterminacy_reported": indeterminacy,
    }


LIKELIHOOD_LINE_RE = re.compile(r"(log|likelihood|posterior)", re.IGNORECASE)
NUMBER_RE = re.compile(
    r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?|NaN|Inf|-Inf"
)
NONFINITE_RE = re.compile(r"(?<![A-Za-z])(?:NaN|[-+]?Inf|Infinity)(?![A-Za-z])", re.IGNORECASE)


def _parse_likelihood(stdout: str, stderr: str) -> dict[str, Any]:
    likelihood_lines = [
        line.strip()
        for line in (stdout + "\n" + stderr).splitlines()
        if LIKELIHOOD_LINE_RE.search(line)
    ]
    tokens = [
        token
        for line in likelihood_lines
        for token in NUMBER_RE.findall(line)
    ]
    values = [float(token) for token in tokens]
    finite_values = [value for value in values if math.isfinite(value)]
    nonfinite_values = [value for value in values if not math.isfinite(value)]

    return {
        "likelihood_lines_found": len(likelihood_lines),
        "likelihood_numeric_values_found": len(values),
        "likelihood_nonfinite_value_count": len(nonfinite_values),
        "finite_likelihood_reported": bool(finite_values) and not nonfinite_values,
        "likelihood_last_finite_value": finite_values[-1] if finite_values else None,
    }


def _parse_mh_acceptance(
    stdout: str,
    stderr: str,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    mh_config = config if config is not None else MH_PILOT_CONFIG
    text = stdout + "\n" + stderr
    acceptance_values = []
    acceptance_lines = []
    in_acceptance_block = 0
    for line in text.splitlines():
        lower_line = line.lower()
        if "acceptance ratio" in lower_line:
            in_acceptance_block = 8
        candidate_line = "accept" in lower_line or (in_acceptance_block > 0 and "chain" in lower_line)
        if in_acceptance_block > 0:
            in_acceptance_block -= 1
        if not candidate_line:
            continue
        values = [
            float(value)
            for value in NUMBER_RE.findall(line)
            if value.lower() not in {"inf", "-inf", "nan"}
        ]
        if not values:
            continue
        value = values[-1]
        if value > 1.0 and value <= 100.0:
            value = value / 100.0
        if 0.0 <= value <= 1.0:
            acceptance_values.append(value)
            acceptance_lines.append(line.strip())

    acceptance_ratio = (
        sum(acceptance_values) / len(acceptance_values)
        if acceptance_values
        else None
    )
    acceptance_in_band = (
        acceptance_ratio is not None
        and mh_config["target_acceptance_min"]
        <= acceptance_ratio
        <= mh_config["target_acceptance_max"]
    )
    nonfinite_tokens = []
    for line in text.splitlines():
        lower_line = line.lower()
        if "pstdev" in lower_line or ("invg" in lower_line and "inf" in lower_line):
            continue
        nonfinite_tokens.extend(NONFINITE_RE.findall(line))
    return {
        "mh_acceptance_values": acceptance_values,
        "mh_acceptance_ratio": acceptance_ratio,
        "mh_acceptance_in_target_band": acceptance_in_band,
        "mh_acceptance_lines_found": len(acceptance_lines),
        "mh_acceptance_lines": acceptance_lines[-5:],
        "mh_chains_completed": len(acceptance_values) >= mh_config["chains"],
        "mh_nonfinite_token_count": len(nonfinite_tokens),
        "mh_nonfinite_tokens": nonfinite_tokens[:10],
        "rhat_status": "unavailable_warning",
        "rhat_value": None,
        "rhat_policy": mh_config["rhat_policy"],
    }


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _generated_file_manifest(
    temp_dir: Path,
    raw_output_dir: Path | None = None,
) -> dict[str, Any]:
    copied_inputs = set(REQUIRED_MODEL_FILES) | {LIKELIHOOD_DATA_FILE}
    entries = []
    for path in sorted(item for item in temp_dir.rglob("*") if item.is_file()):
        relative = path.relative_to(temp_dir).as_posix()
        if relative in copied_inputs:
            continue
        size = path.stat().st_size
        is_raw_chain = (
            "metropolis/" in relative
            and "_mh" in path.name
            and path.suffix.lower() == ".mat"
        )
        external_raw_path = None
        if is_raw_chain and raw_output_dir is not None:
            external_raw_path = raw_output_dir / relative
            external_raw_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, external_raw_path)
        should_hash = not is_raw_chain or size <= RAW_ARTIFACT_HASH_MAX_BYTES
        entries.append(
            {
                "path": relative,
                "size_bytes": size,
                "sha256": _file_sha256(path) if should_hash else None,
                "sha256_skipped_reason": (
                    "raw artifact exceeds practical hash threshold"
                    if not should_hash
                    else None
                ),
                "raw_chain_artifact": is_raw_chain,
                "external_raw_artifact": (
                    str(external_raw_path)
                    if external_raw_path is not None
                    else None
                ),
                "external_untracked": is_raw_chain,
                "committed_to_git": False,
            }
        )
    raw_entries = [entry for entry in entries if entry["raw_chain_artifact"]]
    return {
        "generated_artifact_count": len(entries),
        "generated_artifact_total_bytes": sum(entry["size_bytes"] for entry in entries),
        "raw_chain_artifact_count": len(raw_entries),
        "raw_chain_artifact_total_bytes": sum(entry["size_bytes"] for entry in raw_entries),
        "raw_chain_artifacts_committed": False,
        "raw_chain_artifacts_intentionally_untracked": True,
        "generated_artifacts": entries,
    }


def _compute_rhat_from_metropolis(temp_dir: Path, drop_fraction: float) -> dict[str, Any]:
    try:
        import numpy as np
        from scipy.io import loadmat
    except Exception as exc:  # pragma: no cover - dependency availability varies.
        return {
            "rhat_status": "unavailable",
            "rhat_value": None,
            "rhat_error": f"R-hat dependencies unavailable: {type(exc).__name__}: {exc}",
        }

    chain_files = sorted(temp_dir.rglob("*_mh*_blck*.mat"))
    if not chain_files:
        return {
            "rhat_status": "unavailable",
            "rhat_value": None,
            "rhat_error": "No Dynare metropolis chain files found.",
        }

    chains: dict[int, list[tuple[int, Any]]] = {}
    for path in chain_files:
        match = re.search(r"_mh(\d+)_blck(\d+)\.mat$", path.name)
        if match is None:
            continue
        file_index = int(match.group(1))
        block_index = int(match.group(2))
        try:
            data = loadmat(path)
        except Exception:
            continue
        draws = data.get("x2")
        if draws is None:
            continue
        chains.setdefault(block_index, []).append((file_index, draws))

    chain_arrays = []
    for block_index in sorted(chains):
        pieces = [
            draws
            for _, draws in sorted(chains[block_index], key=lambda item: item[0])
        ]
        if not pieces:
            continue
        chain = np.vstack(pieces)
        if chain.ndim != 2:
            continue
        drop = int(math.ceil(chain.shape[0] * drop_fraction))
        kept = chain[drop:, :]
        if kept.shape[0] >= 2:
            chain_arrays.append(kept)

    if len(chain_arrays) < 2:
        return {
            "rhat_status": "unavailable",
            "rhat_value": None,
            "rhat_error": "Fewer than two post-burn-in chains available.",
            "rhat_chain_count": len(chain_arrays),
        }

    draw_count = min(chain.shape[0] for chain in chain_arrays)
    parameter_count = min(chain.shape[1] for chain in chain_arrays)
    sample = np.stack(
        [chain[-draw_count:, :parameter_count] for chain in chain_arrays],
        axis=0,
    )
    chain_count = sample.shape[0]
    chain_means = np.mean(sample, axis=1)
    chain_variances = np.var(sample, axis=1, ddof=1)
    between = draw_count * np.var(chain_means, axis=0, ddof=1)
    within = np.mean(chain_variances, axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        variance_hat = ((draw_count - 1) / draw_count) * within + between / draw_count
        rhat_values = np.sqrt(variance_hat / within)
    finite = rhat_values[np.isfinite(rhat_values)]
    if finite.size == 0:
        return {
            "rhat_status": "unavailable",
            "rhat_value": None,
            "rhat_error": "R-hat values were not finite.",
            "rhat_chain_count": chain_count,
            "rhat_draws_per_chain": draw_count,
            "rhat_parameter_count": parameter_count,
        }

    max_rhat = float(np.max(finite))
    status = "computed" if max_rhat <= FULL_MH_CONFIG["rhat_max"] else "above_threshold"
    return {
        "rhat_status": status,
        "rhat_value": max_rhat,
        "rhat_max": max_rhat,
        "rhat_chain_count": chain_count,
        "rhat_draws_per_chain": draw_count,
        "rhat_parameter_count": parameter_count,
        "rhat_values": [float(value) for value in rhat_values[:parameter_count]],
        "rhat_policy": FULL_MH_CONFIG["rhat_policy"],
    }


def _write_full_mh_artifacts(
    root: Path,
    result: dict[str, Any],
    repo_output_dir: Path | None = None,
) -> dict[str, Any]:
    output_dir = repo_output_dir if repo_output_dir is not None else full_mh_output_dir(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / FULL_MH_ARTIFACT_FILENAMES["summary"]
    diagnostics_path = output_dir / FULL_MH_ARTIFACT_FILENAMES["diagnostics"]
    manifest_path = output_dir / FULL_MH_ARTIFACT_FILENAMES["manifest"]

    summary = {
        key: value
        for key, value in result.items()
        if key not in {"stdout_tail", "stderr_tail", "generated_artifact_manifest"}
    }
    summary.update(
        {
            "wbs": "WBS-073",
            "full_mh_created": result["status"] == "passed",
            "posterior_inference_claimed": False,
            "publication_grade_posterior_evidence": False,
            "manifest": _path_for_manifest(manifest_path, root),
        }
    )
    manifest = {
        "wbs": "WBS-073",
        "summary_artifact": _path_for_manifest(summary_path, root),
        "diagnostics_artifact": _path_for_manifest(diagnostics_path, root),
        "manifest_artifact": _path_for_manifest(manifest_path, root),
        "committed_artifacts": [
            _path_for_manifest(summary_path, root),
            _path_for_manifest(diagnostics_path, root),
            _path_for_manifest(manifest_path, root),
        ],
        "raw_heavy_chain_artifacts_committed": False,
        "raw_heavy_chain_artifacts_intentionally_untracked": True,
        **result["generated_artifact_manifest"],
    }
    diagnostics = "\n".join(
        [
            "# WBS-073 Full MH Diagnostics",
            "",
            f"Status: {result['status']}.",
            "",
            f"Command: `{' '.join(str(part) for part in result['command'])}`",
            "",
            "Configuration:",
            f"- `mh_replic`: {result['mh_replic']} per chain",
            f"- chains: {result['chains']}",
            f"- Dynare `mh_nblocks`: {result['mh_nblocks']}",
            f"- approved blocks metadata: {result['approved_blocks']}",
            f"- burn-in: {result['mh_drop']}",
            f"- `mh_jscale`: {result['mh_jscale']}",
            "",
            "Diagnostics:",
            f"- finite likelihood reported: {result['finite_likelihood_reported']}",
            f"- acceptance values: {result['mh_acceptance_values']}",
            f"- average acceptance ratio: {result['mh_acceptance_ratio']}",
            f"- R-hat status: {result['rhat_status']}",
            f"- max R-hat: {result['rhat_value']}",
            f"- raw chain artifacts committed: {manifest['raw_heavy_chain_artifacts_committed']}",
            "",
            "This is full-MH operational validation, not final publication-grade posterior evidence.",
            "WBS-074, backtesting, Redux, and sovereign-extension work remain forbidden until explicitly approved.",
            "",
        ]
    )

    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    diagnostics_path.write_text(diagnostics, encoding="utf-8")
    return {
        "summary_artifact": _path_for_manifest(summary_path, root),
        "diagnostics_artifact": _path_for_manifest(diagnostics_path, root),
        "manifest_artifact": _path_for_manifest(manifest_path, root),
    }


def _parse_fenced_csv(text: str, marker: str) -> list[dict[str, str]]:
    start = text.index(marker)
    fenced = text.index("```csv", start)
    body_start = text.index("\n", fenced) + 1
    body_end = text.index("```", body_start)
    return list(csv.DictReader(text[body_start:body_end].splitlines()))


def load_irf_targets(root: Path | None = None) -> list[dict[str, str]]:
    path = irf_targets_file(root)
    if not path.exists():
        return []
    rows = _parse_fenced_csv(path.read_text(encoding="utf-8"), "## Target rows")
    return [row for row in rows if row["status"] == "approved_for_wbs063"]


def _read_irf_series(path: Path) -> dict[str, list[float]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle)
        return {
            row["field"]: [
                float(row[f"h{horizon}"])
                for horizon in range(1, IRF_HORIZON + 1)
            ]
            for row in rows
        }


def _window_values(series: list[float], start: int, end: int) -> list[float]:
    return series[start - 1:end]


def evaluate_irf_targets(
    targets: list[dict[str, str]],
    irf_series: dict[str, list[float]],
) -> dict[str, Any]:
    results = []
    failures = []
    for target in targets:
        field = target["irf_field"]
        values = irf_series.get(field)
        if values is None:
            result = {
                "target_id": target["target_id"],
                "passed": False,
                "reason": f"missing_irf_field:{field}",
            }
            results.append(result)
            failures.append(result)
            continue

        window_start = int(target["sign_window_start"])
        window_end = int(target["sign_window_end"])
        window = _window_values(values, window_start, window_end)
        expected_sign = target["expected_sign"]
        if expected_sign == "positive":
            sign_passed = (
                all(value >= -IRF_EPSILON for value in window)
                and any(value > IRF_EPSILON for value in window)
            )
        elif expected_sign == "negative":
            sign_passed = (
                all(value <= IRF_EPSILON for value in window)
                and any(value < -IRF_EPSILON for value in window)
            )
        else:
            sign_passed = False

        return_horizon = int(target["return_horizon"])
        peak_abs = max(abs(value) for value in window)
        terminal_abs = abs(values[return_horizon - 1])
        return_rule = target["return_rule"]
        return_passed = (
            return_rule == "abs_at_return_horizon_less_than_window_peak"
            and terminal_abs < peak_abs
        )

        result = {
            "target_id": target["target_id"],
            "irf_field": field,
            "passed": sign_passed and return_passed,
            "sign_passed": sign_passed,
            "return_passed": return_passed,
            "window_peak_abs": peak_abs,
            "return_horizon_abs": terminal_abs,
        }
        results.append(result)
        if not result["passed"]:
            failures.append(result)

    return {
        "irf_restrictions_evaluated": bool(targets),
        "irf_target_count": len(targets),
        "irf_targets_passed": len(targets) - len(failures),
        "irf_targets_failed": len(failures),
        "irf_failures": failures,
        "irf_target_results": results,
    }


def run_dynare(
    mode: str = "smoke",
    dynare_executable: str = "dynare",
    timeout_seconds: int = 180,
    residual_tolerance: float = 1e-8,
    mh_jscale: float | None = None,
    work_dir: str | Path | None = None,
    tmp_dir: str | Path | None = None,
    scratch_output_dir: str | Path | None = None,
    repo_output_dir: str | Path | None = None,
    min_free_gb: float = DEFAULT_MIN_EXTERNAL_FREE_GB,
    min_c_free_gb: float = DEFAULT_MIN_C_FREE_GB,
    abort_d_free_gb: float = DEFAULT_ABORT_D_FREE_GB,
    abort_c_free_gb: float = DEFAULT_ABORT_C_FREE_GB,
    disk_telemetry_file: str | Path | None = None,
    disk_telemetry_interval_seconds: float = DEFAULT_DISK_TELEMETRY_INTERVAL_SECONDS,
) -> dict[str, Any]:
    root = repo_root()
    source_dir = samba_model_dir(root)
    normalized_requested_mode = "irfs" if mode == "irf" else mode
    if mode == "likelihood":
        normalized_requested_mode = "likelihood-smoke"
    if mode in {
        "posterior-mode",
        "estimation-smoke",
        "mh-pilot",
        "full-mh",
    }:
        normalized_requested_mode = mode
    dynare_path = shutil.which(dynare_executable)
    if dynare_path is None:
        return {
            "mode": mode,
            "status": "unavailable",
            "returncode": 127,
            "model_file": str(source_dir / "samba_classic.mod"),
            "error": f"Dynare executable not found on PATH: {dynare_executable}",
        }
    if mh_jscale is not None and mh_jscale <= 0:
        return {
            "mode": mode,
            "status": "failed",
            "returncode": 2,
            "model_file": str(source_dir / "samba_classic.mod"),
            "error": "mh_jscale must be positive when provided.",
        }

    full_mh_storage: dict[str, Any] = {}
    full_mh_paths = default_full_mh_storage_paths(root)
    if normalized_requested_mode == "full-mh":
        resolved_work_dir = _resolve_repo_relative_path(
            work_dir,
            full_mh_paths["work_dir"],
            root,
        )
        resolved_tmp_dir = _resolve_repo_relative_path(
            tmp_dir,
            full_mh_paths["tmp_dir"],
            root,
        )
        resolved_scratch_output_dir = _resolve_repo_relative_path(
            scratch_output_dir,
            full_mh_paths["scratch_output_dir"],
            root,
        )
        resolved_repo_output_dir = _resolve_repo_relative_path(
            repo_output_dir,
            full_mh_paths["repo_output_dir"],
            root,
        )
        resolved_disk_telemetry_file = _resolve_repo_relative_path(
            disk_telemetry_file,
            DEFAULT_DISK_TELEMETRY_FILE,
            root,
        )
        preflight = preflight_full_mh_storage(
            resolved_work_dir,
            resolved_tmp_dir,
            resolved_scratch_output_dir,
            min_free_gb,
            min_c_free_gb,
        )
        full_mh_storage = {
            "storage_preflight": preflight,
            "work_dir": str(resolved_work_dir),
            "tmp_dir": str(resolved_tmp_dir),
            "scratch_output_dir": str(resolved_scratch_output_dir),
            "repo_output_dir": _path_for_manifest(resolved_repo_output_dir, root),
            "disk_telemetry_file": _path_for_manifest(
                resolved_disk_telemetry_file,
                root,
            ),
            "disk_telemetry_interval_seconds": disk_telemetry_interval_seconds,
            "abort_d_free_gb": abort_d_free_gb,
            "abort_c_free_gb": abort_c_free_gb,
        }
        if preflight["status"] != "passed":
            return {
                "mode": "full-mh",
                "status": "failed",
                "returncode": 2,
                "model_file": str(source_dir / "samba_classic.mod"),
                "error": "Full-MH storage preflight failed before starting Dynare.",
                **full_mh_storage,
            }
        temp_context = contextlib.nullcontext(str(resolved_work_dir))
        command_env = os.environ.copy()
        command_env.update(
            {
                "TEMP": str(resolved_tmp_dir),
                "TMP": str(resolved_tmp_dir),
                "TMPDIR": str(resolved_tmp_dir),
            }
        )
        disk_monitor = {
            "c_drive_root": Path("C:/"),
            "d_drive_root": _drive_root(resolved_scratch_output_dir),
            "abort_d_free_gb": abort_d_free_gb,
            "abort_c_free_gb": abort_c_free_gb,
            "telemetry_file": resolved_disk_telemetry_file,
            "interval_seconds": disk_telemetry_interval_seconds,
        }
    else:
        resolved_scratch_output_dir = full_mh_paths["scratch_output_dir"]
        resolved_repo_output_dir = full_mh_paths["repo_output_dir"]
        resolved_disk_telemetry_file = _resolve_repo_relative_path(
            disk_telemetry_file,
            DEFAULT_DISK_TELEMETRY_FILE,
            root,
        )
        command_env = None
        disk_monitor = None
        temp_context = tempfile.TemporaryDirectory(prefix="samba_dynare_")

    with temp_context as temp_dir_raw:
        temp_dir = Path(temp_dir_raw)
        try:
            copy_model_inputs(source_dir, temp_dir)
        except FileNotFoundError as exc:
            return {
                "mode": "smoke",
                "status": "failed",
                "returncode": 2,
                "model_file": str(source_dir / "samba_classic.mod"),
                "error": str(exc),
            }

        if mode == "residuals":
            with (temp_dir / "samba_classic.mod").open("a", encoding="utf-8") as handle:
                handle.write("\nresid;\n")
        if mode == "bk":
            with (temp_dir / "samba_classic.mod").open("a", encoding="utf-8") as handle:
                handle.write("\nsteady;\ncheck;\n")
        normalized_mode = normalized_requested_mode
        likelihood_data = {}
        estimation_options: dict[str, Any] = {}
        estimation_modes = {
            "likelihood-smoke",
            "posterior-mode",
            "estimation-smoke",
            "mh-pilot",
            "full-mh",
        }
        if normalized_mode in estimation_modes:
            try:
                likelihood_data = write_likelihood_data(root, temp_dir)
            except (FileNotFoundError, ValueError) as exc:
                return {
                    "mode": mode,
                    "status": "failed",
                    "returncode": 2,
                    "model_file": str(source_dir / "samba_classic.mod"),
                    "error": str(exc),
                }
            with (temp_dir / "samba_classic.mod").open("a", encoding="utf-8") as handle:
                measurement_error_block = "\n".join(
                    f"var {variable}; stderr {metadata['stderr']};"
                    for variable, metadata in LIKELIHOOD_MEASUREMENT_ERRORS.items()
                )
                mh_config = FULL_MH_CONFIG if normalized_mode == "full-mh" else MH_PILOT_CONFIG
                mode_compute = 4 if normalized_mode in {"posterior-mode", "mh-pilot", "full-mh"} else 0
                mh_replic = mh_config["mh_replic"] if normalized_mode in {"mh-pilot", "full-mh"} else 0
                mh_nblocks = mh_config["mh_nblocks"] if normalized_mode in {"mh-pilot", "full-mh"} else None
                mh_drop = mh_config["mh_drop"] if normalized_mode in {"mh-pilot", "full-mh"} else None
                active_mh_jscale = (
                    mh_jscale if mh_jscale is not None else mh_config.get("mh_jscale")
                )
                estimation_options = {
                    "mode_compute": mode_compute,
                    "mh_replic": mh_replic,
                    "chains": mh_config["chains"] if normalized_mode in {"mh-pilot", "full-mh"} else None,
                    "mh_nblocks": mh_nblocks,
                    "mh_drop": mh_drop,
                    "mh_jscale": active_mh_jscale if normalized_mode in {"mh-pilot", "full-mh"} else None,
                    "mh_jscale_source": (
                        "cli"
                        if mh_jscale is not None
                        else (
                            "config"
                            if active_mh_jscale is not None
                            else "dynare_default"
                        )
                    )
                    if normalized_mode in {"mh-pilot", "full-mh"}
                    else None,
                    "dynare_default_mh_jscale": (
                        MH_PILOT_CONFIG["dynare_default_mh_jscale"]
                        if normalized_mode == "mh-pilot"
                        else None
                    ),
                    "approved_blocks": (
                        FULL_MH_CONFIG["approved_blocks"]
                        if normalized_mode == "full-mh"
                        else None
                    ),
                    "target_acceptance_central": (
                        mh_config["target_acceptance_central"]
                        if normalized_mode in {"mh-pilot", "full-mh"}
                        else None
                    ),
                    "estimation_smoke": normalized_mode == "estimation-smoke",
                    "mh_pilot": normalized_mode == "mh-pilot",
                    "full_mh": normalized_mode == "full-mh",
                    "posterior_mode": normalized_mode == "posterior-mode",
                    "persistent_outputs_created": False,
                }
                mh_options = ""
                if normalized_mode in {"mh-pilot", "full-mh"}:
                    mh_options = (
                        f"mh_nblocks={mh_nblocks}, "
                        f"mh_drop={mh_drop}, "
                    )
                    if active_mh_jscale is not None:
                        mh_options += f"mh_jscale={active_mh_jscale}, "
                handle.write(
                    "\nshocks;\n"
                    f"{measurement_error_block}\n"
                    "end;\n"
                    "@#include \"priors.inc\"\n"
                    "estimated_params_init(use_calibration);\n"
                    "end;\n"
                    "estimation("
                    "datafile=classic_mvp_dynare, "
                    f"mode_compute={mode_compute}, "
                    f"mh_replic={mh_replic}, "
                    f"{mh_options}"
                    "lik_init=3, "
                    "diffuse_filter, "
                    "kalman_algo=4, "
                    "nograph, "
                    "nodisplay"
                    ");\n"
                )
        if normalized_mode == "irfs":
            with (temp_dir / "samba_classic.mod").open("a", encoding="utf-8") as handle:
                handle.write(
                    f"\nstoch_simul(order=1, irf={IRF_HORIZON}, nograph, noprint);\n"
                    "fid=fopen('irf_series.csv','w');\n"
                    "fprintf(fid,'field"
                    + "".join(f",h{horizon}" for horizon in range(1, IRF_HORIZON + 1))
                    + "\\n');\n"
                    "fields=fieldnames(oo_.irfs);\n"
                    "for i=1:length(fields)\n"
                    "  v=oo_.irfs.(fields{i});\n"
                    "  fprintf(fid,'%s',fields{i});\n"
                    f"  for j=1:{IRF_HORIZON}\n"
                    "    fprintf(fid,',%.15g',v(j));\n"
                    "  end\n"
                    "  fprintf(fid,'\\n');\n"
                    "end\n"
                    "fclose(fid);\n"
                )

        command = build_dynare_command(dynare_path)
        started = time.monotonic()
        try:
            completed = _run_command(
                command,
                temp_dir,
                timeout_seconds,
                env=command_env,
                disk_monitor=disk_monitor,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = _decode_output(exc.stdout)
            stderr = _decode_output(exc.stderr)
            timeout_result = {
                "mode": mode,
                "status": "failed",
                "returncode": 124,
                "command": command,
                "model_file": str(source_dir / "samba_classic.mod"),
                "working_directory": (
                    "external_scratch"
                    if normalized_mode == "full-mh"
                    else "temporary"
                ),
                "elapsed_seconds": timeout_seconds,
                "stdout_tail": _tail(exc.stdout),
                "stderr_tail": _tail(exc.stderr),
                "process_cleanup": getattr(exc, "cleanup_records", []),
                "error": "Dynare run timed out.",
                **full_mh_storage,
            }
            if normalized_mode == "full-mh":
                full_timeout = {
                    **_parse_mh_acceptance(stdout, stderr, FULL_MH_CONFIG),
                    **_compute_rhat_from_metropolis(temp_dir, FULL_MH_CONFIG["mh_drop"]),
                    "generated_artifact_manifest": _generated_file_manifest(
                        temp_dir,
                        resolved_scratch_output_dir,
                    ),
                }
                timeout_result.update(
                    {
                        **likelihood_data,
                        **estimation_options,
                        **_parse_likelihood(stdout, stderr),
                        **full_timeout,
                        "timeout_artifact_handling": "raw_chain_files_kept_on_external_scratch_if_present",
                        "likelihood_measurement_errors": LIKELIHOOD_MEASUREMENT_ERRORS,
                    }
                )
                timeout_result.update(
                    _write_full_mh_artifacts(
                        root,
                        timeout_result,
                        resolved_repo_output_dir,
                    )
                )
            return timeout_result
        except DynareCommandAborted as exc:
            stdout = _decode_output(exc.stdout)
            stderr = _decode_output(exc.stderr)
            aborted_result = {
                "mode": normalized_mode,
                "status": "failed",
                "returncode": exc.returncode,
                "command": command,
                "model_file": str(source_dir / "samba_classic.mod"),
                "working_directory": (
                    "external_scratch"
                    if normalized_mode == "full-mh"
                    else "temporary"
                ),
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "stdout_tail": _tail(stdout),
                "stderr_tail": _tail(stderr),
                "process_cleanup": exc.cleanup_records,
                "error": exc.reason,
                "disk_abort": exc.returncode == DISK_ABORT_RETURNCODE,
                "disk_abort_telemetry_record": exc.telemetry_record,
                **full_mh_storage,
            }
            if normalized_mode == "full-mh":
                full_abort = {
                    **_parse_mh_acceptance(stdout, stderr, FULL_MH_CONFIG),
                    **_compute_rhat_from_metropolis(temp_dir, FULL_MH_CONFIG["mh_drop"]),
                    "generated_artifact_manifest": _generated_file_manifest(
                        temp_dir,
                        resolved_scratch_output_dir,
                    ),
                }
                aborted_result.update(
                    {
                        **likelihood_data,
                        **estimation_options,
                        **_parse_likelihood(stdout, stderr),
                        **full_abort,
                        "abort_artifact_handling": "raw_chain_files_kept_on_external_scratch_if_present",
                        "likelihood_measurement_errors": LIKELIHOOD_MEASUREMENT_ERRORS,
                    }
                )
                aborted_result.update(
                    _write_full_mh_artifacts(
                        root,
                        aborted_result,
                        resolved_repo_output_dir,
                    )
                )
            return aborted_result

        elapsed = round(time.monotonic() - started, 3)
        residuals = (
            _parse_residuals(completed.stdout)
            if mode == "residuals"
            else {}
        )
        bk = _parse_bk(completed.stdout) if mode == "bk" else {}
        irfs = {}
        if normalized_mode == "irfs":
            targets = load_irf_targets(root)
            irf_series = _read_irf_series(temp_dir / "irf_series.csv")
            irfs = {
                "irf_horizon": IRF_HORIZON,
                "persistent_outputs_created": False,
                **evaluate_irf_targets(targets, irf_series),
            }
        likelihood = (
            _parse_likelihood(completed.stdout, completed.stderr)
            if normalized_mode in estimation_modes
            else {}
        )
        mh_pilot = (
            _parse_mh_acceptance(completed.stdout, completed.stderr)
            if normalized_mode == "mh-pilot"
            else {}
        )
        full_mh = (
            {
                **_parse_mh_acceptance(completed.stdout, completed.stderr, FULL_MH_CONFIG),
                **_compute_rhat_from_metropolis(temp_dir, FULL_MH_CONFIG["mh_drop"]),
                "generated_artifact_manifest": _generated_file_manifest(
                    temp_dir,
                    resolved_scratch_output_dir,
                ),
            }
            if normalized_mode == "full-mh"
            else {}
        )
        status = "passed" if completed.returncode == 0 else "failed"
        returncode = completed.returncode
        if mode == "residuals" and completed.returncode == 0:
            max_abs_residual = residuals["max_abs_residual"]
            residuals_pass = (
                residuals["residual_equation_count"] > 0
                and residuals["nonfinite_residual_count"] == 0
                and max_abs_residual is not None
                and max_abs_residual <= residual_tolerance
            )
            status = "passed" if residuals_pass else "failed"
            returncode = 0 if residuals_pass else 1
        if mode == "bk" and completed.returncode == 0:
            bk_pass = (
                bk["bk_order_condition_verified"]
                and bk["bk_rank_condition_verified"]
                and not bk["bk_order_condition_not_verified"]
                and not bk["bk_indeterminacy_reported"]
            )
            status = "passed" if bk_pass else "failed"
            returncode = 0 if bk_pass else 1
        if normalized_mode == "irfs" and completed.returncode == 0:
            irf_pass = (
                irfs["irf_restrictions_evaluated"]
                and irfs["irf_targets_failed"] == 0
            )
            status = "passed" if irf_pass else "failed"
            returncode = 0 if irf_pass else 1
        if normalized_mode in {"likelihood-smoke", "estimation-smoke"} and completed.returncode == 0:
            likelihood_pass = likelihood["finite_likelihood_reported"]
            status = "passed" if likelihood_pass else "failed"
            returncode = 0 if likelihood_pass else 1
        if normalized_mode == "posterior-mode" and completed.returncode == 0:
            mode_pass = (
                likelihood["finite_likelihood_reported"]
                and "mode" in (completed.stdout + completed.stderr).lower()
            )
            status = "passed" if mode_pass else "failed"
            returncode = 0 if mode_pass else 1
        if normalized_mode == "mh-pilot" and completed.returncode == 0:
            pilot_pass = (
                likelihood["finite_likelihood_reported"]
                and likelihood["likelihood_nonfinite_value_count"] == 0
                and mh_pilot["mh_chains_completed"]
                and mh_pilot["mh_nonfinite_token_count"] == 0
                and mh_pilot["mh_acceptance_in_target_band"]
            )
            status = "passed" if pilot_pass else "failed"
            returncode = 0 if pilot_pass else 1
        if normalized_mode == "mh-pilot" and completed.returncode != 0:
            pilot_pass = (
                likelihood["finite_likelihood_reported"]
                and likelihood["likelihood_nonfinite_value_count"] == 0
                and mh_pilot["mh_chains_completed"]
                and mh_pilot["mh_nonfinite_token_count"] == 0
                and mh_pilot["mh_acceptance_in_target_band"]
            )
            if pilot_pass:
                status = "passed"
                returncode = 0
        if normalized_mode == "full-mh":
            full_mh_pass = (
                likelihood["finite_likelihood_reported"]
                and likelihood["likelihood_nonfinite_value_count"] == 0
                and full_mh["mh_chains_completed"]
                and full_mh["mh_nonfinite_token_count"] == 0
                and full_mh["mh_acceptance_in_target_band"]
                and full_mh["rhat_status"] == "computed"
                and full_mh["rhat_value"] is not None
                and full_mh["rhat_value"] <= FULL_MH_CONFIG["rhat_max"]
            )
            status = "passed" if full_mh_pass else "failed"
            returncode = 0 if full_mh_pass else 1

        result = {
            "mode": normalized_mode,
            "status": status,
            "returncode": returncode,
            "dynare_returncode": completed.returncode,
            "command": command,
            "model_file": str(source_dir / "samba_classic.mod"),
            "working_directory": (
                "external_scratch"
                if normalized_mode == "full-mh"
                else "temporary"
            ),
            "elapsed_seconds": elapsed,
            "residual_tolerance": residual_tolerance if mode == "residuals" else None,
            **full_mh_storage,
            **residuals,
            **bk,
            **irfs,
            **likelihood_data,
            **estimation_options,
            **mh_pilot,
            **full_mh,
            "likelihood_measurement_errors": (
                LIKELIHOOD_MEASUREMENT_ERRORS
                if normalized_mode in estimation_modes
                else None
            ),
            **likelihood,
            "stdout_tail": _tail(completed.stdout),
            "stderr_tail": _tail(completed.stderr),
        }
        if normalized_mode == "full-mh":
            result.update(_write_full_mh_artifacts(root, result, resolved_repo_output_dir))
        return result


def run_smoke(dynare_executable: str = "dynare", timeout_seconds: int = 180) -> dict[str, Any]:
    return run_dynare("smoke", dynare_executable, timeout_seconds)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=(
            "smoke",
            "residuals",
            "bk",
            "irf",
            "irfs",
            "likelihood",
            "likelihood-smoke",
            "posterior-mode",
            "estimation-smoke",
            "mh-pilot",
            "full-mh",
        ),
        default="smoke",
    )
    parser.add_argument("--dynare", default="dynare")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--residual-tolerance", type=float, default=1e-8)
    parser.add_argument(
        "--mh-jscale",
        type=float,
        default=None,
        help="Optional WBS-072 MH pilot proposal scale.",
    )
    parser.add_argument("--work-dir", default=None)
    parser.add_argument("--tmp-dir", default=None)
    parser.add_argument("--scratch-output-dir", default=None)
    parser.add_argument("--repo-output-dir", default=None)
    parser.add_argument(
        "--min-free-gb",
        type=float,
        default=DEFAULT_MIN_EXTERNAL_FREE_GB,
        help="Minimum free GB required on the full-MH scratch drive.",
    )
    parser.add_argument(
        "--min-c-free-gb",
        type=float,
        default=DEFAULT_MIN_C_FREE_GB,
        help="Minimum free GB required on C: for pagefile/cache safety.",
    )
    parser.add_argument(
        "--abort-d-free-gb",
        type=float,
        default=DEFAULT_ABORT_D_FREE_GB,
        help="Hard-abort full-MH if D: free GB falls below this value.",
    )
    parser.add_argument(
        "--abort-c-free-gb",
        type=float,
        default=DEFAULT_ABORT_C_FREE_GB,
        help="Hard-abort full-MH if C: free GB falls below this value.",
    )
    parser.add_argument(
        "--disk-telemetry-file",
        default=None,
        help="JSONL telemetry file for full-MH disk guard records.",
    )
    parser.add_argument(
        "--disk-telemetry-interval-seconds",
        type=float,
        default=DEFAULT_DISK_TELEMETRY_INTERVAL_SECONDS,
        help="Seconds between full-MH disk telemetry records.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    result = run_dynare(
        args.mode,
        args.dynare,
        args.timeout_seconds,
        args.residual_tolerance,
        args.mh_jscale,
        args.work_dir,
        args.tmp_dir,
        args.scratch_output_dir,
        args.repo_output_dir,
        args.min_free_gb,
        args.min_c_free_gb,
        args.abort_d_free_gb,
        args.abort_c_free_gb,
        args.disk_telemetry_file,
        args.disk_telemetry_interval_seconds,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return int(result["returncode"])


if __name__ == "__main__":
    raise SystemExit(main())
