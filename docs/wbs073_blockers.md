# WBS-073 Blockers

Status: `BLOCKED_WBS073_FULL_MH_DISK_ABORT_AND_DIAGNOSTICS`

Current blockers:

- Guarded WBS-073 full-MH rerun started from a clean archived external workdir
  and completed Metropolis chains, but the wrapper hard-aborted during
  post-processing when `D:\` free space reached 49.937 GB, below the approved
  50 GB runtime threshold.
- Finite likelihood was reported and no NaN/Inf likelihood blocker appeared.
- Acceptance values: 0.30705, 0.18170, 0.13610, 0.12315.
- Average acceptance ratio: 0.187, below the approved 0.20 to 0.35 band.
- R-hat status: above_threshold; max R-hat: 4.054739157907651.
- R-hat was computed, so the blocker is not parser unavailability.
- WBS-073 remains blocked. Do not proceed to WBS-074, backtesting, Redux, or
  sovereign-extension work.

Resolved preflight actions:

- stale `D:\SAMBA_RUN\work` was archived to
  `D:\SAMBA_RUN\archive\work_stale_20260606_173108`;
- an intermediate pipe-aborted workdir was archived to
  `D:\SAMBA_RUN\archive\work_pipe_abort_20260606_192912`;
- a fresh empty `D:\SAMBA_RUN\work` was created before the guarded rerun;
- no source files were deleted and no raw/heavy artifacts were committed.

Next safe action: Bruno/assistant review WBS-073 runtime/post-processing and MH
diagnostics before approving any rerun or tuning change. No model equation,
prior, data, calibration, observable, shock, sample, or MH-configuration change
was made.
