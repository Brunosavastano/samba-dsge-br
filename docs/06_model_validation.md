---
status: gate3_calibrated_mvp_validation
do_not_treat_as_full_validation_result: true
wbs: WBS-064
gate: Gate 3
data_created: false
estimation_created: false
posterior_created: false
backtesting_created: false
results_source: docs/wbs064_mvp_calibrated_report.md
---

# Model Validation - Gate 3 Calibrated MVP

This file records only the Gate 3 calibrated SAMBA classic MVP validation. It is
not a final empirical validation result and does not approve Bayesian
estimation, posterior analysis, backtesting, Redux, or the sovereign extension.

## Gate 3 Evidence

- Dynare smoke/parse: passed.
- Steady-state residuals: passed; 36 equations; max absolute residual 0.0.
- BK check: passed; 26 unstable roots for 26 forward-looking variables; order
  and rank conditions verified.
- IRF restrictions: passed; 5 WBS-063 monetary-policy-shock targets evaluated;
  5 passed and 0 failed.

## Scope

The validated model is the calibrated SAMBA classic MVP in
`model/samba_classic/`, using `calibration.m`, `steady_state.m`,
`samba_classic.mod`, `shocks.inc`, and `observables.inc`.

## Still Pending

- WBS-065 local identification protocol.
- Priors and `priors.inc`.
- Likelihood smoke tests.
- Bayesian estimation and posterior outputs.
- Backtesting and full Gate 6 validation.
- Redux and sovereign-extension work.
