import importlib.util
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WRAPPER_FILE = ROOT / "src" / "diagnostics" / "run_dynare.py"


def _load_wrapper():
    spec = importlib.util.spec_from_file_location("run_dynare", WRAPPER_FILE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_full_mh_storage_cli_options_are_accepted():
    wrapper = _load_wrapper()
    parser = wrapper.build_arg_parser()

    args = parser.parse_args(
        [
            "--mode",
            "full-mh",
            "--work-dir",
            "D:/SAMBA_RUN/work",
            "--tmp-dir",
            "D:/SAMBA_RUN/tmp",
            "--scratch-output-dir",
            "D:/SAMBA_RUN/scratch_output/posterior/full",
            "--repo-output-dir",
            "outputs/posterior/full",
            "--min-free-gb",
            "500",
            "--min-c-free-gb",
            "30",
            "--abort-d-free-gb",
            "50",
            "--abort-c-free-gb",
            "30",
            "--disk-telemetry-file",
            "tmp/telemetry.jsonl",
            "--disk-telemetry-interval-seconds",
            "5",
        ]
    )

    assert args.mode == "full-mh"
    assert args.work_dir == "D:/SAMBA_RUN/work"
    assert args.tmp_dir == "D:/SAMBA_RUN/tmp"
    assert args.scratch_output_dir == "D:/SAMBA_RUN/scratch_output/posterior/full"
    assert args.repo_output_dir == "outputs/posterior/full"
    assert args.min_free_gb == 500
    assert args.min_c_free_gb == 30
    assert args.abort_d_free_gb == 50
    assert args.abort_c_free_gb == 30
    assert args.disk_telemetry_file == "tmp/telemetry.jsonl"
    assert args.disk_telemetry_interval_seconds == 5


def test_full_mh_preflight_fails_when_external_drive_root_is_missing(tmp_path):
    wrapper = _load_wrapper()

    result = wrapper.preflight_full_mh_storage(
        tmp_path / "work",
        tmp_path / "tmp",
        tmp_path / "scratch",
        min_free_gb=1,
        min_c_free_gb=1,
        drive_exists_func=lambda _path: False,
    )

    assert result["status"] == "failed"
    assert "does not exist" in result["errors"][0]


def test_full_mh_preflight_fails_when_mocked_free_space_is_too_low(tmp_path):
    wrapper = _load_wrapper()

    class LowSpace:
        free = 10 * 1024 ** 3

    result = wrapper.preflight_full_mh_storage(
        tmp_path / "work",
        tmp_path / "tmp",
        tmp_path / "scratch",
        min_free_gb=500,
        min_c_free_gb=30,
        disk_usage_func=lambda _path: LowSpace,
        c_drive_root=tmp_path,
    )

    assert result["status"] == "failed"
    assert any("requires at least 500.000 GB" in error for error in result["errors"])
    assert any("requires at least 30.000 GB" in error for error in result["errors"])


def test_non_full_mh_mode_is_not_blocked_by_external_storage_guard(monkeypatch):
    wrapper = _load_wrapper()

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("full-MH preflight should not run for smoke mode")

    monkeypatch.setattr(wrapper, "preflight_full_mh_storage", fail_if_called)
    result = wrapper.run_dynare("smoke", dynare_executable="missing-dynare-command")

    assert result["status"] == "unavailable"
    assert "storage_preflight" not in result


def test_disk_abort_reason_triggers_when_mocked_d_free_space_below_threshold():
    wrapper = _load_wrapper()

    record = {
        "d_free_gb": 49.999,
        "c_free_gb": 100.0,
    }

    reason = wrapper.disk_abort_reason(
        record,
        abort_d_free_gb=50,
        abort_c_free_gb=30,
    )

    assert reason is not None
    assert "D: free space" in reason


def test_disk_abort_reason_triggers_when_mocked_c_free_space_below_threshold():
    wrapper = _load_wrapper()

    record = {
        "d_free_gb": 500.0,
        "c_free_gb": 29.999,
    }

    reason = wrapper.disk_abort_reason(
        record,
        abort_d_free_gb=50,
        abort_c_free_gb=30,
    )

    assert reason is not None
    assert "C: free space" in reason


def test_disk_telemetry_writes_valid_jsonl_to_tmp_path(tmp_path, monkeypatch):
    wrapper = _load_wrapper()
    telemetry_file = tmp_path / "telemetry.jsonl"
    monkeypatch.setattr(wrapper, "runtime_process_ids", lambda: {111, 222})

    class Usage:
        free = 64 * 1024 ** 3

    record = wrapper.disk_telemetry_record(
        c_drive_root=tmp_path,
        d_drive_root=tmp_path,
        child_pid=123,
        elapsed_seconds=1.25,
        disk_usage_func=lambda _path: Usage,
    )
    wrapper.write_disk_telemetry_record(telemetry_file, record)

    line = telemetry_file.read_text(encoding="utf-8").strip()
    payload = json.loads(line)
    assert payload["child_pid"] == 123
    assert payload["c_free_gb"] == 64
    assert payload["d_free_gb"] == 64
    assert payload["runtime_process_ids"] == [111, 222]


def test_run_command_disk_monitor_aborts_and_cleans_child_process(tmp_path):
    wrapper = _load_wrapper()
    telemetry_file = tmp_path / "telemetry.jsonl"

    class Usage:
        free = 49 * 1024 ** 3

    try:
        wrapper._run_command(
            [
                sys.executable,
                "-c",
                "import time; time.sleep(30)",
            ],
            tmp_path,
            timeout_seconds=30,
            disk_monitor={
                "c_drive_root": tmp_path,
                "d_drive_root": tmp_path,
                "abort_d_free_gb": 50,
                "abort_c_free_gb": 30,
                "telemetry_file": telemetry_file,
                "interval_seconds": 0.1,
                "disk_usage_func": lambda _path: Usage,
            },
        )
    except wrapper.DynareCommandAborted as exc:
        assert exc.returncode == wrapper.DISK_ABORT_RETURNCODE
        assert "D: free space" in exc.reason
        assert telemetry_file.exists()
    else:
        raise AssertionError("disk monitor should abort the sleeping child process")


def test_run_command_drains_large_stdout_while_process_runs(tmp_path):
    wrapper = _load_wrapper()
    line_count = 20000

    completed = wrapper._run_command(
        [
            sys.executable,
            "-c",
            (
                "import sys; "
                f"[print('x' * 200) for _ in range({line_count})]; "
                "sys.stdout.flush()"
            ),
        ],
        tmp_path,
        timeout_seconds=30,
    )

    assert completed.returncode == 0
    assert completed.stdout.count("\n") == line_count


def test_raw_chain_artifacts_are_copied_only_to_external_manifest_target(tmp_path):
    wrapper = _load_wrapper()
    work = tmp_path / "work"
    raw = tmp_path / "external_raw"
    chain = work / "metropolis" / "samba_classic_mh1_blck1.mat"
    chain.parent.mkdir(parents=True)
    chain.write_bytes(b"raw-chain")

    manifest = wrapper._generated_file_manifest(work, raw)
    entry = manifest["generated_artifacts"][0]

    assert entry["raw_chain_artifact"] is True
    assert entry["external_untracked"] is True
    assert entry["committed_to_git"] is False
    assert entry["external_raw_artifact"] == str(raw / "metropolis" / chain.name)
    assert "local_raw_artifact" not in entry
    assert (raw / "metropolis" / chain.name).read_bytes() == b"raw-chain"


def test_process_tree_cleanup_function_can_be_mocked_safely(monkeypatch):
    wrapper = _load_wrapper()
    calls = []

    def fake_run(command, **_kwargs):
        calls.append(command)

        class Completed:
            returncode = 0
            stdout = "SUCCESS"
            stderr = ""

        return Completed()

    monkeypatch.setattr(wrapper.subprocess, "run", fake_run)
    monkeypatch.setattr(wrapper.sys, "platform", "win32")

    result = wrapper.terminate_process_tree(12345)

    assert result["returncode"] == 0
    assert calls == [["taskkill", "/PID", "12345", "/T", "/F"]]


def test_default_external_storage_paths_point_to_confirmed_d_drive():
    if not sys.platform.startswith("win"):
        return

    wrapper = _load_wrapper()
    paths = wrapper.default_full_mh_storage_paths(ROOT)

    assert str(paths["work_dir"]).startswith("D:")
    assert str(paths["tmp_dir"]).startswith("D:")
    assert str(paths["scratch_output_dir"]).startswith("D:")
    assert paths["repo_output_dir"] == ROOT / "outputs" / "posterior" / "full"
