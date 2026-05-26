import csv
from io import StringIO
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "03_calibration_notes.md"
REGISTRY = ROOT / "docs" / "01_equation_registry.md"
BLOCKERS = ROOT / "docs" / "calibration_blockers.md"
CALIBRATION_FILE = ROOT / "model" / "samba_classic" / "calibration.m"
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
    "sourced_from_samba",
    "sourced_from_project_decision",
    "missing_source",
    "not_required_for_mvp",
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
        "status: calibration_notes_no_values",
        "calibration_values_approved: false",
        "steady_state_values_approved: false",
        "priors_approved: false",
        "dynare_allowed: false",
        "model_files_allowed: false",
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


def test_wbs055_source_tracking_covers_registry_parameters_without_values():
    rows = _source_tracking_rows()
    by_parameter = {row["parameter"]: row for row in rows}
    required_parameters = _registry_required_parameters()

    assert set(by_parameter) == required_parameters
    assert len(required_parameters) >= 16

    for parameter, row in by_parameter.items():
        assert row["required_for_file"] == "model/samba_classic/calibration.m"
        assert row["status"] in ALLOWED_SOURCE_STATUSES
        assert row["value"] == ""
        assert row["source"] == ""
        assert row["source_location"] == ""
        assert row["source_to_check"] != ""


def test_wbs055_has_no_approved_numeric_values_without_source():
    for row in _source_tracking_rows():
        has_numeric_value = bool(re.fullmatch(r"[-+]?\d+(\.\d+)?", row["value"]))
        has_confirmed_source = bool(row["source"] and row["source_location"])

        assert row["status"] in ALLOWED_SOURCE_STATUSES
        assert not has_numeric_value or has_confirmed_source


def test_calibration_file_blocked_while_sources_are_missing():
    missing = [
        row["parameter"]
        for row in _source_tracking_rows()
        if row["status"] == "missing_source"
    ]
    blockers = BLOCKERS.read_text(encoding="utf-8")

    assert missing
    assert "BLOCKED_CALIBRATION_SOURCES" in blockers
    assert "rho_a" in blockers
    assert "rho_admin" in blockers
    assert not CALIBRATION_FILE.exists()


def test_calibration_notes_do_not_create_forbidden_executable_model_files():
    forbidden_suffixes = {".mod", ".m", ".inc"}
    model_dir = ROOT / "model"
    forbidden_model_files = []
    if model_dir.exists():
        forbidden_model_files = [
            str(path.relative_to(ROOT))
            for path in model_dir.rglob("*")
            if path.is_file() and path.suffix in forbidden_suffixes
        ]

    forbidden_paths = [
        ROOT / "src" / "data_pipeline",
    ]
    present_paths = [str(path.relative_to(ROOT)) for path in forbidden_paths if path.exists()]

    assert forbidden_model_files == []
    assert present_paths == []
