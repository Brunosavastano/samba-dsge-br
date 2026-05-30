# WBS-073 Full MH Configuration Proposal

approval_status: proposed
approved_by: pending
approval_date: pending
current_status: WBS-073_CONFIG_PROPOSED
do_not_run_until_approved: true

This proposal reconciles the completed WBS-072 pilot with the next WBS-073
full-MH step. It does not approve or run full MH, does not create
`outputs/posterior/full/`, and does not support posterior inference claims.

Source basis:
- `docs/08_implementation_plan.md`: WBS-073 is full MH after WBS-072 pilot.
- `docs/wbs072_mh_pilot_config.md`: WBS-072 completed with tuned
  `mh_jscale=0.337313`.
- `docs/wbs072_blockers.md`: WBS-072 acceptance blocker resolved.

Proposed WBS-073 configuration:
- `mh_replic`: 20000 per chain
- chains: 4 full-MH chains
- blocks: 2 Dynare MH blocks
- burn-in: first 50 percent of each chain
- `mh_jscale`: 0.337313, inherited from the accepted WBS-072 pilot
- target acceptance band: 0.20 to 0.35
- target central acceptance ratio: 0.234

R-hat rule:
- compute R-hat for eligible estimated parameters and shock standard
  deviations if artifacts support it;
- R-hat must be finite and at or below 1.1 for Gate 5b acceptance;
- if R-hat is unavailable after full MH, WBS-073 remains blocked for review.

Allowed WBS-073 artifacts after approval:
- `outputs/posterior/full/wbs073_full_mh_summary.json`
- `outputs/posterior/full/wbs073_full_mh_diagnostics.md`
- full-MH chain artifacts required by Dynare if summarized and scoped to
  `outputs/posterior/full/`

Forbidden artifacts:
- `outputs/backtesting/`
- validation/backtesting reports from WBS-075..079
- Redux files
- sovereign-extension files
- posterior inference claims before WBS-073 diagnostics pass

Stop conditions:
- likelihood NaN or Inf;
- any chain fails to complete;
- average acceptance outside 0.20 to 0.35;
- R-hat unavailable, nonfinite, or above 1.1;
- generated artifacts would escape `outputs/posterior/full/`;
- full-MH runtime would require changing equations, priors, data, or
  calibration.

Validation commands after approval:
- `python src/diagnostics/run_dynare.py --mode full-mh --timeout-seconds <approved_timeout>`
- `python -m pytest`
- `git diff --check`
