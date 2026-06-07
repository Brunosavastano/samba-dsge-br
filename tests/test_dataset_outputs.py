import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
MODEL_INPUT = ROOT / "data" / "model_input" / "classic_mvp.csv"
METADATA = ROOT / "data" / "model_input" / "classic_mvp_metadata.json"
OBSERVABLES = ROOT / "data" / "observables"


def _allowed_executable_model_files() -> set[str]:
    text = PROJECT_STATUS.read_text(encoding="utf-8")
    allowed = {
        "model/samba_classic/calibration.m",
        "model/samba_classic/steady_state.m",
    }
    if re.search(r"Execution status: WBS-057_COMPLETE", text):
        allowed.add("model/samba_classic/samba_classic.mod")
    if re.search(r"Execution status: .*WBS-058_COMPLETED", text):
        allowed.add("model/samba_classic/shocks.inc")
    if re.search(r"Execution status: .*WBS-059_COMPLETED", text):
        allowed.add("model/samba_classic/observables.inc")
    if re.search(r"Execution status: .*WBS-069_COMPLETED", text):
        allowed.add("model/samba_classic/priors.inc")
    return allowed

EXPECTED_SOURCE_IDS = {
    "br_gdp_real": "IBGE-SIDRA-CNT-1621-v584-c11255-90707-n1-1",
    "br_private_consumption": "IBGE-SIDRA-CNT-1621-v584-c11255-93404-n1-1",
    "br_investment": "IBGE-SIDRA-CNT-1621-v584-c11255-93406-n1-1",
    "br_government_consumption": "IBGE-SIDRA-CNT-1621-v584-c11255-93405-n1-1",
    "br_exports": "IBGE-SIDRA-CNT-1621-v584-c11255-93407-n1-1",
    "br_imports": "IBGE-SIDRA-CNT-1621-v584-c11255-93408-n1-1",
    "br_ipca_headline": "IBGE-SIDRA-IPCA-1737-v63-n1-1",
    "br_selic": "BCB-SGS-432",
    "br_real_exchange_rate": "BCB-SGS-11752",
}


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_wbs052_model_input_shape_sample_and_numeric_values():
    rows = _csv_rows(MODEL_INPUT)
    expected_columns = ["quarter", "y", "pi", "r", "q", "c", "i", "g", "x", "m"]

    assert rows
    assert list(rows[0]) == expected_columns
    assert len(rows) == 68
    assert rows[0]["quarter"] == "2003Q1"
    assert rows[-1]["quarter"] == "2019Q4"

    for row in rows:
        for column in expected_columns[1:]:
            float(row[column])


def test_wbs052_observable_files_use_verified_sources_and_contract_fields():
    for series_id, source_id in EXPECTED_SOURCE_IDS.items():
        rows = _csv_rows(OBSERVABLES / f"{series_id}.csv")

        assert len(rows) == 68
        assert rows[0]["quarter"] == "2003Q1"
        assert rows[-1]["quarter"] == "2019Q4"
        assert {row["source_id"] for row in rows} == {source_id}
        assert {row["revision_policy"] for row in rows} == {"final_revised"}
        assert {row["frequency_model"] for row in rows} == {"quarterly"}
        assert {row["missing_flag"] for row in rows} == {"none"}
        assert all(int(row["observation_count"]) >= 1 for row in rows)
        assert all(row["value"] != "" for row in rows)


def test_wbs052_metadata_documents_no_source_id_invention():
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))

    assert metadata["wbs"] == "WBS-052"
    assert metadata["status"] == "generated_from_verified_sources"
    assert metadata["sample"] == {
        "start": "2003Q1",
        "end": "2019Q4",
        "frequency": "quarterly",
        "revision_policy": "final_revised",
    }
    assert metadata["rows"] == 68
    assert metadata["source_ids"] == EXPECTED_SOURCE_IDS
    assert metadata["no_source_id_invention"] is True
    assert metadata["no_model_or_dynare_files_created"] is True


def test_wbs052_does_not_create_pipeline_or_executable_model_code():
    model_dir = ROOT / "model"
    executable_model_files = []
    if model_dir.exists():
        executable_model_files = [
            path.relative_to(ROOT).as_posix()
            for path in model_dir.rglob("*")
            if (
                path.is_file()
                and path.suffix in {".mod", ".m", ".inc"}
                and path.relative_to(ROOT).as_posix() not in _allowed_executable_model_files()
            )
        ]

    assert executable_model_files == []
    assert not (ROOT / "src" / "data_pipeline").exists()
