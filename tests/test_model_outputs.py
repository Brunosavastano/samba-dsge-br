import csv
import importlib.util
import json
import shutil
import subprocess
import sys
from io import StringIO
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
SOURCING = ROOT / "docs" / "wbs057_equation_sourcing.md"
BLOCKERS = ROOT / "docs" / "wbs057_blockers.md"
MODEL_FILE = ROOT / "model" / "samba_classic" / "samba_classic.mod"
SHOCKS_FILE = ROOT / "model" / "samba_classic" / "shocks.inc"
OBSERVABLES_FILE = ROOT / "model" / "samba_classic" / "observables.inc"
WRAPPER_FILE = ROOT / "src" / "diagnostics" / "run_dynare.py"
FORBIDDEN_WBS057_FILES = {
    ROOT / "model" / "samba_classic" / "priors.inc",
}
FORBIDDEN_GENERATED_PATHS = {
    ROOT / "model" / "samba_classic" / "samba_classic.log",
    ROOT / "model" / "samba_classic" / "samba_classic",
    ROOT / "model" / "samba_classic" / "+samba_classic",
}


def _project_status_text() -> str:
    return STATUS.read_text(encoding="utf-8")


def _wbs057_rows() -> list[dict[str, str]]:
    lines = SOURCING.read_text(encoding="utf-8").splitlines()
    table_start = next(
        idx for idx, line in enumerate(lines)
        if line.startswith("| equation_id |")
    )
    table_lines = []
    for line in lines[table_start:]:
        if not line.startswith("|"):
            break
        table_lines.append(line)

    header = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows.append(dict(zip(header, cells)))
    return rows


def _wbs057_formula_rows() -> list[dict[str, str]]:
    text = SOURCING.read_text(encoding="utf-8")
    start = text.index("## WBS-057b exact formula transcription")
    fenced = text.index("```csv", start)
    body_start = text.index("\n", fenced) + 1
    body_end = text.index("```", body_start)
    return list(csv.DictReader(StringIO(text[body_start:body_end])))


def _wbs057_symbol_rows() -> list[dict[str, str]]:
    text = SOURCING.read_text(encoding="utf-8")
    start = text.index("## WBS-057b Dynare symbol mapping")
    fenced = text.index("```csv", start)
    body_start = text.index("\n", fenced) + 1
    body_end = text.index("```", body_start)
    return list(csv.DictReader(StringIO(text[body_start:body_end])))


def _execution_status() -> str:
    return next(
        line for line in _project_status_text().splitlines()
        if line.startswith("Execution status:")
    )


def _load_dynare_wrapper():
    spec = importlib.util.spec_from_file_location("run_dynare", WRAPPER_FILE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_wbs057_source_mapping_or_transcription_status_blocks_mod_file():
    rows = _wbs057_rows()
    blocking = [
        row["equation_id"]
        for row in rows
        if row["wbs057_blocking"] == "true"
    ]
    blockers = BLOCKERS.read_text(encoding="utf-8")
    status = _project_status_text()
    execution_status = next(
        line for line in status.splitlines()
        if line.startswith("Execution status:")
    )

    assert len(blocking) == 0
    assert (
        "WBS-057_COMPLETED" in execution_status
        or "WBS-057_READY_FOR_MOD" in execution_status
        or "BLOCKED_WBS057_SYMBOL_MAPPING" in execution_status
    )
    assert (
        "Remaining true WBS-057 blockers: 0" in blockers
        or "Remaining true WBS-057 source blockers: 0" in SOURCING.read_text(encoding="utf-8")
    )
    assert "Dynare-ready rows by source/formula status: 24" in SOURCING.read_text(encoding="utf-8")
    assert "Remaining executable formula-text blockers: 0" in SOURCING.read_text(encoding="utf-8")
    if "BLOCKED_WBS057_SYMBOL_MAPPING" in execution_status:
        assert "Remaining WBS-057 symbol blockers: 2" in blockers
    if "WBS-057_READY_FOR_MOD" in execution_status:
        assert "Remaining WBS-057 symbol blockers: 0" in blockers
        assert not MODEL_FILE.exists()
    if "WBS-057_COMPLETED" in execution_status:
        assert MODEL_FILE.exists()
        assert "Dynare parse: passed" in blockers
    assert all(not path.exists() for path in FORBIDDEN_WBS057_FILES)
    if "WBS-058_COMPLETED" not in execution_status:
        assert not SHOCKS_FILE.exists()
    if "WBS-059_COMPLETED" not in execution_status:
        assert not OBSERVABLES_FILE.exists()


def test_wbs057_mod_shell_uses_sourced_inputs_without_future_artifacts():
    status = _project_status_text()
    execution_status = next(
        line for line in status.splitlines()
        if line.startswith("Execution status:")
    )
    if "WBS-057_COMPLETED" not in execution_status:
        return

    text = MODEL_FILE.read_text(encoding="utf-8")
    required_markers = [
        "docs/wbs057_equation_sourcing.md",
        '@#include "calibration.m"',
        "model(linear);",
        "EQ-MON-001",
        "EQ-EXT-003",
        "EQ-FISC-003",
        "EQ-PRICE-001",
        "EQ-HH-001",
        "EQ-FIRM-002",
        "EQ-AGG-003",
    ]
    forbidden_markers = [
        "estimation",
        "stoch_simul",
        '@#include "priors.inc"',
    ]
    if "WBS-058_COMPLETED" not in execution_status:
        forbidden_markers.extend(["shocks;", '@#include "shocks.inc"'])
    if "WBS-059_COMPLETED" not in execution_status:
        forbidden_markers.extend(["varobs", '@#include "observables.inc"'])

    for marker in required_markers:
        assert marker in text
    for marker in forbidden_markers:
        assert marker not in text


def test_wbs058_shocks_include_uses_wp239_stderr_values_only_after_wbs058():
    status = _project_status_text()
    execution_status = next(
        line for line in status.splitlines()
        if line.startswith("Execution status:")
    )
    if "WBS-058_COMPLETED" not in execution_status:
        return

    assert SHOCKS_FILE.exists()
    text = SHOCKS_FILE.read_text(encoding="utf-8")
    model_text = MODEL_FILE.read_text(encoding="utf-8")
    expected = {
        "risk_dom": "0.57",
        "z_i": "3.54",
        "z_c": "8.80",
        "eps_admin": "1.40",
        "z_p": "0.79",
        "pi": "0.14",
        "z_w": "1.38",
        "z_z": "0.17",
        "z_q": "0.80",
        "eps_risk": "0.38",
        "z_g": "1.73",
        "eps_tax": "0.48",
        "eps_sp_target": "0.29",
        "eps_monetary": "0.32",
        "z_px": "3.89",
        "pi_star": "0.85",
        "r_star": "0.19",
        "q_m_star": "1.85",
    }

    assert "WP239 Table 3, p. 98" in text
    assert "shocks;" in text
    assert '@#include "shocks.inc"' in model_text
    assert "varobs" not in text
    assert "estimation" not in text
    assert "stoch_simul" not in text
    for shock, stderr in expected.items():
        assert f"var {shock};" in text
        assert f"stderr {stderr};" in text


def test_wbs059_observables_include_uses_wp239_aligned_varobs_only_after_wbs059():
    status = _project_status_text()
    execution_status = next(
        line for line in status.splitlines()
        if line.startswith("Execution status:")
    )
    if "WBS-059_COMPLETED" not in execution_status:
        return

    assert OBSERVABLES_FILE.exists()
    text = OBSERVABLES_FILE.read_text(encoding="utf-8")
    model_text = MODEL_FILE.read_text(encoding="utf-8")

    assert "WP239 Section 3.1" in text
    assert "varobs y c i g q r_t;" in text
    assert '@#include "observables.inc"' in model_text
    assert "estimation" not in text
    assert "stoch_simul" not in text
    assert "measurement_errors" not in text


def test_wbs060_dynare_wrapper_exists_and_constructs_smoke_command_after_wbs060():
    if "WBS-060_COMPLETED" not in _execution_status():
        return

    assert WRAPPER_FILE.exists()
    wrapper = _load_dynare_wrapper()

    assert wrapper.build_dynare_command("dynare") == [
        "dynare",
        "samba_classic.mod",
        "noclearall",
        "nolog",
    ]
    residual_summary = wrapper._parse_residuals(
        "Equation number  1: EQ-TEST :       0.000000\n"
    )
    assert residual_summary == {
        "residual_equation_count": 1,
        "nonfinite_residual_count": 0,
        "max_abs_residual": 0.0,
    }
    bk_summary = wrapper._parse_bk(
        "There are 26 eigenvalue(s) larger than 1 in modulus for 28 forward-looking variable(s).\n"
        "The order condition is NOT verified.\n"
    )
    assert bk_summary["eigenvalues_larger_than_one"] == 26
    assert bk_summary["forward_looking_variables"] == 28
    assert bk_summary["bk_order_condition_not_verified"] is True
    assert bk_summary["bk_order_condition_verified"] is False
    passed_bk_summary = wrapper._parse_bk(
        "There are 26 eigenvalue(s) larger than 1 in modulus for 26 forward-looking variable(s).\n"
        "The order and rank conditions are verified.\n"
    )
    assert passed_bk_summary["eigenvalues_larger_than_one"] == 26
    assert passed_bk_summary["forward_looking_variables"] == 26
    assert passed_bk_summary["bk_order_condition_verified"] is True
    assert passed_bk_summary["bk_rank_condition_verified"] is True
    assert set(wrapper.REQUIRED_MODEL_FILES) == {
        "samba_classic.mod",
        "calibration.m",
        "steady_state.m",
        "shocks.inc",
        "observables.inc",
    }


def test_wbs060_dynare_wrapper_smoke_runs_in_temp_without_repo_outputs_after_wbs060():
    if "WBS-060_COMPLETED" not in _execution_status():
        return
    if shutil.which("dynare") is None:
        pytest.skip("Dynare is unavailable on PATH.")

    completed = subprocess.run(
        [sys.executable, str(WRAPPER_FILE), "--mode", "smoke"],
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
    assert summary["working_directory"] == "temporary"
    assert summary["returncode"] == 0
    assert all(not path.exists() for path in FORBIDDEN_GENERATED_PATHS)


def test_wbs062_bk_wrapper_passes_only_after_wbs062_completed():
    execution_status = _execution_status()
    if "WBS-062_COMPLETED" not in execution_status:
        return
    if shutil.which("dynare") is None:
        pytest.skip("Dynare is unavailable on PATH.")

    mod_text = MODEL_FILE.read_text(encoding="utf-8")
    assert "predetermined_variables nfa k;" in mod_text

    completed = subprocess.run(
        [sys.executable, str(WRAPPER_FILE), "--mode", "bk"],
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
    assert summary["bk_order_condition_verified"] is True
    assert summary["bk_rank_condition_verified"] is True
    assert all(not path.exists() for path in FORBIDDEN_GENERATED_PATHS)


def test_wbs057b_formula_text_is_transcribed_for_dynare_ready_rows():
    ready_ids = {
        row["equation_id"]
        for row in _wbs057_rows()
        if row["dynare_ready"] == "true"
    }
    formula_rows = _wbs057_formula_rows()
    formula_by_id = {row["equation_id"]: row for row in formula_rows}

    assert set(formula_by_id) == ready_ids
    assert len(formula_rows) == 24

    for row in formula_rows:
        assert row["formula_text_status"] == "transcribed"
        assert row["exact_formula_text"].startswith("C.")
        assert row["source"] != ""
        assert row["source_location"] != ""
        assert row["registry_mapping"] != ""
        assert row["dynare_ready"] == "true"


def test_wbs057b_symbol_mapping_records_unresolved_symbols():
    rows = _wbs057_symbol_rows()
    allowed_statuses = {
        "mapped_to_registry",
        "mapped_to_calibration",
        "mapped_to_steady_state",
        "alias_resolved",
        "not_required_for_wbs057",
        "deferred_to_wbs058_shocks",
        "missing_canonical_name",
        "missing_sourced_value",
        "ambiguous_symbol",
    }
    unresolved_statuses = {
        "missing_canonical_name",
        "missing_sourced_value",
        "ambiguous_symbol",
    }
    mapped_statuses = allowed_statuses - unresolved_statuses
    unresolved = [
        row for row in rows
        if row["mapping_status"] in unresolved_statuses
    ]

    assert len(rows) == 33
    deferred = [
        row for row in rows
        if row["mapping_status"] == "deferred_to_wbs058_shocks"
    ]

    assert len(unresolved) == 0
    assert len(deferred) == 7
    for row in rows:
        assert row["wp239_symbol"] != ""
        assert row["economic_meaning"] != ""
        assert row["type"] in {
            "endogenous",
            "endogenous/shock_state",
            "parameter",
            "shock",
            "shock_state",
            "steady_state_assignment",
            "alias",
            "template_alias_expanded",
            "endogenous_aux",
        }
        assert row["source_location"] != ""
        assert row["used_in_equation_ids"] != ""
        assert row["mapping_status"] in allowed_statuses
        if row["mapping_status"] in mapped_statuses:
            assert row["canonical_project_name"] != ""
            assert row["dynare_name"] != ""
    by_symbol = {row["wp239_symbol"]: row for row in rows}
    assert by_symbol["theta_A"]["mapping_status"] == "mapped_to_calibration"
    assert by_symbol["chi_A"]["mapping_status"] == "mapped_to_calibration"


def test_wbs057_sourcing_uses_required_columns_and_boolean_flags():
    required_columns = {
        "equation_id",
        "block",
        "project_equation_name",
        "wp239_reference",
        "exact_formula_available",
        "source",
        "source_location",
        "registry_mapping",
        "wbs057a_category",
        "wbs057_resolution",
        "wbs057_blocking",
        "deferred_to_wbs058",
        "deferred_to_wbs059",
        "dynare_ready",
        "notes",
    }
    valid_categories = {
        "ready_not_reclassified",
        "true_missing_wp239_formula",
        "formula_available_but_mapping_missing",
        "registry_overreach_not_required_for_mvp",
        "belongs_to_wbs058_shocks",
        "belongs_to_wbs059_observables",
        "calibration_or_steady_state_dependency",
        "notation_alias_or_duplicate",
        "test_contract_issue",
        "reference_extraction_issue",
    }
    valid_resolutions = {
        "not_applicable",
        "resolved_exact_formula_mapped",
        "resolved_parameter_weight_mapped",
        "resolved_by_registry_mapping",
        "resolved_by_calibration_mapping",
        "not_required_for_wbs057",
        "needs_human_formula_review",
        "deferred_to_wbs059_observables",
        "still_missing_in_sources",
    }

    for row in _wbs057_rows():
        assert set(row) == required_columns
        assert row["exact_formula_available"] in {"true", "false"}
        assert row["dynare_ready"] in {"true", "false"}
        assert row["wbs057a_category"] in valid_categories
        assert row["wbs057_resolution"] in valid_resolutions
        assert row["wbs057_blocking"] in {"true", "false"}
        assert row["deferred_to_wbs058"] in {"true", "false"}
        assert row["deferred_to_wbs059"] in {"true", "false"}
        assert row["source"] != ""
        assert row["source_location"] != ""
        assert row["registry_mapping"] != ""
        assert row["notes"] != ""


def test_wbs057_formula_extraction_counts_match_blocker_note():
    rows = _wbs057_rows()
    dynare_ready = [
        row for row in rows
        if row["dynare_ready"] == "true"
    ]
    blocking = [
        row for row in rows
        if row["wbs057_blocking"] == "true"
    ]
    deferred_wbs058 = [
        row for row in rows
        if row["deferred_to_wbs058"] == "true"
    ]
    deferred_wbs059_from_unresolved_27 = [
        row for row in rows
        if row["deferred_to_wbs059"] == "true"
        and row["equation_id"] not in {"EQ-PRICE-003", "EQ-MEAS-001..EQ-MEAS-015"}
    ]
    resolved_weights = [
        row for row in rows
        if row["wbs057_resolution"] == "resolved_parameter_weight_mapped"
    ]
    not_required = [
        row for row in rows
        if row["wbs057_resolution"] == "not_required_for_wbs057"
        and row["equation_id"] == "EQ-AGG-004"
    ]
    missing = [
        row for row in rows
        if row["wbs057_resolution"] == "still_missing_in_sources"
    ]
    human_review = [
        row for row in rows
        if row["wbs057_resolution"] == "needs_human_formula_review"
    ]

    assert len(dynare_ready) == 24
    assert len(blocking) == 0
    assert len(deferred_wbs058) == 11
    assert len(deferred_wbs059_from_unresolved_27) == 0
    assert len(resolved_weights) == 15
    assert len(not_required) == 1
    assert len(human_review) == 0
    assert len(missing) == 0
    assert any(
        row["equation_id"] == "EQ-AGG-004"
        and row["exact_formula_available"] == "false"
        and row["wbs057a_category"] == "true_missing_wp239_formula"
        and row["wbs057_resolution"] == "not_required_for_wbs057"
        for row in rows
    )
