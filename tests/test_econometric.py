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
WBS071A_SMOKE_ARTIFACT = ROOT / "outputs" / "posterior" / "smoke" / "wbs071a_estimation_smoke.json"
WBS072_CONFIG = ROOT / "docs" / "wbs072_mh_pilot_config.md"
WBS072_PILOT_SUMMARY = ROOT / "outputs" / "posterior" / "pilot" / "wbs072_mh_pilot_summary.json"
WBS072_PILOT_DIAGNOSTICS = ROOT / "outputs" / "posterior" / "pilot" / "wbs072_mh_pilot_diagnostics.md"
WBS073_CONFIG = ROOT / "docs" / "wbs073_full_mh_config.md"
WBS073_FULL_SUMMARY = ROOT / "outputs" / "posterior" / "full" / "wbs073_full_mh_summary.json"
WBS073_FULL_DIAGNOSTICS = ROOT / "outputs" / "posterior" / "full" / "wbs073_full_mh_diagnostics.md"
WBS073_FULL_MANIFEST = ROOT / "outputs" / "posterior" / "full" / "wbs073_full_mh_manifest.json"
FORBIDDEN_PERSISTENT_OUTPUTS = (
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


def _forbidden_persistent_outputs() -> tuple[Path, ...]:
    paths = list(FORBIDDEN_PERSISTENT_OUTPUTS)
    if "WBS-073_COMPLETED" in _execution_status() or "BLOCKED_WBS073" in _execution_status():
        pass
    elif "WBS-072_COMPLETED" in _execution_status():
        paths.append(ROOT / "outputs" / "posterior" / "full")
    elif "WBS-071a_COMPLETED" in _execution_status():
        paths.extend(
            [
                ROOT / "outputs" / "posterior" / "pilot",
                ROOT / "outputs" / "posterior" / "full",
            ]
        )
    else:
        paths.append(ROOT / "outputs" / "posterior")
    return tuple(paths)


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
    assert all(not path.exists() for path in _forbidden_persistent_outputs())


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
    assert all(not path.exists() for path in _forbidden_persistent_outputs())


def test_wbs071_completed_posterior_mode_records_temp_run_without_future_outputs():
    if "WBS-071_COMPLETED" not in _execution_status():
        return

    result = ROOT / "docs" / "wbs071_posterior_mode.md"
    blocker = ROOT / "docs" / "wbs071_blockers.md"
    assert result.exists()
    result_text = result.read_text(encoding="utf-8")
    blocker_text = blocker.read_text(encoding="utf-8")

    assert "Status: `WBS-071_COMPLETED`" in result_text
    assert "mh_replic=0" in result_text
    assert "mode_compute=4" in result_text
    assert "-456.997406" in result_text
    assert "No MH chain" in result_text
    assert "RESOLVED_WBS071_POSTERIOR_MODE_COMPLETED" in blocker_text
    assert all(not path.exists() for path in _forbidden_persistent_outputs())


def test_wbs071a_estimation_smoke_records_minimal_artifact_without_mh_outputs():
    if "WBS-071a_COMPLETED" not in _execution_status():
        return

    result = ROOT / "docs" / "wbs071a_estimation_smoke.md"
    assert result.exists()
    assert WBS071A_SMOKE_ARTIFACT.exists()

    result_text = result.read_text(encoding="utf-8")
    summary = json.loads(WBS071A_SMOKE_ARTIFACT.read_text(encoding="utf-8"))

    assert "Status: `WBS-071a_COMPLETED`" in result_text
    assert summary["mode"] == "estimation-smoke"
    assert summary["status"] == "passed"
    assert summary["mh_replic"] == 0
    assert summary["mode_compute"] == 0
    assert summary["finite_likelihood_reported"] is True
    assert summary["likelihood_nonfinite_value_count"] == 0
    assert summary["posterior_mode"] is False
    assert summary["persistent_outputs_created"] is False
    assert all(not path.exists() for path in _forbidden_persistent_outputs())


def test_wbs072_mh_pilot_config_is_proposal_only_without_chains():
    if "WBS-072_CONFIG_PROPOSED" not in _execution_status():
        return

    assert WBS072_CONFIG.exists()
    text = WBS072_CONFIG.read_text(encoding="utf-8")

    assert "approval_status: proposed" in text
    assert "do_not_run_until_approved: true" in text
    assert "`mh_replic`: 2000 per chain" in text
    assert "chains: 2 independent pilot chains" in text
    assert "target acceptance band: 0.20 to 0.35" in text
    assert "R-hat scope:" in text
    assert "outputs/posterior/pilot/" in text
    assert "outputs/posterior/full/" in text
    assert all(not path.exists() for path in _forbidden_persistent_outputs())


def test_wbs072_mh_pilot_approved_config_records_amendment():
    if "WBS-072_CONFIG_APPROVED" not in _execution_status() and "WBS-072_COMPLETED" not in _execution_status():
        return

    assert WBS072_CONFIG.exists()
    text = WBS072_CONFIG.read_text(encoding="utf-8")

    assert "approval_status: approved" in text
    assert "approved_by: Bruno" in text
    assert "approval_date: 2026-05-30" in text
    assert "amendment: R-hat unavailable is warning, not blocker." in text
    assert "`mh_replic`: 2000 per chain" in text
    assert "chains: 2 independent pilot chains" in text
    assert "target acceptance band: 0.20 to 0.35" in text
    assert "not final convergence evidence" in text
    assert "outputs/posterior/full/" in text


def test_wbs072_completed_mh_pilot_records_only_pilot_artifacts():
    if "WBS-072_COMPLETED" not in _execution_status():
        return

    assert WBS072_PILOT_SUMMARY.exists()
    assert WBS072_PILOT_DIAGNOSTICS.exists()
    summary = json.loads(WBS072_PILOT_SUMMARY.read_text(encoding="utf-8"))
    diagnostics = WBS072_PILOT_DIAGNOSTICS.read_text(encoding="utf-8")

    assert summary["wbs"] == "WBS-072"
    assert summary["mode"] == "mh-pilot"
    assert summary["status"] == "passed"
    assert summary["mh_replic"] == 2000
    assert summary["chains"] == 2
    assert summary["mh_nblocks"] == 2
    assert summary["mh_drop"] == 0.5
    assert 0.20 <= summary["mh_acceptance_ratio"] <= 0.35
    assert summary["mh_acceptance_in_target_band"] is True
    assert summary["mh_nonfinite_token_count"] == 0
    assert summary["rhat_status"] in {"computed", "unavailable_warning", "above_threshold_warning"}
    assert summary["full_mh_created"] is False
    assert summary["posterior_inference_claimed"] is False
    assert "not final convergence evidence" in diagnostics
    assert all(not path.exists() for path in _forbidden_persistent_outputs())


def test_wbs073_full_mh_config_records_approval_only_for_wbs073():
    if (
        "WBS-073_APPROVED_FOR_FULL_MH" not in _execution_status()
        and "WBS-073_COMPLETED" not in _execution_status()
        and "BLOCKED_WBS073" not in _execution_status()
    ):
        return

    assert WBS073_CONFIG.exists()
    text = WBS073_CONFIG.read_text(encoding="utf-8")

    assert "approval_status: approved" in text
    assert "approved_by: Bruno" in text
    assert "approval_date: 2026-05-30" in text
    assert "approved_timeout_seconds: 43200" in text
    assert "`mh_replic`: 20000 per chain" in text
    assert "chains: 4 full-MH chains" in text
    assert "`mh_jscale`: 0.337313" in text
    assert "final publication-grade posterior inference claims" in text


def test_wbs073_completed_full_mh_records_only_lightweight_artifacts():
    if "WBS-073_COMPLETED" not in _execution_status():
        return

    assert WBS073_FULL_SUMMARY.exists()
    assert WBS073_FULL_DIAGNOSTICS.exists()
    assert WBS073_FULL_MANIFEST.exists()
    summary = json.loads(WBS073_FULL_SUMMARY.read_text(encoding="utf-8"))
    manifest = json.loads(WBS073_FULL_MANIFEST.read_text(encoding="utf-8"))
    diagnostics = WBS073_FULL_DIAGNOSTICS.read_text(encoding="utf-8")

    assert summary["wbs"] == "WBS-073"
    assert summary["mode"] == "full-mh"
    assert summary["status"] == "passed"
    assert summary["mh_replic"] == 20000
    assert summary["chains"] == 4
    assert summary["mh_nblocks"] == 4
    assert summary["approved_blocks"] == 2
    assert summary["mh_drop"] == 0.5
    assert summary["mh_jscale"] == 0.337313
    assert 0.20 <= summary["mh_acceptance_ratio"] <= 0.35
    assert summary["rhat_status"] == "computed"
    assert summary["rhat_value"] <= 1.1
    assert summary["posterior_inference_claimed"] is False
    assert summary["publication_grade_posterior_evidence"] is False
    assert manifest["raw_heavy_chain_artifacts_committed"] is False
    assert "not final publication-grade posterior evidence" in diagnostics
    assert all(not path.exists() for path in _forbidden_persistent_outputs())
