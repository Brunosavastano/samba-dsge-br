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

    assert "gate_status: monetary_block_registered" in text
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
    by_id = {entry["equation_id"]: entry for entry in entries}

    assert set(by_id) == {"EQ-MON-001", "EQ-MON-002", "EQ-MON-003"}
    assert all(entry["block"] == "MON" for entry in entries)
    assert all(entry["gate"] == "WBS-035" for entry in entries)
    assert "monetary_irf_sign_timing_magnitude_benchmark" in by_id["EQ-MON-001"]["tests"]
    assert "pi_target" in by_id["EQ-MON-001"]["variables"]
    assert "y_gap" in by_id["EQ-MON-001"]["variables"]
    assert "eps_pi_target_absent_in_calibrated_mvp" in by_id["EQ-MON-002"]["tests"]
    assert "eps_monetary" in by_id["EQ-MON-003"]["shocks"]
