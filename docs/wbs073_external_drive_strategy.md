# WBS-073 External-Drive Scratch Strategy

Status: `prepared_for_review`

Confirmed external drive: `D:\`

Purpose: keep WBS-073 full-MH scratch, temporary files, and heavy raw chain
artifacts off `C:\`. The repo keeps only lightweight summaries, diagnostics,
and manifests.

## Directory Layout

- `D:\SAMBA_RUN\work`
- `D:\SAMBA_RUN\tmp`
- `D:\SAMBA_RUN\scratch_output\posterior\full`
- `D:\SAMBA_RUN\logs`
- repo lightweight output: `outputs/posterior/full/`

## Future WBS-073 Command

```powershell
python src/diagnostics/run_dynare.py --mode full-mh --timeout-seconds 86400 --work-dir D:\SAMBA_RUN\work --tmp-dir D:\SAMBA_RUN\tmp --scratch-output-dir D:\SAMBA_RUN\scratch_output\posterior\full --repo-output-dir outputs\posterior\full --min-free-gb 500 --min-c-free-gb 30
```

## Runtime Rules

- Do not unplug `D:\` while Dynare/Octave is running.
- Do not allow Windows to sleep during the run.
- `TEMP`, `TMP`, and `TMPDIR` are set only for the Dynare child process.
- Dynare runs from the external work directory because model includes resolve
  relative to the working directory.
- Raw heavy chain artifacts remain on `D:\` and are marked external/untracked
  in the manifest.
- Only `wbs073_full_mh_summary.json`,
  `wbs073_full_mh_diagnostics.md`, and `wbs073_full_mh_manifest.*` are copied
  back to the repo.
- `C:\` may still be used by Windows pagefile/cache, so the wrapper keeps a
  30 GB `C:\` free-space guard.

## Preflight Guards

Before full-MH starts, the wrapper must verify:

- `D:\` exists;
- work/tmp/scratch directories exist and are writable;
- external scratch free space is at least 500 GB by default;
- `C:\` free space is at least 30 GB by default.

Full MH must not rerun until Bruno reviews this strategy and explicitly
approves the external-drive execution.
