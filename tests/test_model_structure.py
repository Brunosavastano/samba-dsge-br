import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "model" / "samba_classic"
PROJECT_STATUS = ROOT / "docs" / "PROJECT_STATUS.md"


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
    return allowed


def test_samba_classic_structure_exists():
    assert MODEL_DIR.is_dir()
    assert (MODEL_DIR / "README.md").is_file()
    assert (MODEL_DIR / "manifest.json").is_file()


def test_samba_classic_manifest_is_structure_only():
    manifest = json.loads((MODEL_DIR / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["wbs"] == "WBS-054"
    assert manifest["status"] == "structure_only"
    assert manifest["dynare_version_verified"] == "7.0"
    assert manifest["octave_version_verified"] == "11.1.0"
    assert manifest["equation_registry"] == "docs/01_equation_registry.md"
    assert manifest["calibration_notes"] == "docs/03_calibration_notes.md"


def test_wbs054_does_not_create_executable_model_files():
    forbidden_suffixes = {".mod", ".m", ".inc"}
    forbidden = [
        path.relative_to(ROOT).as_posix()
        for path in MODEL_DIR.rglob("*")
        if (
            path.is_file()
            and path.suffix in forbidden_suffixes
            and path.relative_to(ROOT).as_posix() not in _allowed_executable_model_files()
        )
    ]

    assert forbidden == []
