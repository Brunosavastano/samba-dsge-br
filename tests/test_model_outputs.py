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


def test_wbs057_equation_sourcing_blocks_mod_when_formulas_are_missing():
    rows = _wbs057_rows()
    missing = [
        row["equation_id"]
        for row in rows
        if row["status"] == "missing_formula"
    ]
    blockers = BLOCKERS.read_text(encoding="utf-8")
    status = _project_status_text()

    assert missing
    assert "BLOCKED_WBS057_EQUATION_SOURCES" in status
    assert "Missing exact formula count: 34" in blockers
    assert not MODEL_FILE.exists()


def test_wbs057_sourcing_uses_only_allowed_statuses():
    allowed = {
        "sourced_exact_formula",
        "sourced_project_decision",
        "loglinear_convention",
        "missing_formula",
        "not_required_for_mvp",
    }

    for row in _wbs057_rows():
        assert row["status"] in allowed
        assert row["usable_in_samba_classic_mod"] in {"true", "false"}
        if row["status"] == "missing_formula":
            assert row["usable_in_samba_classic_mod"] == "false"
