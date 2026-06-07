import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
TARGETS = ROOT / "docs" / "05_replication_targets.md"
VALIDATION = ROOT / "docs" / "06_model_validation.md"
WBS064_REPORT = ROOT / "docs" / "wbs064_mvp_calibrated_report.md"
USER_REPORT = ROOT / "outputs" / "reports" / "mvp_calibrated_report.md"


def _allowed_executable_model_files() -> set[str]:
    text = PROJECT_STATUS.read_text(encoding="utf-8")
    allowed = {
        "model/samba_classic/calibration.m",
        "model/samba_classic/steady_state.m",
    }
    if re.search(r"Execution status: WBS-057_COMPLETE", text):
        allowed.add("model/samba_classic/samba_classic.mod")
    if re.search(r"Execution status: .*WBS-058_COMPLETED", text):
        allowed.add("model/samba_classic/shocks.inc")
    if re.search(r"Execution status: .*WBS-059_COMPLETED", text):
        allowed.add("model/samba_classic/observables.inc")
    if re.search(r"Execution status: .*WBS-069_COMPLETED", text):
        allowed.add("model/samba_classic/priors.inc")
    return allowed


def test_replication_targets_template_has_required_irf_fields():
    text = TARGETS.read_text(encoding="utf-8")

    assert "status: template" in text
    assert "do_not_treat_as_validation_result: true" in text
    assert "data_created: false" in text
    assert "results_created: false" in text
    assert "expected_sign" in text
    assert "timing_window" in text
    assert "magnitude_band" in text
    assert "benchmark_source" in text
    assert "targets_approved: false" in text
    assert "earliest_target_fill_wbs: WBS-074" in text


def test_model_validation_records_gate3_without_claiming_full_validation():
    text = VALIDATION.read_text(encoding="utf-8")

    assert text.startswith("---\nstatus: gate3_calibrated_mvp_validation\n")
    assert "do_not_treat_as_full_validation_result: true" in text
    assert "posterior_created: false" in text
    assert "backtesting_created: false" in text
    assert "Dynare smoke/parse: passed." in text
    assert "Steady-state residuals: passed" in text
    assert "BK check: passed" in text
    assert "IRF restrictions: passed" in text
    assert "not a final empirical validation result" in text


def test_validation_templates_do_not_create_forbidden_implementation_files():
    model_dir = ROOT / "model"
    executable_model_files = []
    if model_dir.exists():
        executable_model_files = [
            path.relative_to(ROOT).as_posix()
            for path in model_dir.rglob("*")
            if (
                path.is_file()
                and path.suffix in {".mod", ".m", ".inc"}
                and path.relative_to(ROOT).as_posix() not in _allowed_executable_model_files()
            )
        ]

    assert executable_model_files == []
    assert not (ROOT / "src" / "data_pipeline").exists()


def test_wbs064_reports_exist_and_do_not_claim_future_phase_completion():
    for report in (WBS064_REPORT, USER_REPORT):
        assert report.exists()
        text = report.read_text(encoding="utf-8")
        assert "Residuals" in text or "residuals" in text
        assert "BK" in text
        assert "IRF" in text
        assert "0 failed" in text
        forbidden_claims = [
            "Bayesian estimation complete",
            "posterior complete",
            "backtesting complete",
            "Redux complete",
            "sovereign extension complete",
            "Gate 6 completed",
        ]
        for claim in forbidden_claims:
            assert claim not in text
