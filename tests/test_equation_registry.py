import csv
import re
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "01_equation_registry.md"
LITERATURE_MAP = ROOT / "docs" / "00a_literature_map.md"
DATA_DICTIONARY = ROOT / "docs" / "02_data_dictionary.md"
PROJECT_STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
MODEL_FILE = ROOT / "model" / "samba_classic" / "samba_classic.mod"


def _csv_block_after(text: str, heading: str) -> list[str]:
    start = text.index(heading)
    fenced = text.index("```csv", start)
    body_start = text.index("\n", fenced) + 1
    body_end = text.index("```", body_start)
    return [
        line.strip()
        for line in text[body_start:body_end].splitlines()
        if line.strip()
    ]


def _registry_entries(text: str) -> list[dict[str, str]]:
    rows = _csv_block_after(text, "## 4. Registry entries")
    return list(csv.DictReader(StringIO("\n".join(rows))))


def _csv_dicts_after(text: str, heading: str) -> list[dict[str, str]]:
    rows = _csv_block_after(text, heading)
    return list(csv.DictReader(StringIO("\n".join(rows))))


def _pipe_tokens(value: str) -> set[str]:
    if value == "none":
        return set()
    return {token for token in value.split("|") if token}


def _wbs057_completed() -> bool:
    return "Execution status: WBS-057_COMPLETED" in PROJECT_STATUS.read_text(
        encoding="utf-8"
    )


def test_equation_registry_gate2b_is_approved_but_blocks_dynare_until_calibration():
    text = REGISTRY.read_text(encoding="utf-8")

    assert "gate_status: approved" in text
    assert "gate2b_passed: true" in text
    assert "dynare_allowed: false" in text
    assert "core_blocks_registered: true" in text
    assert "decision_status: approved" in text
    assert "approved_by: Bruno" in text
    assert "measurement_draft_registered: true" in text
    assert "Gate 2b is passed for the minimum viable equation registry." in text
    assert "Runtime verification and calibration notes are required" in text
    if (ROOT / "model").exists() and not _wbs057_completed():
        assert not list((ROOT / "model").rglob("*.mod"))


def test_equation_registry_declares_required_entry_fields():
    text = REGISTRY.read_text(encoding="utf-8")
    schema_rows = _csv_block_after(text, "## 2. Entry schema")
    declared_fields = {row.split(",", 1)[0] for row in schema_rows[1:]}

    required_fields = {
        "equation_id",
        "block",
        "title",
        "equation_type",
        "source_map_id",
        "source_reference_id",
        "source_locator",
        "variables",
        "parameters",
        "shocks",
        "tests",
        "status",
        "gate",
    }

    assert required_fields.issubset(declared_fields)


def test_equation_registry_namespaces_are_unique_and_sourced():
    text = REGISTRY.read_text(encoding="utf-8")
    literature = LITERATURE_MAP.read_text(encoding="utf-8")
    namespace_rows = _csv_block_after(text, "## 3. Planned namespaces")[1:]

    namespaces = [row.split(",", 1)[0] for row in namespace_rows]
    assert len(namespaces) == len(set(namespaces))

    for row in namespace_rows:
        source_map_id = row.split(",")[2]
        assert source_map_id in literature


def test_equation_registry_entries_are_unique_and_sourced():
    text = REGISTRY.read_text(encoding="utf-8")
    literature = LITERATURE_MAP.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    equation_ids = [entry["equation_id"] for entry in entries]

    assert len(equation_ids) == len(set(equation_ids))

    for entry in entries:
        assert entry["source_map_id"] in literature
        assert entry["source_reference_id"] in literature
        assert entry["status"] in {"draft", "sourced", "reviewed", "approved", "deferred"}


def test_registry_has_no_orphan_blocks_sources_or_links_for_wbs044():
    text = REGISTRY.read_text(encoding="utf-8")
    literature = LITERATURE_MAP.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    namespace_rows = _csv_dicts_after(text, "## 3. Planned namespaces")
    map_rows = (
        _csv_dicts_after(literature, "## 4. MVP block map")
        + _csv_dicts_after(literature, "## 5. Out-of-MVP map")
    )
    reference_rows = _csv_dicts_after(literature, "## 2. Canonical references")
    equation_ids = {entry["equation_id"] for entry in entries}
    blocks = {row["block"] for row in namespace_rows}
    map_ids = {row["map_id"] for row in map_rows}
    reference_ids = {row["reference_id"] for row in reference_rows}
    id_pattern = re.compile(r"^EQ-(MON|EXT|FISC|PRICE|HH|FIRM|AGG|SHOCK|MEAS)-\d{3}$")

    assert all(id_pattern.match(entry["equation_id"]) for entry in entries)
    assert all(entry["block"] in blocks for entry in entries)
    assert all(entry["source_map_id"] in map_ids for entry in entries)
    assert all(entry["source_reference_id"] in reference_ids for entry in entries)

    for entry in entries:
        linked_ids = [
            marker.removeprefix("linked_to_")
            for marker in entry["tests"].split(";")
            if marker.startswith("linked_to_EQ-")
        ]
        assert set(linked_ids).issubset(equation_ids)


def test_registry_measurement_variables_are_not_orphaned_for_wbs044():
    registry_text = REGISTRY.read_text(encoding="utf-8")
    dictionary_text = DATA_DICTIONARY.read_text(encoding="utf-8")
    entries = _registry_entries(registry_text)
    dictionary_rows = (
        _csv_dicts_after(dictionary_text, "## 3. Core sources required for Gate 1b")
        + _csv_dicts_after(dictionary_text, "## 4. Additional planned MVP observables")
    )
    dictionary_variables = {row["variable"] for row in dictionary_rows}
    dictionary_series_ids = {row["series_id"] for row in dictionary_rows}
    all_registry_variables = set().union(
        *(_pipe_tokens(entry["variables"]) for entry in entries)
    )
    measurement_entries = [entry for entry in entries if entry["block"] == "MEAS"]

    assert dictionary_variables.issubset(all_registry_variables)

    for entry in measurement_entries:
        model_var, series_id = entry["variables"].split("|", 1)
        assert model_var in dictionary_variables
        assert series_id in dictionary_series_ids


def test_monetary_policy_registry_entries_are_complete_for_wbs035():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    mon_entries = [entry for entry in entries if entry["block"] == "MON"]
    by_id = {entry["equation_id"]: entry for entry in mon_entries}

    assert set(by_id) == {"EQ-MON-001", "EQ-MON-002", "EQ-MON-003"}
    assert all(entry["gate"] == "WBS-035" for entry in mon_entries)
    assert "monetary_irf_sign_timing_magnitude_benchmark" in by_id["EQ-MON-001"]["tests"]
    assert "pi_target" in by_id["EQ-MON-001"]["variables"]
    assert "y_gap" in by_id["EQ-MON-001"]["variables"]
    assert "eps_pi_target_absent_in_calibrated_mvp" in by_id["EQ-MON-002"]["tests"]
    assert "eps_monetary" in by_id["EQ-MON-003"]["shocks"]


def test_external_registry_entries_are_complete_for_wbs036():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    ext_entries = [entry for entry in entries if entry["block"] == "EXT"]
    by_id = {entry["equation_id"]: entry for entry in ext_entries}

    assert set(by_id) == {"EQ-EXT-001", "EQ-EXT-002", "EQ-EXT-003", "EQ-EXT-004"}
    assert all(entry["gate"] == "WBS-036" for entry in ext_entries)
    assert "nfa" in by_id["EQ-EXT-001"]["variables"]
    assert "risk" in by_id["EQ-EXT-001"]["variables"]
    assert "psi_nfa" in by_id["EQ-EXT-001"]["parameters"]
    assert "nfa_debt_elastic_premium_present" in by_id["EQ-EXT-001"]["tests"]
    assert "rho_risk" in by_id["EQ-EXT-002"]["parameters"]
    assert "eps_risk" in by_id["EQ-EXT-002"]["shocks"]
    assert "external_balance_identity_located" in by_id["EQ-EXT-003"]["tests"]
    assert "q_up_means_brl_real_depreciation" in by_id["EQ-EXT-004"]["tests"]


def test_fiscal_registry_entries_are_complete_for_wbs037():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    fisc_entries = [entry for entry in entries if entry["block"] == "FISC"]
    by_id = {entry["equation_id"]: entry for entry in fisc_entries}

    assert set(by_id) == {"EQ-FISC-001", "EQ-FISC-002", "EQ-FISC-003", "EQ-FISC-004"}
    assert all(entry["gate"] == "WBS-037" for entry in fisc_entries)
    assert "sp_target" in by_id["EQ-FISC-001"]["variables"]
    assert "b" in by_id["EQ-FISC-001"]["variables"]
    assert "phi_b" in by_id["EQ-FISC-001"]["parameters"]
    assert "phi_y_sp" not in by_id["EQ-FISC-001"]["parameters"]
    assert "sp_ss" not in by_id["EQ-FISC-001"]["parameters"]
    assert "eps_sp_target" in by_id["EQ-FISC-001"]["shocks"]
    assert "sp_target_separate_from_sp" in by_id["EQ-FISC-001"]["tests"]
    assert "wp239_c31_no_output_gap_feedback" in by_id["EQ-FISC-001"]["tests"]
    assert "government_consumption_instrument_located" in by_id["EQ-FISC-002"]["tests"]
    assert "b_represents_public_debt_gdp" in by_id["EQ-FISC-003"]["tests"]
    assert "no_regime_2016_2023_in_mvp" in by_id["EQ-FISC-004"]["tests"]


def test_administered_prices_registry_entries_are_complete_for_wbs038():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    admin_entries = [entry for entry in entries if entry["block"] == "ADMIN"]
    by_id = {entry["equation_id"]: entry for entry in admin_entries}
    price_parameters = _pipe_tokens(by_id["EQ-PRICE-001"]["parameters"])

    assert set(by_id) == {"EQ-PRICE-001", "EQ-PRICE-002", "EQ-PRICE-003"}
    assert all(entry["gate"] == "WBS-038" for entry in admin_entries)
    assert "pi_a" in by_id["EQ-PRICE-001"]["variables"]
    assert "delta_q" in by_id["EQ-PRICE-001"]["variables"]
    assert "mc" in by_id["EQ-PRICE-001"]["variables"]
    assert "rho_admin" in price_parameters
    assert "alpha_a_fx" in price_parameters
    assert "alpha_a_mc" in price_parameters
    assert "theta_admin" in price_parameters
    assert "chi_admin" in price_parameters
    assert "rho_a" not in price_parameters
    assert "alpha_a_target" not in price_parameters
    assert "alpha_a_m" not in price_parameters
    assert "eps_admin" in by_id["EQ-PRICE-001"]["shocks"]
    assert "not_generic_shock" in by_id["EQ-PRICE-001"]["tests"]
    assert "admin_shock_source_located" in by_id["EQ-PRICE-002"]["tests"]
    assert "measurement_deferred_to_gate1b" in by_id["EQ-PRICE-003"]["tests"]


def test_household_registry_entries_are_complete_for_wbs039():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    hh_entries = [entry for entry in entries if entry["block"] == "HH"]
    by_id = {entry["equation_id"]: entry for entry in hh_entries}

    assert set(by_id) == {"EQ-HH-001", "EQ-HH-002", "EQ-HH-003", "EQ-HH-004"}
    assert all(entry["gate"] == "WBS-039" for entry in hh_entries)
    assert "lambda" in by_id["EQ-HH-001"]["variables"]
    assert "q_k" in by_id["EQ-HH-001"]["variables"]
    assert "euler_locator_present" in by_id["EQ-HH-001"]["tests"]
    assert "habit_state" in by_id["EQ-HH-002"]["variables"]
    assert "consumption_habit_locator_present" in by_id["EQ-HH-002"]["tests"]
    assert "wn" in by_id["EQ-HH-003"]["variables"]
    assert "labor_supply_locator_present" in by_id["EQ-HH-003"]["tests"]
    assert "rule_of_thumb_locator_present" in by_id["EQ-HH-004"]["tests"]


def test_firm_registry_entries_are_complete_for_wbs040():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    firm_entries = [entry for entry in entries if entry["block"] == "FIRM"]
    by_id = {entry["equation_id"]: entry for entry in firm_entries}

    assert set(by_id) == {"EQ-FIRM-001", "EQ-FIRM-002", "EQ-FIRM-003", "EQ-FIRM-004"}
    assert all(entry["gate"] == "WBS-040" for entry in firm_entries)
    assert "mc" in by_id["EQ-FIRM-001"]["variables"]
    assert "m_int" in by_id["EQ-FIRM-001"]["variables"]
    assert "production_locator_present" in by_id["EQ-FIRM-001"]["tests"]
    assert "phillips_locator_present" in by_id["EQ-FIRM-002"]["tests"]
    assert "mc_used_in_pricing" in by_id["EQ-FIRM-002"]["tests"]
    assert "q_k" in by_id["EQ-FIRM-003"]["variables"]
    assert "investment_locator_present" in by_id["EQ-FIRM-003"]["tests"]
    assert "imported_input_locator_present" in by_id["EQ-FIRM-004"]["tests"]


def test_aggregation_registry_entries_are_complete_for_wbs041():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    agg_entries = [entry for entry in entries if entry["block"] == "AGG"]
    by_id = {entry["equation_id"]: entry for entry in agg_entries}

    assert set(by_id) == {"EQ-AGG-001", "EQ-AGG-002", "EQ-AGG-003", "EQ-AGG-004"}
    assert all(entry["gate"] == "WBS-041" for entry in agg_entries)
    assert "market_clearing_locator_present" in by_id["EQ-AGG-001"]["tests"]
    assert "abs" in by_id["EQ-AGG-002"]["variables"]
    assert "nx" in by_id["EQ-AGG-002"]["variables"]
    assert "nfa" in by_id["EQ-AGG-002"]["variables"]
    assert "real_gdp_identity_located" in by_id["EQ-AGG-003"]["tests"]
    assert "gdp_deflator_identity_located" in by_id["EQ-AGG-003"]["tests"]
    assert "y_pot" in by_id["EQ-AGG-004"]["variables"]
    assert "y_gap_structural_variable_present" in by_id["EQ-AGG-004"]["tests"]


def test_shock_registry_entries_are_complete_for_wbs042():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    shock_entries = [entry for entry in entries if entry["block"] == "SHOCK"]
    by_shock = {entry["shocks"]: entry for entry in shock_entries}
    expected_shocks = {
        "eps_monetary",
        "eps_pi_target",
        "eps_fiscal_g",
        "eps_sp_target",
        "eps_tax",
        "eps_tfp",
        "eps_pref",
        "eps_investment",
        "eps_price_free",
        "eps_price_admin",
        "eps_wage",
        "eps_import_price",
        "eps_risk",
        "eps_foreign_y",
        "eps_foreign_r",
        "eps_foreign_pi",
        "eps_commodity",
    }

    assert set(by_shock) == expected_shocks
    assert all(entry["gate"] == "WBS-042" for entry in shock_entries)
    assert all(entry["equation_type"] == "shock_process" for entry in shock_entries)
    assert all("std_pending" in entry["parameters"] for entry in shock_entries)
    assert all("shock_name_declared" in entry["tests"] for entry in shock_entries)
    assert by_shock["eps_pi_target"]["status"] == "deferred"
    assert "eps_pi_target_off_in_calibrated_mvp" in by_shock["eps_pi_target"]["tests"]
    assert by_shock["eps_commodity"]["status"] == "deferred"
    assert "source_locator_pending" in by_shock["eps_commodity"]["tests"]


def test_measurement_registry_entries_are_draft_for_wbs043():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    meas_entries = [entry for entry in entries if entry["block"] == "MEAS"]
    by_variable = {
        entry["variables"].split("|", 1)[0]: entry
        for entry in meas_entries
    }
    expected_variables = {
        "y",
        "pi",
        "r",
        "q",
        "c",
        "i",
        "g",
        "x",
        "m",
        "pi_f",
        "pi_a",
        "pi_m",
        "pi_target",
        "risk",
        "y_gap",
    }

    assert set(by_variable) == expected_variables
    assert all(entry["gate"] == "WBS-043" for entry in meas_entries)
    assert all(entry["equation_type"] == "measurement_draft" for entry in meas_entries)
    assert all(entry["status"] == "draft" for entry in meas_entries)
    assert all(entry["source_map_id"] == "LM-MEAS-001" for entry in meas_entries)
    assert all("measurement_draft_until_gate1b" in entry["tests"] for entry in meas_entries)
    assert all("source_id_tbd_allowed_until_gate1b" in entry["tests"] for entry in meas_entries)
    assert all("measurement_transform_pending_gate1b" in entry["parameters"] for entry in meas_entries)
    assert all(entry["shocks"] == "none" for entry in meas_entries)
    assert "q_up_means_brl_real_depreciation" in by_variable["q"]["tests"]
    assert "pi_target_deterministic_in_calibrated_mvp" in by_variable["pi_target"]["tests"]
    assert "y_gap_structural_variable_present" in by_variable["y_gap"]["tests"]
    if (ROOT / "model").exists() and not _wbs057_completed():
        assert not list((ROOT / "model").rglob("*.mod"))


def test_wbs057b_symbol_mappings_are_registered_for_model_phase():
    text = REGISTRY.read_text(encoding="utf-8")
    rows = _csv_dicts_after(text, "## 5. WBS-057b Dynare symbol mappings")
    by_symbol = {row["wp239_symbol"]: row for row in rows}
    allowed_statuses = {
        "mapped_to_registry",
        "mapped_to_calibration",
        "alias_resolved",
        "deferred_to_wbs058_shocks",
    }

    assert len(rows) == 26
    assert by_symbol["cO_t"]["dynare_name"] == "c_o"
    assert by_symbol["sB_t"]["dynare_name"] == "risk_dom"
    assert by_symbol["piH_t"]["dynare_name"] == "pi_g|pi_i"
    assert by_symbol["vH_t"]["dynare_name"] == "v_g|v_i"
    assert by_symbol["theta_A"]["dynare_name"] == "theta_admin"
    assert by_symbol["theta_A"]["mapping_status"] == "mapped_to_calibration"
    assert by_symbol["chi_A"]["dynare_name"] == "chi_admin"
    assert by_symbol["chi_A"]["mapping_status"] == "mapped_to_calibration"
    assert {
        row["mapping_status"] for row in rows
    }.issubset(allowed_statuses)
    assert all(row["mapping_status"] != "missing_sourced_value" for row in rows)
    assert sum(
        row["mapping_status"] == "deferred_to_wbs058_shocks"
        for row in rows
    ) == 7
    assert MODEL_FILE.exists() == _wbs057_completed()
