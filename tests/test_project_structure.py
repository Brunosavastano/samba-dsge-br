from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_bootstrap_files_exist():
    required = [
        "README.md",
        "CONTRIBUTING.md",
        ".gitignore",
        "pyproject.toml",
        "requirements.txt",
        "Makefile",
        "samba_dsge_br_spec_standalone_consolidado.md",
        "docs/08_implementation_plan.md",
        "docs/00b_modeling_decisions.md",
        "docs/gate0_approval_record.md",
        "docs/gate1b_approval_record.md",
        "docs/gate2b_approval_record.md",
        "config/sample.yaml",
        "config/environment.yaml",
        "models/registry.json",
        "outputs/schema/irf.schema.json",
        "outputs/schema/run_metadata.schema.json",
    ]

    missing = [path for path in required if not (ROOT / path).exists()]
    assert missing == []


def test_forbidden_implementation_paths_not_created_in_bootstrap():
    forbidden = [
        "model",
        "data",
        "src/data_pipeline",
    ]

    present = [path for path in forbidden if (ROOT / path).exists()]
    assert present == []


def test_readme_documents_model_directory_conventions():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "models/ = metadata registry" in readme
    assert "model/  = arquivos executaveis Dynare/MATLAB/Octave" in readme
    assert "pyproject.toml" in readme
    assert "requirements.txt" in readme
