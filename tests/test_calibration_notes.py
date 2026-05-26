import csv
from io import StringIO
import re
from pathlib import Path
import hashlib


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "03_calibration_notes.md"
REGISTRY = ROOT / "docs" / "01_equation_registry.md"
BLOCKERS = ROOT / "docs" / "calibration_blockers.md"
CALIBRATION_FILE = ROOT / "model" / "samba_classic" / "calibration.m"
WP239 = ROOT / "docs" / "references" / "bcb_wp239_samba.pdf"
WP239_SHA256 = "8EC1FCF4CC37CEE968C4BF8D23D92DBE537F0401A25CA509BEFA84D8E0C1325E"
PLACEHOLDER_PARAMETERS = {
    "none",
    "none_for_mvp_monetary_shock_term",
    "source_located_parameters_pending_calibration",
    "source_located_weights_pending_calibration",
    "measurement_transform_pending_gate1b",
    "std_pending_calibration",
    "std_pending_future_phase",
    "std_pending_source_locator",
}
ALLOWED_SOURCE_STATUSES = {
    "sourced_from_samba_calibration",
    "sourced_from_samba_posterior_mean",
    "sourced_from_samba_posterior_mode",
    "sourced_from_project_decision",
    "estimated_in_samba_no_point_value_found",
    "missing_source",
    "naming_conflict",
    "not_required_for_mvp",
}
BLOCKING_SOURCE_STATUSES = {
    "estimated_in_samba_no_point_value_found",
    "missing_source",
    "naming_conflict",
}


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


def _registry_required_parameters() -> set[str]:
    text = REGISTRY.read_text(encoding="utf-8")
    rows = list(csv.DictReader(StringIO("\n".join(_csv_block_after(text, "## 4. Registry entries")))))
    required = set()

    for row in rows:
        for parameter in row["parameters"].split("|"):
            parameter = parameter.strip()
            if parameter and parameter not in PLACEHOLDER_PARAMETERS:
                required.add(parameter)

    return required


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


def test_calibration_notes_contract_flags():
    text = NOTES.read_text(encoding="utf-8")
    required_flags = [
        "status: calibration_source_taxonomy_ready",
        "calibration_values_approved: true",
        "steady_state_values_approved: false",
        "priors_approved: false",
        "dynare_allowed: false",
        "model_files_allowed: calibration_m_only",
        "no_parameter_value_invention: true",
    ]

    for flag in required_flags:
        assert flag in text


def test_calibration_notes_cover_required_registry_objects():
    text = NOTES.read_text(encoding="utf-8")
    required_terms = [
        "rho_r",
        "phi_pi",
        "phi_y",
        "r_ss",
        "psi_nfa",
        "nfa_ss",
        "rho_risk",
        "rho_sp_target",
        "phi_b",
        "phi_y_sp",
        "sp_ss",
        "rho_a",
        "alpha_a_target",
        "alpha_a_fx",
        "alpha_a_m",
        "alpha_a_mc",
        "rho_admin",
        "mc",
        "q_k",
        "wn",
        "lambda",
        "y_gap",
        "y_pot",
        "nfa",
        "m_int",
        "pi_target",
        "sp_target",
        "risk",
        "eps_monetary",
        "eps_admin",
        "eps_risk",
        "eps_pi_target",
    ]

    missing = [term for term in required_terms if term not in text]
    assert missing == []


def test_calibration_notes_do_not_assign_numeric_values():
    text = NOTES.read_text(encoding="utf-8")
    guarded_symbols = [
        "rho_r",
        "phi_pi",
        "phi_y",
        "r_ss",
        "psi_nfa",
        "nfa_ss",
        "rho_risk",
        "rho_sp_target",
        "phi_b",
        "phi_y_sp",
        "sp_ss",
        "rho_a",
        "alpha_a_target",
        "alpha_a_fx",
        "alpha_a_m",
        "rho_admin",
    ]
    assignment = re.compile(
        rf"^\s*({'|'.join(guarded_symbols)})\s*[:=]\s*[-+]?\d",
        re.MULTILINE,
    )

    assert assignment.search(text) is None


def test_wbs055_source_tracking_covers_registry_parameters_and_legacy_rows():
    rows = _source_tracking_rows()
    by_parameter = {row["parameter"]: row for row in rows}
    required_parameters = _registry_required_parameters()
    required_columns = {
        "parameter",
        "canonical_project_name",
        "aliases",
        "block",
        "role",
        "value",
        "source",
        "source_location",
        "status",
        "usable_in_mvp_calibration_m",
        "notes",
    }
    legacy_parameters = {
        "phi_y_sp",
        "sp_ss",
        "rho_a",
        "alpha_a_target",
        "alpha_a_m",
    }

    assert required_parameters == {
        row["parameter"]
        for row in rows
        if row["usable_in_mvp_calibration_m"] == "true"
    }
    assert legacy_parameters.issubset(by_parameter)
    assert len(rows) >= 16

    for parameter, row in by_parameter.items():
        assert set(row) == required_columns
        assert row["canonical_project_name"] != ""
        assert row["status"] in ALLOWED_SOURCE_STATUSES
        assert row["usable_in_mvp_calibration_m"] in {"true", "false"}
        assert row["notes"] != ""


def test_wbs055_source_status_counts_match_wp239_review():
    rows = _source_tracking_rows()
    counts = {status: 0 for status in ALLOWED_SOURCE_STATUSES}

    for row in rows:
        counts[row["status"]] += 1

    assert counts["sourced_from_samba_calibration"] == 2
    assert counts["sourced_from_samba_posterior_mean"] == 10
    assert counts["sourced_from_samba_posterior_mode"] == 0
    assert counts["estimated_in_samba_no_point_value_found"] == 0
    assert counts["missing_source"] == 0
    assert counts["naming_conflict"] == 0
    assert counts["sourced_from_project_decision"] == 0
    assert counts["not_required_for_mvp"] == 5


def test_wbs055_has_no_approved_numeric_values_without_source():
    for row in _source_tracking_rows():
        has_numeric_value = bool(re.fullmatch(r"[-+]?\d+(\.\d+)?", row["value"]))
        has_confirmed_source = bool(row["source"] and row["source_location"])

        assert row["status"] in ALLOWED_SOURCE_STATUSES
        if row["usable_in_mvp_calibration_m"] == "true":
            assert has_numeric_value
            assert has_confirmed_source
            assert row["status"] in {
                "sourced_from_samba_calibration",
                "sourced_from_samba_posterior_mean",
                "sourced_from_samba_posterior_mode",
                "sourced_from_project_decision",
            }
        else:
            assert row["value"] == ""
            assert row["status"] == "not_required_for_mvp"


def test_wp239_reference_is_local_and_hash_locked():
    assert WP239.exists()
    digest = hashlib.sha256(WP239.read_bytes()).hexdigest().upper()
    assert digest == WP239_SHA256


def test_calibration_file_only_blocked_if_unresolved_source_rows_remain():
    blocking = [
        row["parameter"]
        for row in _source_tracking_rows()
        if row["status"] in BLOCKING_SOURCE_STATUSES
    ]
    blockers = BLOCKERS.read_text(encoding="utf-8")

    assert blocking == []
    assert "WBS-055_READY_FOR_CALIBRATION_M" in blockers
    assert "Remaining `missing_source` count: 0" in blockers
    assert "Remaining `naming_conflict` count: 0" in blockers
    if blocking:
        assert not CALIBRATION_FILE.exists()


def test_wbs055_has_no_naming_conflicts_for_mvp_required_parameters():
    rows = _source_tracking_rows()
    conflicts = [
        row["parameter"]
        for row in rows
        if row["status"] == "naming_conflict"
        and row["usable_in_mvp_calibration_m"] == "true"
    ]
    assert conflicts == []


def test_calibration_notes_do_not_create_forbidden_executable_model_files():
    forbidden_suffixes = {".mod", ".m", ".inc"}
    model_dir = ROOT / "model"
    allowed_model_files = {
        ROOT / "model" / "samba_classic" / "calibration.m",
    }
    forbidden_model_files = []
    if model_dir.exists():
        forbidden_model_files = [
            str(path.relative_to(ROOT))
            for path in model_dir.rglob("*")
            if (
                path.is_file()
                and path.suffix in forbidden_suffixes
                and path not in allowed_model_files
            )
        ]

    forbidden_paths = [
        ROOT / "src" / "data_pipeline",
    ]
    present_paths = [str(path.relative_to(ROOT)) for path in forbidden_paths if path.exists()]

    assert forbidden_model_files == []
    assert present_paths == []
