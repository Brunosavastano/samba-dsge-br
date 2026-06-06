# WBS-073 Blockers

Status: `BLOCKED_WBS073_EXTERNAL_WORKDIR_NOT_CLEAN`

Current blocker:
- Guarded rerun preflight found stale generated Dynare/Metropolis artifacts
  under `D:\SAMBA_RUN\work` from the previously aborted WBS-073 attempt.
- The documented guarded command reuses `D:\SAMBA_RUN\work`, so stale
  `samba_classic\metropolis`, `samba_classic\Output`, `samba_classic\prior`,
  and generated `+samba_classic` files could contaminate a new manifest/R-hat
  pass.
- `D:\` had approximately 923.404 GB free and `C:\` had approximately
  152.887 GB free, so disk capacity was not the blocker.
- No Dynare/MH rerun was started.
- Next safe action: Bruno approves either cleanup/archive of the old external
  work dir or a repo-documented isolated external work dir for the guarded
  WBS-073 rerun.

Previous blockers:
- `BLOCKED_WBS073_DISK_GUARD_PENDING_REVIEW`
- `BLOCKED_WBS073_EXTERNAL_DISK_GUARD`

Observed WBS-073 external-drive rerun:
- command used `D:\SAMBA_RUN\work`, `D:\SAMBA_RUN\tmp`, and
  `D:\SAMBA_RUN\scratch_output\posterior\full`;
- start: 2026-06-05 23:33:51 America/Sao_Paulo;
- controlled abort: 2026-06-06 04:24:32 America/Sao_Paulo;
- approximate elapsed time: 17441 seconds.

Exact blocker:
- `D:\` free space fell from approximately 923.422 GB to 527.253 GB while the
  run was still active and still declining toward the approved 500 GB safety
  margin;
- `C:\` remained stable, around 152.6 GB free;
- after terminating Python/Dynare/Octave process tree, `D:\` returned to
  approximately 923.404 GB free.

Diagnostics unavailable:
- acceptance ratio: unavailable;
- R-hat: unavailable;
- final finite-likelihood result: unavailable from wrapper JSON.

Artifact status:
- no raw/heavy chain files were copied into the repo;
- visible raw external artifacts remain under `D:\SAMBA_RUN\work`;
- lightweight repo artifacts summarize this failed operational attempt.

WBS-073 remains blocked. Do not proceed to WBS-074, backtesting, Redux, or
sovereign-extension work until Bruno reviews a revised WBS-073 runtime strategy.
