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


def test_wbs028_observables_require_quarterly_model_frequency():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")
    rows = (
        _csv_block_after(text, "## 3. Core sources required for Gate 1b")
        + _csv_block_after(text, "## 4. Additional planned MVP observables")
    )

    assert rows
    assert all(row["frequency_model"] == "quarterly" for row in rows)


def test_wbs028_frequency_validation_contract_is_documented():
    text = DATA_DICTIONARY.read_text(encoding="utf-8")

    assert "### 5.3 WBS-028 quarterly frequency validation contract" in text
    assert "status: validation_contract_defined_no_data_created" in text
    assert "frequency_model_required: quarterly" in text
    assert "applies_to: all_planned_observables" in text
    assert "frequency_model = quarterly" in text
    assert "missing or non-quarterly frequency_model fails validation" in text
    assert "data_created: false" in text
    assert "pipeline_created: false" in text
    assert not (ROOT / "data").exists()
    assert not (ROOT / "src" / "data_pipeline").exists()
