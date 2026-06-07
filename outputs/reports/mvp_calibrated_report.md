# MVP Calibrated Report

Gate 3 status: completed for the calibrated SAMBA classic MVP.

Validated evidence:
- Dynare smoke/parse passed.
- Residuals passed: 36 equations; max absolute residual 0.0.
- BK passed: 26 unstable roots for 26 forward-looking variables; order and rank
  conditions verified.
- IRF restrictions passed: 5 evaluated, 5 passed, 0 failed.

Included model files:
- `model/samba_classic/samba_classic.mod`
- `model/samba_classic/calibration.m`
- `model/samba_classic/steady_state.m`
- `model/samba_classic/shocks.inc`
- `model/samba_classic/observables.inc`

Limits:
- No identification, priors, estimation, posterior, backtesting, Redux, or
  sovereign-extension work is approved by this report.
- Full validation remains a later Gate 6 task.
