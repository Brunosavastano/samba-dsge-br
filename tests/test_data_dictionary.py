from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DICTIONARY = ROOT / "docs" / "02_data_dictionary.md"


def test_data_dictionary_skeleton_exists_and_blocks_data_extraction():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")

    assert "gate_status: skeleton_created" in text
    assert "data_extraction_allowed: false" in text
    assert "core_source_ids_verified: false" in text
    assert "Gate 1b is not passed." in text


def test_data_dictionary_uses_tbd_source_ids_for_core_sources():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    expected = [
        "TBD-verify-in-task-WBS-024",
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

