import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
PRIORS_FILE = ROOT / "model" / "samba_classic" / "priors.inc"
WRAPPER_FILE = ROOT / "src" / "diagnostics" / "run_dynare.py"
FORBIDDEN_PERSISTENT_OUTPUTS = (
    ROOT / "outputs" / "posterior",
    ROOT / "outputs" / "backtesting",
    ROOT / "model" / "samba_redux",
    ROOT / "model" / "sovereign_extension",
)


def _execution_status() -> str:
    return next(
        line
        for line in STATUS.read_text(encoding="utf-8").splitlines()
        if line.startswith("Execution status:")
    )


def test_wbs070_finite_likelihood_runs_in_temp_without_future_outputs():
    if "WBS-070_COMPLETED" not in _execution_status():
        return
    if shutil.which("dynare") is None:
        pytest.skip("Dynare is unavailable on PATH.")

    assert PRIORS_FILE.exists()
    completed = subprocess.run(
        [sys.executable, str(WRAPPER_FILE), "--mode", "likelihood-smoke", "--timeout-seconds", "240"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    summary = json.loads(completed.stdout)
    assert summary["status"] == "passed"
    assert summary["mode"] == "likelihood-smoke"
    assert summary["working_directory"] == "temporary"
    assert summary["likelihood_observation_count"] == 67
    assert summary["likelihood_observable_columns"] == ["y", "c", "i", "g", "q", "r_t"]
    assert summary["likelihood_data_transformations"]["y_c_i_g"] == "first log-difference, demeaned"
    assert summary["likelihood_measurement_errors"]["y"]["stderr"] == 0.08
    assert summary["likelihood_measurement_errors"]["y"]["source"] == "BCB_WP239"
    assert summary["finite_likelihood_reported"] is True
    assert summary["likelihood_nonfinite_value_count"] == 0
    assert all(not path.exists() for path in FORBIDDEN_PERSISTENT_OUTPUTS)


def test_wbs071_blocked_posterior_mode_does_not_create_future_outputs():
    status = _execution_status()
    if "BLOCKED_WBS071_POSTERIOR_MODE_TIMEOUT" not in status:
        return

    blocker = ROOT / "docs" / "wbs071_blockers.md"
    assert blocker.exists()
    text = blocker.read_text(encoding="utf-8")
    assert "mode_compute=4" in text
    assert "mh_replic=0" in text
    assert "did not report a completed posterior mode" in text
    assert all(not path.exists() for path in FORBIDDEN_PERSISTENT_OUTPUTS)
