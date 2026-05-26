import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "03_calibration_notes.md"


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


def test_calibration_notes_do_not_create_forbidden_model_paths():
    forbidden = [
        ROOT / "model",
        ROOT / "src" / "data_pipeline",
    ]

    present = [str(path.relative_to(ROOT)) for path in forbidden if path.exists()]
    assert present == []
