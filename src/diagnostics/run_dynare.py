"""Run the SAMBA classic Dynare model from a temporary working directory."""

from __future__ import annotations

import argparse
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
)
IRF_HORIZON = 20


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def samba_model_dir(root: Path | None = None) -> Path:
    base = root if root is not None else repo_root()
    return base / "model" / "samba_classic"


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
    if sys.platform.startswith("win") and Path(command[0]).suffix.lower() in {
        ".bat",
        ".cmd",
    }:
        return subprocess.run(
            subprocess.list2cmdline(command),
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            shell=True,
            check=False,
        )

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
        if mode == "irfs":
            with (temp_dir / "samba_classic.mod").open("a", encoding="utf-8") as handle:
                handle.write(
                    f"\nstoch_simul(order=1, irf={IRF_HORIZON}, nograph, noprint);\n"
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
        irfs = (
            {
                "irf_horizon": IRF_HORIZON,
                "irf_restrictions_evaluated": False,
                "persistent_outputs_created": False,
            }
            if mode == "irfs"
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

        return {
            "mode": mode,
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
            "stdout_tail": _tail(completed.stdout),
            "stderr_tail": _tail(completed.stderr),
        }


def run_smoke(dynare_executable: str = "dynare", timeout_seconds: int = 180) -> dict[str, Any]:
    return run_dynare("smoke", dynare_executable, timeout_seconds)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("smoke", "residuals", "bk", "irfs"), default="smoke")
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
