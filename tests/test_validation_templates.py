from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "docs" / "05_replication_targets.md"
VALIDATION = ROOT / "docs" / "06_model_validation.md"


def test_replication_targets_template_has_required_irf_fields():
    text = TARGETS.read_text(encoding="utf-8")

    assert "status: template" in text
    assert "do_not_treat_as_validation_result: true" in text
    assert "data_created: false" in text
    assert "results_created: false" in text
    assert "expected_sign" in text
    assert "timing_window" in text
    assert "magnitude_band" in text
    assert "benchmark_source" in text
    assert "targets_approved: false" in text
    assert "earliest_target_fill_wbs: WBS-074" in text


def test_model_validation_template_is_not_a_result():
    text = VALIDATION.read_text(encoding="utf-8")

    assert text.startswith("---\nstatus: template\n")
    assert "do_not_treat_as_validation_result: true" in text
    assert "validation_approved: false" in text
    assert "earliest_validation_result_gate: Gate 6" in text
    assert "requires_estimation_outputs: true" in text
    assert "requires_backtesting_outputs: true" in text
    assert "no_result_invention: true" in text


def test_validation_templates_do_not_create_forbidden_implementation_files():
    model_dir = ROOT / "model"
    executable_model_files = []
    if model_dir.exists():
        executable_model_files = [
            path.relative_to(ROOT).as_posix()
            for path in model_dir.rglob("*")
            if path.is_file() and path.suffix in {".mod", ".m", ".inc"}
        ]

    assert executable_model_files == []
    assert not (ROOT / "src" / "data_pipeline").exists()
