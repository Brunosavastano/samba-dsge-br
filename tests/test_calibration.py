import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "03_calibration_notes.md"
CALIBRATION = ROOT / "model" / "samba_classic" / "calibration.m"


ASSIGNMENT_RE = re.compile(
    r"^\s*([A-Za-z]\w*)\s*=\s*([-+]?\d+(?:\.\d+)?)\s*;\s*$"
)
BLOCKING_STATUSES = {
    "estimated_in_samba_no_point_value_found",
    "missing_source",
    "naming_conflict",
}


def _source_tracking_rows() -> list[dict[str, str]]:
    text = NOTES.read_text(encoding="utf-8")
    lines = text.splitlines()
    heading = lines.index("## WBS-055 calibration source tracking")
    table_start = next(
        idx for idx in range(heading, len(lines))
        if lines[idx].startswith("| parameter |")
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


def _calibration_assignments() -> dict[str, str]:
    assignments = {}
    for line in CALIBRATION.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        match = ASSIGNMENT_RE.match(line)
        assert match, f"Unexpected calibration.m line: {line}"
        parameter, value = match.groups()
        assignments[parameter] = value
    return assignments


def test_calibration_file_exists_and_documents_source():
    text = CALIBRATION.read_text(encoding="utf-8")

    assert "docs/03_calibration_notes.md" in text
    assert "WBS-055" in text
    assert "Do not add undocumented parameters" in text


def test_calibration_assigns_only_usable_sourced_parameters():
    rows = _source_tracking_rows()
    usable_rows = {
        row["canonical_project_name"]: row
        for row in rows
        if row["usable_in_mvp_calibration_m"] == "true"
    }
    assignments = _calibration_assignments()

    assert set(assignments) == set(usable_rows)

    for parameter, value in assignments.items():
        row = usable_rows[parameter]
        assert row["value"] == value
        assert row["source"] != ""
        assert row["source_location"] != ""
        assert row["status"] not in BLOCKING_STATUSES


def test_calibration_does_not_use_legacy_or_blocked_parameters():
    assignments = _calibration_assignments()

    forbidden = {
        row["parameter"]
        for row in _source_tracking_rows()
        if row["usable_in_mvp_calibration_m"] == "false"
        or row["status"] in BLOCKING_STATUSES
    }

    assert set(assignments).isdisjoint(forbidden)
