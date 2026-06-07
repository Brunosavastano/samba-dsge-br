# WBS-073 Runtime Diagnostics

Status: `BLOCKED_WBS073_FULL_MH_DISK_ABORT_AND_DIAGNOSTICS`

Scope: WBS-073 guarded full-MH operational rerun using confirmed external
`D:\` scratch space. No WBS-074, backtesting, Redux, sovereign-extension,
equation, prior, data, calibration, observable, shock, sample, `mh_jscale`,
`mh_replic`, chain, burn-in, or MH-configuration change was made.

## External Workdir Cleanup

The stale external work directory was handled before the rerun:

- stale workdir: `D:\SAMBA_RUN\work`
- archive path: `D:\SAMBA_RUN\archive\work_stale_20260606_173108`
- stale file count: 87
- stale total bytes: 19,202,580
- action: renamed/moved only; no source files deleted
- fresh workdir: `D:\SAMBA_RUN\work` recreated empty

An intermediate wrapper-abort workdir was also archived after diagnosing a
mechanical pipe-drain issue:

- archive path: `D:\SAMBA_RUN\archive\work_pipe_abort_20260606_192912`
- file count: 80
- total bytes: 319,111
- partial telemetry moved to `D:\SAMBA_RUN\logs`
- no raw/heavy artifacts copied into the repo

## Wrapper Runtime Fix

The first guarded attempt after workdir cleanup stalled because the wrapper
started Dynare with captured stdout/stderr but did not drain those pipes while
the child process was running. The process tree was terminated with `taskkill`
before any new full-MH result was accepted.

`src/diagnostics/run_dynare.py` now drains stdout and stderr on background
threads while the child process runs. This is a mechanical wrapper/runtime fix;
it does not change model economics or MH configuration.

## Guarded Rerun

Command used the repo-documented external scratch strategy with:

- work dir: `D:\SAMBA_RUN\work`
- temp dir: `D:\SAMBA_RUN\tmp`
- scratch output dir: `D:\SAMBA_RUN\scratch_output\posterior\full`
- repo output dir: `outputs/posterior/full`
- start guard: `D:\` at least 500 GB free
- hard abort: `D:\` below 50 GB free
- hard abort: `C:\` below 30 GB free

Storage preflight passed:

- `D:\` free before run: 923.404 GB
- `C:\` free before run: 152.955 GB
- fresh workdir item count: 0

## Result

The guarded full-MH run produced lightweight diagnostics but did not pass
WBS-073:

- status: failed
- wrapper return code: 125
- disk abort: true
- abort point: `D:\` free space 49.937 GB, below the 50 GB hard threshold
- `C:\` free space at abort telemetry: 151.364 GB
- final observed free space after cleanup: `C:\` 151.33 GB, `D:\` 923.37 GB
- chains completed: true
- finite likelihood reported: true
- NaN/Inf likelihood blocker: not observed
- acceptance values: 0.30705, 0.18170, 0.13610, 0.12315
- average acceptance ratio: 0.187
- target acceptance band: 0.20 to 0.35
- R-hat status: above_threshold
- max R-hat: 4.054739157907651

## Artifact Status

Lightweight repo artifacts:

- `outputs/posterior/full/wbs073_full_mh_summary.json`
- `outputs/posterior/full/wbs073_full_mh_diagnostics.md`
- `outputs/posterior/full/wbs073_full_mh_manifest.json`

Raw chain artifacts remain external and untracked under
`D:\SAMBA_RUN\scratch_output\posterior\full`. The manifest records external raw
artifact paths, sizes, hashes, and `external_untracked` status. No raw/heavy
chain files were staged in the repo.

Conclusion: WBS-073 remains blocked by the disk guard abort and by MH
diagnostics outside acceptance/R-hat criteria. Do not proceed to WBS-074,
backtesting, Redux, or sovereign-extension work.
