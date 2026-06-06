# WBS-073 Full MH Diagnostics

Status: `failed_external_disk_guard_abort`.

This was an operational WBS-073 full-MH attempt using the confirmed external `D:\` scratch strategy. It is not final publication-grade posterior evidence.

## Result

- Start: 2026-06-05 23:33:51 America/Sao_Paulo.
- Abort: 2026-06-06 04:24:32 America/Sao_Paulo.
- Approximate elapsed time: 17441 seconds.
- Abort reason: `D:\` free space fell to approximately 527.253 GB and was still declining toward the 500 GB approved safety margin.
- `C:\` remained stable, around 152.6 GB free.
- After terminating the Dynare/Octave process tree, `D:\` returned to approximately 923.404 GB free.

## Diagnostics Availability

- Acceptance ratio: unavailable.
- R-hat: unavailable.
- Finite likelihood result: unavailable from final wrapper output.
- stdout/stderr logs in `D:\SAMBA_RUN\logs` remained empty because the wrapper was killed before final JSON output.

## Artifact Policy

- External raw artifact entries recorded in manifest: 6.
- Raw external artifacts are marked `external_untracked` and were not copied into the repo.
- No backtesting, Redux, sovereign-extension, or WBS-074 artifacts were created.
