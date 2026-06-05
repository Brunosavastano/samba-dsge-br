# WBS-073 Blockers

Status: `BLOCKED_WBS073_EXTERNAL_DRIVE_REVIEW`

Current blocker:
- WBS-073 full MH previously exhausted `C:\` during a long Dynare/Octave run.
- WBS-073 now requires the external-drive scratch strategy before any rerun.
- Do not rerun full MH on `C:\` without explicit approval.

External-drive preparation:
- confirmed drive: `D:\`
- free space observed during preparation: approximately 923 GB
- prepared directories: `D:\SAMBA_RUN\work`, `D:\SAMBA_RUN\tmp`,
  `D:\SAMBA_RUN\scratch_output\posterior\full`, `D:\SAMBA_RUN\logs`
- strategy doc: `docs/wbs073_external_drive_strategy.md`

Required next action:
- Bruno reviews the external-drive strategy and approves the WBS-073 full-MH
  rerun command.

WBS-073 remains blocked. Do not proceed to WBS-074, backtesting, Redux, or
sovereign-extension work until a completed WBS-073 summary is reviewed.
