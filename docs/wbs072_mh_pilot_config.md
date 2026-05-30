# WBS-072 MH Pilot Configuration Proposal

approval_status: proposed
current_status: WBS-072_CONFIG_PROPOSED
do_not_run_until_approved: true

This is a proposal only. It does not approve or run MH, does not start chains,
and does not create posterior draws.

Proposed pilot configuration:
- `mh_replic`: 2000 per chain
- chains: 2 independent pilot chains
- blocks: 2 Dynare MH blocks, if compatible with the wrapper/runtime
- burn-in: first 50 percent of each pilot chain excluded from diagnostics
- target acceptance band: 0.20 to 0.35
- R-hat scope: preliminary R-hat for key estimated parameters and shock
  standard deviations in `model/samba_classic/priors.inc`, if feasible from
  pilot artifacts

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
- preliminary R-hat is unavailable or above 1.1 for key parameters;
- any full-MH, backtesting, Redux, or sovereign artifact would be needed.

Validation commands after approval:
- `python src/diagnostics/run_dynare.py --mode mh-pilot --timeout-seconds 1800`
- `python -m pytest`
- `git diff --check`
