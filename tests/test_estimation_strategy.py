import csv
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
STRATEGY = ROOT / "docs" / "04_estimation_strategy.md"
PRIORS_FILE = ROOT / "model" / "samba_classic" / "priors.inc"


def _execution_status() -> str:
    return next(
        line for line in STATUS.read_text(encoding="utf-8").splitlines()
        if line.startswith("Execution status:")
    )


def test_wbs065_identification_protocol_exists_without_running_identification():
    assert STRATEGY.exists()
    text = STRATEGY.read_text(encoding="utf-8")

    assert "status: wbs069_priors_inc_completed" in text
    assert "wbs: WBS-069" in text
    assert "priors_table_created: true" in text
    assert "identification_run_created: true" in text
    assert "identification_outputs_created: true" in text
    assert "priors_created: true" in text
    assert "estimation_started: false" in text
    assert "posterior_created: false" in text
    assert "Iskrev/Dynare identification gate" in text
    assert "WBS-066" in text
    assert "WBS-067 Parameter Treatment Decisions" in text
    assert "WBS-068 Source-Backed Priors Table" in text


def _wbs067_rows() -> list[dict[str, str]]:
    text = STRATEGY.read_text(encoding="utf-8")
    start = text.index("## WBS-067 Parameter Treatment Decisions")
    fenced = text.index("```csv", start)
    body_start = text.index("\n", fenced) + 1
    body_end = text.index("```", body_start)
    return list(csv.DictReader(StringIO(text[body_start:body_end])))


def _wbs068_prior_rows() -> list[dict[str, str]]:
    text = STRATEGY.read_text(encoding="utf-8")
    start = text.index("## WBS-068 Source-Backed Priors Table")
    fenced = text.index("```csv", start)
    body_start = text.index("\n", fenced) + 1
    body_end = text.index("```", body_start)
    return list(csv.DictReader(StringIO(text[body_start:body_end])))


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
    if "WBS-069_COMPLETED" in execution_status:
        assert PRIORS_FILE.exists()
    else:
        assert not PRIORS_FILE.exists()
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


def test_wbs067_classifies_every_nonidentified_entry_without_priors():
    execution_status = _execution_status()
    if "WBS-067_COMPLETED" not in execution_status:
        return

    rows = _wbs067_rows()
    decisions = {row["wbs067_decision"] for row in rows}
    entries = {row["diagnostic_entry"] for row in rows}

    assert len(rows) == 25
    assert decisions <= {
        "fixed_at_sourced_calibration",
        "requires_restriction_or_reparameterization",
        "not_required_for_mvp",
    }
    assert "requires_human_review" not in decisions
    assert {
        "phi_pi",
        "phi_y",
        "psi_nfa",
        "external_debt_lom_adjustment",
        "pi_target_gross_ss",
        "lambda_g",
        "lambda_i",
        "lambda_f",
    } <= entries
    assert {
        row["diagnostic_entry"]
        for row in rows
        if row["entry_type"] == "shock_stderr"
    } == {
        "SE_pi_target",
        "SE_y_gap",
        "SE_q_f",
        "SE_q_g",
        "SE_q_i",
        "SE_q_m",
        "SE_q_x_star",
        "SE_q_d",
        "SE_y_d",
        "SE_r_k",
        "SE_mc",
        "SE_mc_x",
        "SE_m_c",
        "SE_m_i",
        "SE_m_x",
        "SE_m",
        "SE_x",
    }
    if "WBS-069_COMPLETED" not in execution_status:
        assert "priors_created: false" in STRATEGY.read_text(encoding="utf-8")
        assert not PRIORS_FILE.exists()


def test_wbs068_priors_table_is_sourced_and_priors_inc_is_phase_gated():
    execution_status = _execution_status()
    if "WBS-068_COMPLETED" not in execution_status:
        return

    rows = _wbs068_prior_rows()
    excluded_by_wbs067 = {
        "phi_pi",
        "phi_y",
        "psi_nfa",
        "external_debt_lom_adjustment",
        "pi_target_gross_ss",
        "lambda_g",
        "lambda_i",
        "lambda_f",
        "stderr_pi_target",
        "stderr_y_gap",
    }

    assert len(rows) == 28
    assert {row["eligible_for_wbs069_priors_inc"] for row in rows} == {"true"}
    assert {row["source"] for row in rows} == {"BCB_WP239"}
    assert all(row["prior_distribution"] for row in rows)
    assert all(row["prior_mean"] for row in rows)
    assert all(row["prior_sd"] for row in rows)
    assert all(row["source_location"] for row in rows)
    assert all(row["rationale"] for row in rows)
    assert excluded_by_wbs067.isdisjoint({row["canonical_name"] for row in rows})
    if "WBS-069_COMPLETED" in execution_status:
        assert "priors_created: true" in STRATEGY.read_text(encoding="utf-8")
        assert PRIORS_FILE.exists()
    else:
        assert "priors_created: false" in STRATEGY.read_text(encoding="utf-8")
        assert not PRIORS_FILE.exists()
    assert not (ROOT / "outputs" / "posterior").exists()


def test_wbs069_priors_inc_translates_only_wbs068_eligible_rows():
    if "WBS-069_COMPLETED" not in _execution_status():
        return

    rows = _wbs068_prior_rows()
    text = PRIORS_FILE.read_text(encoding="utf-8")
    model_params = {
        row["canonical_name"]
        for row in rows
        if row["scope"] == "model_parameter"
    }
    shock_names = {
        row["canonical_name"].removeprefix("stderr_")
        for row in rows
        if row["scope"] == "shock_stderr"
    }
    excluded = {
        "phi_pi",
        "phi_y",
        "psi_nfa",
        "external_debt_lom_adjustment",
        "pi_target_gross_ss",
        "lambda_g",
        "lambda_i",
        "lambda_f",
        "stderr pi_target",
        "stderr y_gap",
    }

    assert "estimated_params;" in text
    assert "end;" in text
    assert text.count("_pdf") == len(rows)
    assert "estimation(" not in text
    assert "mh_replic" not in text
    assert "posterior" not in text
    assert "datafile" not in text
    for parameter in model_params:
        assert f"  {parameter}, " in text
    for shock in shock_names:
        assert f"  stderr {shock}, " in text
    for name in excluded:
        assert name not in text
