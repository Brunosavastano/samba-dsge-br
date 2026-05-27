from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
SOURCING = ROOT / "docs" / "wbs057_equation_sourcing.md"
BLOCKERS = ROOT / "docs" / "wbs057_blockers.md"
MODEL_FILE = ROOT / "model" / "samba_classic" / "samba_classic.mod"


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


def test_wbs057_equation_sourcing_blocks_mod_when_rows_are_not_dynare_ready():
    rows = _wbs057_rows()
    not_ready = [
        row["equation_id"]
        for row in rows
        if row["dynare_ready"] == "false"
        and "Not required" not in row["notes"]
        and "not required" not in row["notes"]
        and "Do not implement" not in row["notes"]
        and "Measurement equations are WBS-059" not in row["registry_mapping"]
    ]
    blockers = BLOCKERS.read_text(encoding="utf-8")
    status = _project_status_text()

    assert not_ready
    assert "BLOCKED_WBS057_EQUATION_SOURCES" in status
    assert "Remaining unresolved MVP-required rows: 27" in blockers
    assert "Dynare-ready rows: 9" in blockers
    assert not MODEL_FILE.exists()


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
        "dynare_ready",
        "notes",
    }

    for row in _wbs057_rows():
        assert set(row) == required_columns
        assert row["exact_formula_available"] in {"true", "false"}
        assert row["dynare_ready"] in {"true", "false"}
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
    unresolved = [
        row for row in rows
        if row["dynare_ready"] == "false"
        and row["exact_formula_available"] == "true"
        and "Duplicate" not in row["notes"]
        and "Not required" not in row["notes"]
        and "not required" not in row["notes"]
        and "Do not implement" not in row["notes"]
    ]

    assert len(dynare_ready) == 9
    assert len(unresolved) == 26
    assert any(
        row["equation_id"] == "EQ-AGG-004"
        and row["exact_formula_available"] == "false"
        for row in rows
    )
