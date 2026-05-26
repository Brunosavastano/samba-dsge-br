from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DICTIONARY = ROOT / "docs" / "02_data_dictionary.md"


def test_wbs030_missing_policy_contract_is_documented():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")

    assert "### 5.5 WBS-030 missing-policy validation contract" in text
    assert "status: validation_contract_defined_no_data_created" in text
    assert "applies_to: all_planned_observables" in text
    assert "silent_missing: forbidden" in text
    assert "default_interpolation: forbidden" in text
    assert "required_missing_flags:" in text
    assert "missing_source_observation" in text
    assert "incomplete_quarter" in text
    assert "transformation_not_computed" in text
    assert "do not fill silently" in text
    assert "missing observation without a missing flag fails validation" in text
    assert "data_created: false" in text
    assert "pipeline_created: false" in text


def test_wbs030_missing_policy_does_not_create_data_or_pipeline():
    assert not (ROOT / "data").exists()
    assert not (ROOT / "src" / "data_pipeline").exists()
