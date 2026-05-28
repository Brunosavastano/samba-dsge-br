import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
TARGETS = ROOT / "docs" / "05_replication_targets.md"
BLOCKERS = ROOT / "docs" / "wbs063_blockers.md"
WRAPPER_FILE = ROOT / "src" / "diagnostics" / "run_dynare.py"
FORBIDDEN_GENERATED_PATHS = {
    ROOT / "outputs" / "irfs",
    ROOT / "outputs" / "posterior",
    ROOT / "outputs" / "identification",
    ROOT / "outputs" / "backtesting",
    ROOT / "model" / "samba_classic" / "priors.inc",
}


def _load_dynare_wrapper():
    spec = importlib.util.spec_from_file_location("run_dynare", WRAPPER_FILE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _execution_status() -> str:
    return next(
        line for line in STATUS.read_text(encoding="utf-8").splitlines()
        if line.startswith("Execution status:")
    )


def test_wbs063_cannot_complete_without_approved_irf_targets():
    targets = TARGETS.read_text(encoding="utf-8")
    status = _execution_status()

    if "targets_approved: false" in targets:
        assert "WBS-063_COMPLETED" not in status
        assert "BLOCKED_WBS063_IRF_TARGETS" in status
        assert BLOCKERS.exists()
        blockers = BLOCKERS.read_text(encoding="utf-8")
        assert "approved IRF targets: 0" in blockers
        assert "required approved IRF targets: 5" in blockers


def test_wbs063_irf_smoke_runs_in_temp_without_committed_outputs_when_blocked():
    if "BLOCKED_WBS063_IRF_TARGETS" not in _execution_status():
        return
    if shutil.which("dynare") is None:
        pytest.skip("Dynare is unavailable on PATH.")

    wrapper = _load_dynare_wrapper()
    assert wrapper.IRF_HORIZON == 20

    completed = subprocess.run(
        [sys.executable, str(WRAPPER_FILE), "--mode", "irfs"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=240,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    summary = json.loads(completed.stdout)
    assert summary["status"] == "passed"
    assert summary["mode"] == "irfs"
    assert summary["irf_horizon"] == 20
    assert summary["irf_restrictions_evaluated"] is False
    assert summary["persistent_outputs_created"] is False
    assert all(not path.exists() for path in FORBIDDEN_GENERATED_PATHS)
