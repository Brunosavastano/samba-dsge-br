import csv
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "01_equation_registry.md"
LITERATURE_MAP = ROOT / "docs" / "00a_literature_map.md"


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


def test_equation_registry_exists_and_blocks_dynare_until_gate2b():
    text = REGISTRY.read_text(encoding="utf-8")

    assert "gate_status: aggregation_block_registered" in text
    assert "gate2b_passed: false" in text
    assert "dynare_allowed: false" in text
    assert "core_blocks_registered: false" in text
    assert "Gate 2b is not passed." in text
    assert not (ROOT / "model").exists()


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
    assert "eps_sp_target" in by_id["EQ-FISC-001"]["shocks"]
    assert "sp_target_separate_from_sp" in by_id["EQ-FISC-001"]["tests"]
    assert "government_consumption_instrument_located" in by_id["EQ-FISC-002"]["tests"]
    assert "b_represents_public_debt_gdp" in by_id["EQ-FISC-003"]["tests"]
    assert "no_regime_2016_2023_in_mvp" in by_id["EQ-FISC-004"]["tests"]


def test_administered_prices_registry_entries_are_complete_for_wbs038():
    text = REGISTRY.read_text(encoding="utf-8")
    entries = _registry_entries(text)
    admin_entries = [entry for entry in entries if entry["block"] == "ADMIN"]
    by_id = {entry["equation_id"]: entry for entry in admin_entries}

    assert set(by_id) == {"EQ-PRICE-001", "EQ-PRICE-002", "EQ-PRICE-003"}
    assert all(entry["gate"] == "WBS-038" for entry in admin_entries)
    assert "pi_a" in by_id["EQ-PRICE-001"]["variables"]
    assert "pi_target" in by_id["EQ-PRICE-001"]["variables"]
    assert "delta_q" in by_id["EQ-PRICE-001"]["variables"]
    assert "pi_m" in by_id["EQ-PRICE-001"]["variables"]
    assert "rho_a" in by_id["EQ-PRICE-001"]["parameters"]
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
