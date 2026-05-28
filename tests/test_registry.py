import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_STATUS = ROOT / "docs" / "PROJECT_STATUS.md"


def _wbs057_completed() -> bool:
    return "Execution status: WBS-057_COMPLETED" in PROJECT_STATUS.read_text(
        encoding="utf-8"
    )


def test_registry_json_is_valid_and_minimal_schema_present():
    registry_path = ROOT / "models" / "registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    required = {
        "model_id",
        "spec_version",
        "plan_version",
        "status",
        "description",
        "dynare_file",
        "steady_state_file",
        "calibration_file",
        "observables_file",
        "shocks_file",
        "priors_file",
        "data_config",
        "sample_config",
        "environment_config",
        "equation_registry",
        "data_dictionary",
        "created_at",
        "updated_at",
        "notes",
    }

    assert required.issubset(registry)


def test_registry_keeps_metadata_separate_from_executable_model_files():
    registry = json.loads((ROOT / "models" / "registry.json").read_text(encoding="utf-8"))

    assert registry["status"] == "planned"
    assert registry["dynare_file"].startswith("model/")
    assert "metadata only" in registry["notes"]
    assert (ROOT / registry["dynare_file"]).exists() == _wbs057_completed()
