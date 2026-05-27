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


def test_wbs057_source_mapping_or_transcription_status_blocks_mod_file():
    rows = _wbs057_rows()
    blocking = [
        row["equation_id"]
        for row in rows
        if row["wbs057_blocking"] == "true"
    ]
    blockers = BLOCKERS.read_text(encoding="utf-8")
    status = _project_status_text()

    assert len(blocking) == 0
    assert (
        "WBS-057_READY_FOR_MOD" in status
        or "BLOCKED_WBS057_MOD_TRANSCRIPTION" in status
    )
    assert (
        "Remaining true WBS-057 blockers: 0" in blockers
        or "Remaining true WBS-057 source blockers: 0" in blockers
    )
    assert "Dynare-ready rows: 24" in blockers
    if "BLOCKED_WBS057_MOD_TRANSCRIPTION" in status:
        assert "exact executable Dynare equation text is not present" in blockers
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
        "wbs057a_category",
        "wbs057_resolution",
        "wbs057_blocking",
        "deferred_to_wbs058",
        "deferred_to_wbs059",
        "dynare_ready",
        "notes",
    }
    valid_categories = {
        "ready_not_reclassified",
        "true_missing_wp239_formula",
        "formula_available_but_mapping_missing",
        "registry_overreach_not_required_for_mvp",
        "belongs_to_wbs058_shocks",
        "belongs_to_wbs059_observables",
        "calibration_or_steady_state_dependency",
        "notation_alias_or_duplicate",
        "test_contract_issue",
        "reference_extraction_issue",
    }
    valid_resolutions = {
        "not_applicable",
        "resolved_exact_formula_mapped",
        "resolved_parameter_weight_mapped",
        "resolved_by_registry_mapping",
        "resolved_by_calibration_mapping",
        "not_required_for_wbs057",
        "needs_human_formula_review",
        "deferred_to_wbs059_observables",
        "still_missing_in_sources",
    }

    for row in _wbs057_rows():
        assert set(row) == required_columns
        assert row["exact_formula_available"] in {"true", "false"}
        assert row["dynare_ready"] in {"true", "false"}
        assert row["wbs057a_category"] in valid_categories
        assert row["wbs057_resolution"] in valid_resolutions
        assert row["wbs057_blocking"] in {"true", "false"}
        assert row["deferred_to_wbs058"] in {"true", "false"}
        assert row["deferred_to_wbs059"] in {"true", "false"}
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
    blocking = [
        row for row in rows
        if row["wbs057_blocking"] == "true"
    ]
    deferred_wbs058 = [
        row for row in rows
        if row["deferred_to_wbs058"] == "true"
    ]
    deferred_wbs059_from_unresolved_27 = [
        row for row in rows
        if row["deferred_to_wbs059"] == "true"
        and row["equation_id"] not in {"EQ-PRICE-003", "EQ-MEAS-001..EQ-MEAS-015"}
    ]
    resolved_weights = [
        row for row in rows
        if row["wbs057_resolution"] == "resolved_parameter_weight_mapped"
    ]
    not_required = [
        row for row in rows
        if row["wbs057_resolution"] == "not_required_for_wbs057"
        and row["equation_id"] == "EQ-AGG-004"
    ]
    missing = [
        row for row in rows
        if row["wbs057_resolution"] == "still_missing_in_sources"
    ]
    human_review = [
        row for row in rows
        if row["wbs057_resolution"] == "needs_human_formula_review"
    ]

    assert len(dynare_ready) == 24
    assert len(blocking) == 0
    assert len(deferred_wbs058) == 11
    assert len(deferred_wbs059_from_unresolved_27) == 0
    assert len(resolved_weights) == 15
    assert len(not_required) == 1
    assert len(human_review) == 0
    assert len(missing) == 0
    assert any(
        row["equation_id"] == "EQ-AGG-004"
        and row["exact_formula_available"] == "false"
        and row["wbs057a_category"] == "true_missing_wp239_formula"
        and row["wbs057_resolution"] == "not_required_for_wbs057"
        for row in rows
    )
