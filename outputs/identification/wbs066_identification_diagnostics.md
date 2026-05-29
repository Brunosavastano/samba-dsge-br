# WBS-066 Identification Diagnostics

Status: BLOCKED_WBS066_IDENTIFICATION_SOLVE

Scope: local identification diagnostics for the calibrated SAMBA classic MVP.

Inputs used:
- `model/samba_classic/samba_classic.mod`
- `model/samba_classic/calibration.m`
- `model/samba_classic/steady_state.m`
- `model/samba_classic/shocks.inc`
- `model/samba_classic/observables.inc`

Probe: temporary Dynare model with `steady; check; identification;` appended.

Observed result:
- `steady; check;` passed the Blanchard-Kahn check.
- Unstable roots: 26.
- Forward-looking variables: 26.
- Dynare reported that order and rank conditions are verified.
- `identification;` stopped with `info = 3`.
- Identification message: `Current_params` does not solve because Blanchard and Kahn conditions are not satisfied and there is no stable equilibrium.

Interpretation: WBS-066 remains blocked by a Dynare identification solve mismatch. The model should not proceed to WBS-067 until this mismatch is diagnosed.

Forbidden artifacts not created:
- no priors
- no posterior outputs
- no Bayesian estimation
- no backtesting outputs
- no Redux files
- no sovereign-extension files
