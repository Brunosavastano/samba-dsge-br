# WBS-072 MH Pilot Configuration Proposal

approval_status: approved
approved_by: Bruno
approval_date: 2026-05-30
current_status: WBS-072_CONFIG_APPROVED
completion_status: WBS-072_COMPLETED
do_not_run_until_approved: false
amendment: R-hat unavailable is warning, not blocker.

This configuration is approved for WBS-072 only. It does not approve WBS-073
full MH and does not support posterior inference claims from the pilot.

Proposed pilot configuration:
- `mh_replic`: 2000 per chain
- chains: 2 independent pilot chains
- blocks: 2 Dynare MH blocks, if compatible with the wrapper/runtime
- burn-in: first 50 percent of each pilot chain excluded from diagnostics
- target acceptance band: 0.20 to 0.35
- target central acceptance ratio: 0.234
- R-hat scope: compute preliminary R-hat for key estimated parameters and shock
  standard deviations in `model/samba_classic/priors.inc`, if feasible from
  pilot artifacts
- R-hat policy: unavailable R-hat or R-hat above 1.1 is a pilot diagnostic
  warning, not a WBS-072 blocker; it is not final convergence evidence

Allowed WBS-072 artifacts after approval:
- `outputs/posterior/pilot/wbs072_mh_pilot_summary.json`
- `outputs/posterior/pilot/wbs072_mh_pilot_diagnostics.md`
- temporary Dynare pilot files only if summarized and not treated as full
  posterior evidence

Forbidden until WBS-073:
- `outputs/posterior/full/`
- full MH chains
- posterior validation/backtesting outputs
- `outputs/backtesting/`
- Redux or sovereign-extension files

Stop conditions:
- Dynare exits nonzero or times out;
- likelihood becomes NaN or Inf;
- acceptance rate falls outside 0.20 to 0.35;
- any full-MH, backtesting, Redux, or sovereign artifact would be needed.

Diagnostic warnings, not stop conditions:
- preliminary R-hat is unavailable;
- preliminary R-hat is above 1.1 for key parameters.

Validation commands after approval:
- `python src/diagnostics/run_dynare.py --mode mh-pilot --timeout-seconds 1800`
- `python -m pytest`
- `git diff --check`

## WBS-072 Pilot Tuning Result

The approved pilot initially returned average acceptance `0.1325`, below the
approved `0.20` to `0.35` band. Only the proposal scale was tuned; model
equations, priors, data, and calibration were not changed.

Tuning rule:
- Dynare default `mh_jscale`: `0.449778`, computed as `2.38 / sqrt(28)`
  estimated parameters.
- Approved bounded attempt used: `mh_jscale = 0.337313`, approximately
  `0.75` times the Dynare default.

Accepted WBS-072 pilot result:
- command: `python src/diagnostics/run_dynare.py --mode mh-pilot --timeout-seconds 1800 --mh-jscale 0.337313`
- `mh_replic`: 2000 per chain
- chains: 2
- blocks: 2
- burn-in: 50 percent
- average acceptance ratio: `0.28225`
- chain acceptance ratios: `0.2725`, `0.2920`
- R-hat status: unavailable warning, not final convergence evidence
- posterior inference claimed: false
- full MH started: false
