import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "03_calibration_notes.md"
CALIBRATION = ROOT / "model" / "samba_classic" / "calibration.m"
STEADY_STATE = ROOT / "model" / "samba_classic" / "steady_state.m"
STEADY_STATE_BLOCKERS = ROOT / "docs" / "steady_state_blockers.md"
PROJECT_STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
WRAPPER = ROOT / "src" / "diagnostics" / "run_dynare.py"


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


def _residual_parameter_rows() -> list[dict[str, str]]:
    text = NOTES.read_text(encoding="utf-8")
    lines = text.splitlines()
    heading = lines.index("## WBS-061 residual-blocking parameter assignments")
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


def _steady_state_assignments() -> dict[str, str]:
    assignments = {}
    for line in STEADY_STATE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        match = ASSIGNMENT_RE.match(line)
        assert match, f"Unexpected steady_state.m line: {line}"
        variable, value = match.groups()
        assignments[variable] = value
    return assignments


def _steady_state_rows() -> list[dict[str, str]]:
    text = NOTES.read_text(encoding="utf-8")
    lines = text.splitlines()
    heading = lines.index("## Approved MVP steady-state assignments")
    table_start = next(
        idx for idx in range(heading, len(lines))
        if lines[idx].startswith("| variable |")
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


def test_calibration_file_exists_and_documents_source():
    text = CALIBRATION.read_text(encoding="utf-8")

    assert "docs/03_calibration_notes.md" in text
    assert "WBS-055" in text
    assert "Do not add undocumented parameters" in text


def test_calibration_assigns_only_usable_sourced_parameters():
    rows = _source_tracking_rows() + _residual_parameter_rows()
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


def test_wbs056_steady_state_sources_are_documented_without_missing_sources():
    rows = _steady_state_rows()
    missing = [row["variable"] for row in rows if row["status"] == "missing_source"]

    assert rows
    assert missing == []
    assert all(row["usable_in_steady_state_m"] == "true" for row in rows)


def test_wbs056_steady_state_file_exists_and_matches_documented_assignments():
    text = STEADY_STATE.read_text(encoding="utf-8")
    rows = _steady_state_rows()
    usable_rows = {
        row["variable"]: row
        for row in rows
        if row["usable_in_steady_state_m"] == "true"
    }
    assignments = _steady_state_assignments()

    assert "docs/03_calibration_notes.md" in text
    assert "WBS-056" in text
    assert set(assignments) == set(usable_rows)

    for variable, value in assignments.items():
        row = usable_rows[variable]
        assert row["value_or_expression"] == value
        assert row["status"] != "missing_source"
        if value == "0":
            assert row["status"] == "zero_by_loglinear_convention"
        else:
            assert row["status"] in {
                "derived_from_calibration_parameter",
                "sourced_from_samba",
                "sourced_from_project_decision",
            }


def test_wbs061_steady_state_residuals_below_tolerance_after_wbs061():
    status = PROJECT_STATUS.read_text(encoding="utf-8")
    if "WBS-061_COMPLETED" not in status:
        return
    if shutil.which("dynare") is None:
        pytest.skip("Dynare is unavailable on PATH.")

    completed = subprocess.run(
        [
            sys.executable,
            str(WRAPPER),
            "--mode",
            "residuals",
            "--residual-tolerance",
            "1e-8",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=240,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    summary = json.loads(completed.stdout)
    assert summary["status"] == "passed"
    assert summary["residual_equation_count"] > 0
    assert summary["nonfinite_residual_count"] == 0
    assert summary["max_abs_residual"] <= 1e-8
