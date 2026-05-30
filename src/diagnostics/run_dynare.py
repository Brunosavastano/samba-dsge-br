"""Run the SAMBA classic Dynare model from a temporary working directory."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import time
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


def _run_command(
    command: list[str],
    cwd: Path,
    timeout_seconds: int,
) -> subprocess.CompletedProcess[str]:
    def _run_shell_command() -> subprocess.CompletedProcess[str]:
        process = subprocess.Popen(
            subprocess.list2cmdline(command),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            if sys.platform.startswith("win"):
                subprocess.run(
                    ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            else:
                process.kill()
            stdout, stderr = process.communicate()
            raise subprocess.TimeoutExpired(
                cmd=command,
                timeout=timeout_seconds,
                output=stdout,
                stderr=stderr,
            )
        return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)

    if sys.platform.startswith("win") and Path(command[0]).suffix.lower() in {
        ".bat",
        ".cmd",
    }:
        return _run_shell_command()

    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
        check=False,
    )


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
) -> dict[str, Any]:
    root = repo_root()
    source_dir = samba_model_dir(root)
    dynare_path = shutil.which(dynare_executable)
    if dynare_path is None:
        return {
            "mode": mode,
            "status": "unavailable",
            "returncode": 127,
            "model_file": str(source_dir / "samba_classic.mod"),
            "error": f"Dynare executable not found on PATH: {dynare_executable}",
        }

    with tempfile.TemporaryDirectory(prefix="samba_dynare_") as temp_dir_raw:
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
        normalized_mode = "irfs" if mode == "irf" else mode
        if mode == "likelihood":
            normalized_mode = "likelihood-smoke"
        if mode == "posterior-mode":
            normalized_mode = "posterior-mode"
        likelihood_data = {}
        if normalized_mode in {"likelihood-smoke", "posterior-mode"}:
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
                mode_compute = 0 if normalized_mode == "likelihood-smoke" else 4
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
                    "mh_replic=0, "
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
            completed = _run_command(command, temp_dir, timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            return {
                "mode": mode,
                "status": "failed",
                "returncode": 124,
                "command": command,
                "model_file": str(source_dir / "samba_classic.mod"),
                "working_directory": "temporary",
                "elapsed_seconds": timeout_seconds,
                "stdout_tail": _tail(exc.stdout),
                "stderr_tail": _tail(exc.stderr),
                "error": "Dynare smoke run timed out.",
            }

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
            if normalized_mode in {"likelihood-smoke", "posterior-mode"}
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
        if normalized_mode == "likelihood-smoke" and completed.returncode == 0:
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

        return {
            "mode": normalized_mode,
            "status": status,
            "returncode": returncode,
            "dynare_returncode": completed.returncode,
            "command": command,
            "model_file": str(source_dir / "samba_classic.mod"),
            "working_directory": "temporary",
            "elapsed_seconds": elapsed,
            "residual_tolerance": residual_tolerance if mode == "residuals" else None,
            **residuals,
            **bk,
            **irfs,
            **likelihood_data,
            "likelihood_measurement_errors": (
                LIKELIHOOD_MEASUREMENT_ERRORS
                if normalized_mode in {"likelihood-smoke", "posterior-mode"}
                else None
            ),
            **likelihood,
            "stdout_tail": _tail(completed.stdout),
            "stderr_tail": _tail(completed.stderr),
        }


def run_smoke(dynare_executable: str = "dynare", timeout_seconds: int = 180) -> dict[str, Any]:
    return run_dynare("smoke", dynare_executable, timeout_seconds)


def main() -> int:
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
        ),
        default="smoke",
    )
    parser.add_argument("--dynare", default="dynare")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--residual-tolerance", type=float, default=1e-8)
    args = parser.parse_args()

    result = run_dynare(
        args.mode,
        args.dynare,
        args.timeout_seconds,
        args.residual_tolerance,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return int(result["returncode"])


if __name__ == "__main__":
    raise SystemExit(main())
