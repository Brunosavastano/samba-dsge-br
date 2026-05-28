"""Run the SAMBA classic Dynare model from a temporary working directory."""

from __future__ import annotations

import argparse
import json
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


def run_smoke(dynare_executable: str = "dynare", timeout_seconds: int = 180) -> dict[str, Any]:
    root = repo_root()
    source_dir = samba_model_dir(root)
    dynare_path = shutil.which(dynare_executable)
    if dynare_path is None:
        return {
            "mode": "smoke",
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

        command = build_dynare_command(dynare_path)
        started = time.monotonic()
        try:
            completed = _run_command(command, temp_dir, timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            return {
                "mode": "smoke",
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
        return {
            "mode": "smoke",
            "status": "passed" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "command": command,
            "model_file": str(source_dir / "samba_classic.mod"),
            "working_directory": "temporary",
            "elapsed_seconds": elapsed,
            "stdout_tail": _tail(completed.stdout),
            "stderr_tail": _tail(completed.stderr),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("smoke",), default="smoke")
    parser.add_argument("--dynare", default="dynare")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()

    result = run_smoke(args.dynare, args.timeout_seconds)
    print(json.dumps(result, indent=2, sort_keys=True))
    return int(result["returncode"])


if __name__ == "__main__":
    raise SystemExit(main())
