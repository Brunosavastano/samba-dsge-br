# WBS-073 Full MH Configuration Proposal

approval_status: approved
approved_by: Bruno
approval_date: 2026-05-30
approved_timeout_seconds: 43200
approval_notes: approved with assistant-reviewed safeguards
current_status: BLOCKED_WBS073_FULL_MH_TIMEOUT
do_not_run_until_approved: false

This WBS-073 approval reconciles the completed WBS-072 pilot with the full-MH
operational validation step. It approves WBS-073 only and does not support
final publication-grade posterior inference claims.

Source basis:
- `docs/08_implementation_plan.md`: WBS-073 is full MH after WBS-072 pilot.
- `docs/wbs072_mh_pilot_config.md`: WBS-072 completed with tuned
  `mh_jscale=0.337313`.
- `docs/wbs072_blockers.md`: WBS-072 acceptance blocker resolved.

Approved WBS-073 configuration:
- `mh_replic`: 20000 per chain
- chains: 4 full-MH chains
- approved blocks: 2
- runtime Dynare `mh_nblocks`: 4 to implement the approved four-chain run
- burn-in: first 50 percent of each chain
- `mh_jscale`: 0.337313, inherited from the accepted WBS-072 pilot
- target acceptance band: 0.20 to 0.35
- target central acceptance ratio: 0.234
- approved timeout seconds: 43200

R-hat rule:
- compute R-hat for eligible estimated parameters and shock standard
  deviations if artifacts support it;
- R-hat must be finite and at or below 1.1 for Gate 5b acceptance;
- if R-hat is unavailable after full MH, WBS-073 remains blocked unless a
  parser issue is separately fixed and diagnostics are otherwise complete.

Allowed WBS-073 artifacts after approval:
- `outputs/posterior/full/wbs073_full_mh_summary.json`
- `outputs/posterior/full/wbs073_full_mh_diagnostics.md`
- `outputs/posterior/full/wbs073_full_mh_manifest.json`
- raw heavy chain artifacts must not be committed unless separately approved
  and small; generated raw filenames, sizes, and hashes must be summarized in
  the manifest

Forbidden artifacts:
- `outputs/backtesting/`
- validation/backtesting reports from WBS-075..079
- Redux files
- sovereign-extension files
- final posterior inference claims before later validation gates

Stop conditions:
- likelihood NaN or Inf;
- any chain fails to complete;
- average acceptance outside 0.20 to 0.35;
- R-hat unavailable, nonfinite, or above 1.1;
- generated artifacts would escape `outputs/posterior/full/`;
- full-MH runtime would require changing equations, priors, data, or
  calibration.

Validation commands after approval:
- `python src/diagnostics/run_dynare.py --mode full-mh --timeout-seconds 43200`
- `python -m pytest`
- `git diff --check`

## WBS-073 Run Result

The approved WBS-073 full-MH command was run with the approved timeout of
43200 seconds. It timed out before final diagnostics completed, with the stdout
tail showing convergence-diagnostic progress through parameter 28. Because the
run did not complete, R-hat was not available and WBS-073 remains blocked.

No backtesting, Redux, sovereign-extension, or WBS-074 artifacts were created.
