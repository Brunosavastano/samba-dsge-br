import importlib.util
import csv
import json
import shutil
import subprocess
import sys
from io import StringIO
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
TARGETS = ROOT / "docs" / "05_replication_targets.md"
WBS063_TARGETS = ROOT / "docs" / "wbs063_irf_targets.md"
BLOCKERS = ROOT / "docs" / "wbs063_blockers.md"
WRAPPER_FILE = ROOT / "src" / "diagnostics" / "run_dynare.py"
FORBIDDEN_GENERATED_PATHS = {
    ROOT / "outputs" / "irfs",
    ROOT / "outputs" / "posterior",
    ROOT / "outputs" / "identification",
    ROOT / "outputs" / "backtesting",
    ROOT / "model" / "samba_classic" / "priors.inc",
}


def _load_dynare_wrapper():
    spec = importlib.util.spec_from_file_location("run_dynare", WRAPPER_FILE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _execution_status() -> str:
    return next(
        line for line in STATUS.read_text(encoding="utf-8").splitlines()
        if line.startswith("Execution status:")
    )


def _forbidden_generated_paths() -> set[Path]:
    paths = set(FORBIDDEN_GENERATED_PATHS)
    if (
        "BLOCKED_WBS066_IDENTIFICATION_SOLVE" in _execution_status()
        or "WBS-066_COMPLETED" in _execution_status()
    ):
        paths.discard(ROOT / "outputs" / "identification")
    if "WBS-069_COMPLETED" in _execution_status():
        paths.discard(ROOT / "model" / "samba_classic" / "priors.inc")
    return paths


def _wbs063_target_rows() -> list[dict[str, str]]:
    text = WBS063_TARGETS.read_text(encoding="utf-8")
    start = text.index("## Target rows")
    fenced = text.index("```csv", start)
    body_start = text.index("\n", fenced) + 1
    body_end = text.index("```", body_start)
    return list(csv.DictReader(StringIO(text[body_start:body_end])))


def test_wbs063_has_five_source_backed_irf_targets():
    targets = TARGETS.read_text(encoding="utf-8")
    rows = _wbs063_target_rows()

    assert "targets_approved: false" in targets
    assert "wbs063_mvp_irf_targets_approved: true" in targets
    assert len(rows) == 5
    assert {row["status"] for row in rows} == {"approved_for_wbs063"}
    assert {row["shock_name"] for row in rows} == {"eps_monetary"}
    assert all(row["benchmark_source"] == "BCB_WP239" for row in rows)
    assert all(row["numeric_magnitude"] == "deferred" for row in rows)
    assert all(row["return_rule"] != "" for row in rows)


def test_wbs063_cannot_complete_without_approved_irf_targets():
    targets = TARGETS.read_text(encoding="utf-8")
    status = _execution_status()

    if (
        "targets_approved: false" in targets
        and "wbs063_mvp_irf_targets_approved: true" not in targets
    ):
        assert "WBS-063_COMPLETED" not in status
        assert "BLOCKED_WBS063_IRF_TARGETS" in status
        assert BLOCKERS.exists()
        blockers = BLOCKERS.read_text(encoding="utf-8")
        assert "approved IRF targets: 0" in blockers
        assert "required approved IRF targets: 5" in blockers


def test_wbs063_irf_restrictions_run_in_temp_without_committed_outputs():
    execution_status = _execution_status()
    if (
        "WBS-063_COMPLETED" not in execution_status
        and "BLOCKED_WBS063_IRF_TARGETS" not in execution_status
    ):
        return
    if shutil.which("dynare") is None:
        pytest.skip("Dynare is unavailable on PATH.")

    wrapper = _load_dynare_wrapper()
    assert wrapper.IRF_HORIZON == 20

    completed = subprocess.run(
        [sys.executable, str(WRAPPER_FILE), "--mode", "irf"],
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
    assert summary["mode"] == "irfs"
    assert summary["irf_horizon"] == 20
    assert summary["irf_restrictions_evaluated"] is True
    assert summary["irf_target_count"] == 5
    assert summary["irf_targets_failed"] == 0
    assert summary["persistent_outputs_created"] is False
    assert all(not path.exists() for path in _forbidden_generated_paths())
