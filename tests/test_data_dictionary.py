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


def test_data_dictionary_skeleton_exists_and_blocks_data_extraction():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")

    assert "gate_status: skeleton_created" in text
    assert "data_extraction_allowed: false" in text
    assert "core_source_ids_verified: false" in text
    assert "Gate 1b is not passed." in text


def test_data_dictionary_uses_tbd_source_ids_for_core_sources():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    expected = [
        "TBD-verify-in-task-WBS-025",
        "TBD-verify-in-task-WBS-026",
        "TBD-verify-in-task-WBS-027",
        "TBD-verify-in-task-WBS-045",
        "TBD-verify-in-task-WBS-046",
        "TBD-verify-in-task-WBS-047",
        "TBD-verify-in-task-WBS-048",
        "TBD-verify-in-task-WBS-049",
    ]

    missing = [placeholder for placeholder in expected if placeholder not in text]
    assert missing == []
    assert "TBD-verify-in-task-WBS-024" not in text


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
