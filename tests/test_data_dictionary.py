from pathlib import Path
import csv
from io import StringIO


ROOT = Path(__file__).resolve().parents[1]
DATA_DICTIONARY = ROOT / "docs" / "02_data_dictionary.md"


def _csv_block_after(text: str, heading: str) -> list[dict[str, str]]:
    start = text.index(heading)
    fenced = text.index("```csv", start)
    body_start = text.index("\n", fenced) + 1
    body_end = text.index("```", body_start)
    rows = [
        line.strip()
        for line in text[body_start:body_end].splitlines()
        if line.strip()
    ]
    return list(csv.DictReader(StringIO("\n".join(rows))))


def test_data_dictionary_gate1b_is_approved_for_core_sources_only():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")

    assert "gate: Gate 1b" in text
    assert "gate_status: approved" in text
    assert "gate1b_passed: true" in text
    assert "data_extraction_allowed: true" in text
    assert "data_extraction_status: completed_wbs052_core_dataset" in text
    assert "core_source_ids_verified: true" in text
    assert "decision_status: approved" in text
    assert "approved_by: Bruno" in text
    assert "WBS-052 generated the core final-revised dataset from verified sources only." in text


def test_data_dictionary_uses_no_tbd_source_ids_for_core_sources_after_gate1b():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    assert "TBD-verify-in-task-WBS-024" not in text
    assert "TBD-verify-in-task-WBS-025" not in text
    assert "TBD-verify-in-task-WBS-026" not in text
    assert "TBD-verify-in-task-WBS-027" not in text
    assert "TBD-verify-in-task-WBS-045" not in text
    assert "TBD-verify-in-task-WBS-046" not in text
    assert "TBD-verify-in-task-WBS-047" not in text
    assert "TBD-verify-in-task-WBS-048" not in text
    assert "TBD-verify-in-task-WBS-049" not in text

    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    assert len(rows) == 9
    assert all(row["source_status"] == "verified" for row in rows)
    assert all("TBD" not in row["source_id"] for row in rows)


def test_data_dictionary_declares_required_metadata_fields():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    required_fields = [
        "series_id",
        "variable",
        "source_id",
        "revision_policy",
        "vintage_date",
        "frequency_model",
        "transform",
        "quarterly_conversion",
        "gate_status",
    ]

    missing = [field for field in required_fields if field not in text]
    assert missing == []


def test_real_gdp_source_is_verified_for_wbs024():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    gdp = by_series["br_gdp_real"]

    assert gdp["source"] == "IBGE SIDRA Contas Nacionais Trimestrais"
    assert gdp["source_id"] == "IBGE-SIDRA-CNT-1621-v584-c11255-90707-n1-1"
    assert gdp["source_status"] == "verified"
    assert gdp["wbs"] == "WBS-024"
    assert gdp["gate_status"] == "Gate 1b source verified"
    assert "https://sidra.ibge.gov.br/tabela/1621" in text
    assert "no data was extracted or saved in WBS-024" in text


def test_headline_ipca_source_is_verified_for_wbs025():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    ipca = by_series["br_ipca_headline"]

    assert ipca["source"] == "IBGE SIDRA Indice Nacional de Precos ao Consumidor Amplo"
    assert ipca["source_id"] == "IBGE-SIDRA-IPCA-1737-v63-n1-1"
    assert ipca["source_status"] == "verified"
    assert ipca["wbs"] == "WBS-025"
    assert ipca["gate_status"] == "Gate 1b source verified"
    assert "https://sidra.ibge.gov.br/tabela/1737" in text
    assert "quarterly transformation contract is defined in WBS-031" in text
    assert "no data was extracted or saved in WBS-025" in text


def test_selic_source_is_verified_for_wbs026():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    selic = by_series["br_selic"]

    assert selic["source"] == "Banco Central do Brasil SGS"
    assert selic["source_id"] == "BCB-SGS-432"
    assert selic["source_status"] == "verified"
    assert selic["wbs"] == "WBS-026"
    assert selic["gate_status"] == "Gate 1b source verified"
    assert "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json" in text
    assert "Selic over SGS 11 is a documented alternative" in text
    assert "interest-rate transformation contract is defined in WBS-032" in text
    assert "no data was extracted or saved in WBS-026" in text


def test_real_exchange_rate_source_is_verified_for_wbs027():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    exchange_rate = by_series["br_real_exchange_rate"]

    assert exchange_rate["source"] == "Banco Central do Brasil SGS"
    assert exchange_rate["source_id"] == "BCB-SGS-11752"
    assert exchange_rate["source_status"] == "verified"
    assert exchange_rate["wbs"] == "WBS-027"
    assert exchange_rate["gate_status"] == "Gate 1b source verified"
    assert "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11752/dados?formato=json" in text
    assert "q_t` up = BRL real depreciation" in text
    assert "no dataset was generated or saved in WBS-027" in text


def test_private_consumption_source_is_verified_for_wbs045():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    consumption = by_series["br_private_consumption"]

    assert consumption["source"] == "IBGE SIDRA Contas Nacionais Trimestrais"
    assert consumption["source_id"] == "IBGE-SIDRA-CNT-1621-v584-c11255-93404-n1-1"
    assert consumption["source_status"] == "verified"
    assert consumption["wbs"] == "WBS-045"
    assert consumption["gate_status"] == "Gate 1b source verified"
    assert "category 93404 Despesa de consumo das familias" in text
    assert "https://sidra.ibge.gov.br/tabela/1621" in text
    assert "no data was extracted or saved in WBS-045" in text


def test_investment_source_is_verified_for_wbs046():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    investment = by_series["br_investment"]

    assert investment["source"] == "IBGE SIDRA Contas Nacionais Trimestrais"
    assert investment["source_id"] == "IBGE-SIDRA-CNT-1621-v584-c11255-93406-n1-1"
    assert investment["source_status"] == "verified"
    assert investment["wbs"] == "WBS-046"
    assert investment["gate_status"] == "Gate 1b source verified"
    assert "category 93406 Formacao bruta de capital fixo" in text
    assert "https://sidra.ibge.gov.br/tabela/1621" in text
    assert "no data was extracted or saved in WBS-046" in text


def test_government_consumption_source_is_verified_for_wbs047():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    government = by_series["br_government_consumption"]

    assert government["source"] == "IBGE SIDRA Contas Nacionais Trimestrais"
    assert government["source_id"] == "IBGE-SIDRA-CNT-1621-v584-c11255-93405-n1-1"
    assert government["source_status"] == "verified"
    assert government["wbs"] == "WBS-047"
    assert government["gate_status"] == "Gate 1b source verified"
    assert "category 93405 Despesa de consumo da administracao publica" in text
    assert "https://sidra.ibge.gov.br/tabela/1621" in text
    assert "no data was extracted or saved in WBS-047" in text


def test_exports_source_is_verified_for_wbs048():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    exports = by_series["br_exports"]

    assert exports["source"] == "IBGE SIDRA Contas Nacionais Trimestrais"
    assert exports["source_id"] == "IBGE-SIDRA-CNT-1621-v584-c11255-93407-n1-1"
    assert exports["source_status"] == "verified"
    assert exports["wbs"] == "WBS-048"
    assert exports["gate_status"] == "Gate 1b source verified"
    assert "category 93407 Exportacao de bens e servicos" in text
    assert "https://sidra.ibge.gov.br/tabela/1621" in text
    assert "no data was extracted or saved in WBS-048" in text


def test_imports_source_is_verified_for_wbs049():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 3. Core sources required for Gate 1b")
    by_series = {row["series_id"]: row for row in rows}
    imports = by_series["br_imports"]

    assert imports["source"] == "IBGE SIDRA Contas Nacionais Trimestrais"
    assert imports["source_id"] == "IBGE-SIDRA-CNT-1621-v584-c11255-93408-n1-1"
    assert imports["source_status"] == "verified"
    assert imports["wbs"] == "WBS-049"
    assert imports["gate_status"] == "Gate 1b source verified"
    assert "category 93408 Importacao de bens e servicos (-)" in text
    assert "https://sidra.ibge.gov.br/tabela/1621" in text
    assert "no data was extracted or saved in WBS-049" in text


def test_free_and_administered_ipca_sources_are_verified_for_wbs050():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 4. Additional planned MVP observables")
    by_series = {row["series_id"]: row for row in rows}
    free = by_series["br_ipca_free"]
    administered = by_series["br_ipca_administered"]

    assert free["source"] == "Banco Central do Brasil SGS"
    assert free["source_id"] == "BCB-SGS-11428"
    assert free["source_status"] == "verified"
    assert free["wbs"] == "WBS-050"
    assert free["gate_status"] == "Gate 1b source verified"
    assert administered["source"] == "Banco Central do Brasil SGS"
    assert administered["source_id"] == "BCB-SGS-4449"
    assert administered["source_status"] == "verified"
    assert administered["wbs"] == "WBS-050"
    assert administered["gate_status"] == "Gate 1b source verified"
    assert "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11428/dados?formato=json" in text
    assert "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4449/dados?formato=json" in text
    assert "no data was extracted or saved in WBS-050" in text


def test_wbs051_auxiliary_sources_remain_explicitly_deferred():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = _csv_block_after(text, "## 4. Additional planned MVP observables")
    by_series = {row["series_id"]: row for row in rows}
    deferred_series = [
        "br_import_price_inflation",
        "br_inflation_target",
        "br_risk_premium",
        "br_output_gap",
    ]

    for series_id in deferred_series:
        row = by_series[series_id]
        assert row["source"] == "TBD"
        assert row["source_id"] == "TBD-verify-in-task-WBS-051"
        assert row["source_status"] == "tbd"
        assert row["wbs"] == "WBS-051"
        assert row["gate_status"] == "Gate 1a skeleton"

    assert text.count("source_selection_deferred") == len(deferred_series)
    assert "WBS-051 permits pinned source or TBD" in text
    assert "pi_target_t is explicit and exogenous/deterministic in the calibrated MVP" in text
    assert "risk_t has an AR(1) structural process" in text
    assert "y_gap_t is structural in the MVP" in text
    assert "no data was extracted or saved in WBS-051" in text


def test_wbs031_inflation_transformation_contract_forbids_simple_average():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")

    assert "### 5.1 WBS-031 inflation transformation contract" in text
    assert "status: contract_defined_no_data_created" in text
    assert "monthly_percent_input_rule" in text
    assert "product(1 + monthly_percent / 100) - 1" in text
    assert "index_input_rule" in text
    assert "log(index_last_month_of_quarter) - log(index_last_month_previous_quarter)" in text
    assert "simple_average_for_quarterly_inflation: forbidden" in text
    assert "output_unit_for_dataset_contract: decimal_rate" in text
    assert "data_created: false" in text
    assert "pipeline_created: false" in text
    assert "quarterly transformation contract is defined in WBS-031" in text
    assert not (ROOT / "src" / "data_pipeline").exists()


def test_wbs032_interest_rate_transformation_contract_is_documented():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")

    assert "### 5.2 WBS-032 interest-rate transformation contract" in text
    assert "status: contract_defined_no_data_created" in text
    assert "baseline_source: BCB-SGS-432" in text
    assert "raw_unit_expected: annual_percent_rate" in text
    assert "quarterly_level_rule" in text
    assert "arithmetic_average(raw_annual_percent_rate_observations_in_quarter)" in text
    assert "effective_quarterly_rule" in text
    assert "(1 + quarterly_policy_rate / 100)^(1 / 4) - 1" in text
    assert "selic_over_alternative" in text
    assert "output_unit_for_dataset_contract: annual_percent_rate" in text
    assert "data_created: false" in text
    assert "pipeline_created: false" in text
    assert "interest-rate transformation contract is defined in WBS-032" in text
    assert not (ROOT / "src" / "data_pipeline").exists()
