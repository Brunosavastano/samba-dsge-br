# WBS-066 Identification Diagnostics

Status: WBS-066_COMPLETED

Scope: local identification diagnostics for the calibrated SAMBA classic MVP.

Inputs used:
- `model/samba_classic/samba_classic.mod`
- `model/samba_classic/calibration.m`
- `model/samba_classic/steady_state.m`
- `model/samba_classic/shocks.inc`
- `model/samba_classic/observables.inc`

Initial blocker probe: temporary Dynare model with `steady; check; identification;`
appended.

Initial observed result:
- `steady; check;` passed the Blanchard-Kahn check.
- Unstable roots: 26.
- Forward-looking variables: 26.
- Dynare reported that order and rank conditions are verified.
- `identification;` stopped with `info = 3`.
- Identification message: `Current_params` does not solve because Blanchard and Kahn conditions are not satisfied and there is no stable equilibrium.

Mechanical resolution:
- Dynare identification calls `dynare_estimation_init`, which resets the stationary QZ criterion to `0.999999`.
- With `qz_criterium=0.999999`, the model fails the order condition; with the Gate 3 check criterion it passes with 26 unstable roots and 26 forward-looking variables.
- Dynare's documented `diffuse_filter` / `lik_init=3` path is for nonstationary cases.
- A temporary WBS-066 probe using `options_.qz_criterium=1.000001; identification(diffuse_filter, no_identification_strength, no_identification_moments, no_identification_minimal, no_identification_spectrum);` completed with exit code 0.

Completed diagnostic result:
- Dynare tested all current stderr and model parameter values.
- Reduced-form identification rank diagnostic completed.
- The rank of Tau, the Jacobian of steady state and reduced-form solution matrices, is deficient.
- Dynare reports the following entries as not identified.
- Nonidentified shock standard deviations: `SE_pi_target`, `SE_y_gap`, `SE_q_f`, `SE_q_g`, `SE_q_i`, `SE_q_m`, `SE_q_x_star`, `SE_q_d`, `SE_y_d`, `SE_r_k`, `SE_mc`, `SE_mc_x`, `SE_m_c`, `SE_m_i`, `SE_m_x`, `SE_m`, `SE_x`.
- Nonidentified model parameters: `phi_pi`, `phi_y`, `psi_nfa`, `external_debt_lom_adjustment`, `pi_target_gross_ss`, `lambda_g`, `lambda_i`, `lambda_f`.
- Full moments/spectrum/minimal diagnostics remain inappropriate for this WBS without additional treatment because the full diffuse run reports NaNs in theoretical moments and more shocks than observables for Komunjer-Ng.

Interpretation: WBS-066 local identification diagnostics are complete. WBS-067 must classify and treat the nonidentified parameters before priors or estimation.

Forbidden artifacts not created:
- no priors
- no posterior outputs
- no Bayesian estimation
- no backtesting outputs
- no Redux files
- no sovereign-extension files
