# WBS-073 Runtime Diagnostics

Status: `BLOCKED_WBS073_EXTERNAL_WORKDIR_NOT_CLEAN`

Scope: WBS-073 full-MH operational rerun using confirmed external `D:\` scratch
space. No WBS-074, backtesting, Redux, sovereign-extension, equation, prior,
data, calibration, observable, shock, sample, or `mh_jscale` change was made.

## Guard Implementation Prepared

Guard implementation prepared; no Dynare run performed for this update.

- start threshold: `D:\` at least 500 GB free.
- runtime hard abort: `D:\` below 50 GB free.
- runtime hard abort: `C:\` below 30 GB free.
- disk telemetry file: `outputs/posterior/full/wbs073_disk_telemetry.jsonl`.
- telemetry interval: 60 seconds during future full-MH runs.
- full-MH remains blocked until the guard implementation is reviewed and a
  separate guarded rerun is approved.

## Guarded Rerun Preflight

Bruno approved the guarded rerun for this pass, conditional on preflight. The
preflight did not start Dynare because `D:\SAMBA_RUN\work` still contains
generated artifacts from the previous aborted WBS-073 attempt:

- `D:\SAMBA_RUN\work\samba_classic\metropolis\*.mat`
- `D:\SAMBA_RUN\work\samba_classic\metropolis\metropolis.log`
- `D:\SAMBA_RUN\work\samba_classic\Output\samba_classic_mode.mat`
- `D:\SAMBA_RUN\work\samba_classic\prior\definition.mat`
- generated `D:\SAMBA_RUN\work\+samba_classic\...` files

Free-space checks passed at preflight: `D:\` approximately 923.404 GB free and
`C:\` approximately 152.887 GB free. The blocker is contamination risk from the
stale external work directory, not current disk capacity.

## Command

```powershell
python src/diagnostics/run_dynare.py --mode full-mh --timeout-seconds 86400 --work-dir D:\SAMBA_RUN\work --tmp-dir D:\SAMBA_RUN\tmp --scratch-output-dir D:\SAMBA_RUN\scratch_output\posterior\full --repo-output-dir outputs/posterior/full --min-free-gb 500 --min-c-free-gb 30
```

## Storage Preflight

- `C:\` free before run: approximately 155.018 GB.
- `D:\` free before run: approximately 923.422 GB.
- approved external minimum: 500 GB free.
- approved `C:\` safety margin: 30 GB free.

## Runtime Observation

- start: 2026-06-05 23:33:51 America/Sao_Paulo.
- controlled abort: 2026-06-06 04:24:32 America/Sao_Paulo.
- approximate elapsed time: 17441 seconds.
- `D:\` free space fell to approximately 527.253 GB and was still declining
  toward the approved 500 GB guard.
- `C:\` remained stable around 152.6 GB free.
- after terminating the process tree, `D:\` returned to approximately
  923.404 GB free.

## Process Cleanup

The Python/Dynare/Octave process tree was terminated manually before the
external drive crossed the approved safety margin. No project Dynare/Octave
process remained active after cleanup.

## Artifact Findings

- repo raw/heavy chain files: none.
- external visible artifacts: small Metropolis `.mat` block files and
  `metropolis.log` under `D:\SAMBA_RUN\work\samba_classic\metropolis`.
- stdout/stderr files under `D:\SAMBA_RUN\logs` remained empty because the
  wrapper was killed before final JSON output.
- lightweight repo artifacts summarize this failed operational attempt:
  `outputs/posterior/full/wbs073_full_mh_summary.json`,
  `outputs/posterior/full/wbs073_full_mh_diagnostics.md`, and
  `outputs/posterior/full/wbs073_full_mh_manifest.json`.

## Diagnostics Availability

- acceptance ratio: unavailable.
- R-hat: unavailable.
- finite likelihood from final wrapper output: unavailable.

Conclusion: WBS-073 remains blocked by transient/open runtime disk use during
the full-MH run. The external drive protected `C:\`, but the approved full-MH
configuration still consumed too much transient external disk space for the
current guard.
