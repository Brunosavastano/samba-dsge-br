from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
STRATEGY = ROOT / "docs" / "04_estimation_strategy.md"


def _execution_status() -> str:
    return next(
        line for line in STATUS.read_text(encoding="utf-8").splitlines()
        if line.startswith("Execution status:")
    )


def test_wbs065_identification_protocol_exists_without_running_identification():
    assert STRATEGY.exists()
    text = STRATEGY.read_text(encoding="utf-8")

    assert "status: wbs066_identification_completed" in text
    assert "wbs: WBS-066" in text
    assert "identification_run_created: true" in text
    assert "identification_outputs_created: true" in text
    assert "priors_created: false" in text
    assert "estimation_started: false" in text
    assert "posterior_created: false" in text
    assert "Iskrev/Dynare identification gate" in text
    assert "WBS-066" in text


def test_wbs065_protocol_does_not_create_future_phase_artifacts():
    execution_status = _execution_status()
    diagnostics = ROOT / "outputs" / "identification" / "wbs066_identification_diagnostics.md"

    if (
        "WBS-066_COMPLETED" not in execution_status
        and "BLOCKED_WBS066_IDENTIFICATION_SOLVE" not in execution_status
    ):
        assert not (ROOT / "outputs" / "identification").exists()
    if (
        "BLOCKED_WBS066_IDENTIFICATION_SOLVE" in execution_status
        or "WBS-066_COMPLETED" in execution_status
    ):
        assert diagnostics.exists()
        text = diagnostics.read_text(encoding="utf-8")
        assert "WBS-066_COMPLETED" in text
        assert "diffuse_filter" in text
        assert "rank of Tau" in text
        assert "not identified" in text
        assert "order and rank conditions are verified" in text
        assert "no priors" in text
        assert "no posterior outputs" in text
    assert not (ROOT / "model" / "samba_classic" / "priors.inc").exists()
    assert not (ROOT / "outputs" / "posterior").exists()
    assert not (ROOT / "outputs" / "backtesting").exists()
    assert not (ROOT / "model" / "samba_redux").exists()
    assert not (ROOT / "model" / "sovereign_extension").exists()


def test_wbs065_protocol_defines_parameter_classification_without_priors():
    text = STRATEGY.read_text(encoding="utf-8")

    required_statuses = [
        "locally_identified",
        "weak_or_collinear",
        "fixed_at_sourced_calibration",
        "requires_prior_after_wbs068",
        "requires_restriction_or_reparameterization",
        "requires_human_review",
    ]
    for status in required_statuses:
        assert status in text
    assert "must not invent parameters" in text
    assert "must not invent parameters,\npriors" in text
