---
status: wbs068_priors_table_completed
wbs: WBS-068
gate: Gate 5a preparation
identification_run_created: true
identification_outputs_created: true
priors_table_created: true
priors_created: false
estimation_started: false
posterior_created: false
---

# Identification Strategy

This document defines the WBS-065 protocol for local identification of the
calibrated SAMBA classic MVP. It does not run identification, create priors,
start estimation, or approve posterior analysis.

## Scope

Model scope: calibrated SAMBA classic MVP after Gate 3.

Inputs for the future WBS-066 identification run:
- `model/samba_classic/samba_classic.mod`
- `model/samba_classic/calibration.m`
- `model/samba_classic/steady_state.m`
- `model/samba_classic/shocks.inc`
- `model/samba_classic/observables.inc`
- `docs/03_calibration_notes.md`
- `docs/01_equation_registry.md`
- `docs/wbs064_mvp_calibrated_report.md`

Forbidden in WBS-065:
- `outputs/identification/`
- `model/samba_classic/priors.inc`
- posterior outputs
- backtesting outputs
- Bayesian estimation
- Redux
- sovereign extension

## Identification Method

The future WBS-066 task must use local identification diagnostics for the
calibrated model, following the Iskrev/Dynare identification gate referenced in
`docs/08_implementation_plan.md`.

Minimum future diagnostics:
- local identification status for each candidate parameter;
- weak or collinear parameter flags;
- rank or singularity diagnostics reported by the identification routine;
- model and runtime metadata;
- no posterior or MH output.

## Candidate Parameter Policy

WBS-066 must classify only parameters already present in the calibrated MVP and
documented in `docs/03_calibration_notes.md`. It must not invent parameters,
priors, bounds, source IDs, equations, or results.

Parameters may be classified later as:
- locally_identified
- weak_or_collinear
- fixed_at_sourced_calibration
- requires_prior_after_wbs068
- requires_restriction_or_reparameterization
- not_required_for_mvp
- requires_human_review

## Pass Criteria For Gate 4 Preparation

WBS-066 passes only if identification diagnostics are run and every candidate
parameter has a recorded status. WBS-067 must then decide how to handle any
weak or collinear parameters before priors or estimation can start.

## Stop Conditions

Stop and do not proceed to priors or estimation if:
- Dynare identification cannot run;
- identification reports weak, collinear, or unidentified parameters without a
  WBS-067 treatment decision;
- any candidate parameter is missing from calibration notes;
- any prior or posterior output would be needed to complete the task.

## Next Task

Next safe task: WBS-069, translate the approved WBS-068 prior rows to
`model/samba_classic/priors.inc`. Do not start estimation, create posterior
outputs, run backtesting, Redux, or sovereign extension before the relevant
later WBS.

## WBS-066 Completed Result

WBS-066 local identification diagnostics were attempted against the existing
calibrated SAMBA classic MVP. A temporary Dynare probe with `steady; check;`
followed by `identification;` reported that the standalone model check passed:
26 eigenvalues were larger than one for 26 forward-looking variables, and the
order and rank conditions were verified.

The Dynare `identification;` command then stopped with `info = 3`, reporting
that `Current_params` does not solve because Blanchard and Kahn conditions are
not satisfied and there is no stable equilibrium. This is recorded as
the initial WBS-066 solve mismatch.

The mismatch was mechanical: Dynare identification uses the estimation
initializer, which resets the stationary QZ criterion to `0.999999`. A
temporary diagnostic using the documented nonstationary path
`diffuse_filter`/`lik_init=3`, `qz_criterium=1.000001`, and reduced-form
identification completed with exit code 0.

The completed diagnostic reports a deficient rank of Tau and identifies the
shock standard deviations and model parameters requiring WBS-067 treatment in
`outputs/identification/wbs066_identification_diagnostics.md`.

The attempt did not create priors, posterior outputs, backtesting outputs,
estimation artifacts, Redux files, or sovereign-extension files. The diagnostic
record is `outputs/identification/wbs066_identification_diagnostics.md`.

## WBS-067 Parameter Treatment Decisions

WBS-067 classifies every entry reported as not identified by the WBS-066
reduced-form diagnostic. These decisions do not create priors and do not start
estimation. Rows marked `fixed_at_sourced_calibration` remain fixed at the
documented WBS-055/WBS-057 values for the MVP unless a later WBS provides an
approved source-backed prior or reparameterization.

```csv
diagnostic_entry,entry_type,wbs067_decision,treatment,next_allowed_wbs,source_basis
SE_pi_target,shock_stderr,not_required_for_mvp,Keep target shock off; pi_target remains deterministic/exogenous in the calibrated MVP,WBS-068,docs/03_calibration_notes.md eps_pi_target off
SE_y_gap,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced shock or measurement treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_q_f,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_q_g,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_q_i,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_q_m,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_q_x_star,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_q_d,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_y_d,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_r_k,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_mc,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_mc_x,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_m_c,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_m_i,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_m_x,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_m,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
SE_x,shock_stderr,requires_restriction_or_reparameterization,Exclude from priors; keep as restricted exogenous handle until a sourced stochastic treatment is approved,WBS-068,outputs/identification/wbs066_identification_diagnostics.md
phi_pi,model_parameter,fixed_at_sourced_calibration,Keep fixed at sourced WP239 posterior-mean MVP assignment unless later source-backed estimation treatment is approved,WBS-068,docs/03_calibration_notes.md and model/samba_classic/calibration.m
phi_y,model_parameter,fixed_at_sourced_calibration,Keep fixed at sourced WP239 posterior-mean MVP assignment unless later source-backed estimation treatment is approved,WBS-068,docs/03_calibration_notes.md and model/samba_classic/calibration.m
psi_nfa,model_parameter,not_required_for_mvp,Exclude from priors while unused by the current Dynare model; do not estimate until a source-backed model equation uses it,WBS-068,Dynare preprocessor unused-parameter warning and docs/03_calibration_notes.md
external_debt_lom_adjustment,model_parameter,not_required_for_mvp,Exclude from priors while unused by the current Dynare model; do not estimate until a source-backed equation uses it,WBS-068,Dynare preprocessor unused-parameter warning and docs/03_calibration_notes.md
pi_target_gross_ss,model_parameter,not_required_for_mvp,Exclude from priors while unused by the current Dynare model; do not estimate until a source-backed equation uses it,WBS-068,Dynare preprocessor unused-parameter warning and docs/03_calibration_notes.md
lambda_g,model_parameter,fixed_at_sourced_calibration,Keep fixed at sourced WP239 formula-derived MVP assignment unless later source-backed estimation treatment is approved,WBS-068,docs/03_calibration_notes.md and model/samba_classic/calibration.m
lambda_i,model_parameter,fixed_at_sourced_calibration,Keep fixed at sourced WP239 formula-derived MVP assignment unless later source-backed estimation treatment is approved,WBS-068,docs/03_calibration_notes.md and model/samba_classic/calibration.m
lambda_f,model_parameter,fixed_at_sourced_calibration,Keep fixed at sourced WP239 formula-derived MVP assignment unless later source-backed estimation treatment is approved,WBS-068,docs/03_calibration_notes.md and model/samba_classic/calibration.m
```

WBS-067 pass condition: every WBS-066 nonidentified entry has a treatment
decision, and none is left as `requires_human_review`. WBS-068 may prepare a
source-backed priors table, but it must not create `priors.inc` or start
estimation.

## WBS-068 Source-Backed Priors Table

WBS-068 records priors only where WP239 Table 3 explicitly reports a prior
distribution, mean, and standard deviation. These rows are documentation only:
no `priors.inc`, posterior output, estimation run, Redux file, or sovereign
extension is created here.

Rows excluded by WBS-067 remain excluded from the WBS-069 `priors.inc` until a
later source-backed treatment is approved. In particular, `phi_pi`, `phi_y`,
`lambda_g`, `lambda_i`, and `lambda_f` remain fixed at sourced calibration;
`psi_nfa`, `external_debt_lom_adjustment`, `pi_target_gross_ss`, and the
restricted auxiliary stderr entries remain out of the prior set.

```csv
prior_id,scope,canonical_name,wp239_symbol,prior_distribution,prior_mean,prior_sd,source,source_location,wbs067_status,eligible_for_wbs069_priors_inc,rationale
PRIOR-001,model_parameter,rho_r,gamma_R,Beta,0.60,0.15,BCB_WP239,Table 3 Taylor rule PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-002,model_parameter,rho_risk,rho_Bstar,Beta,0.50,0.25,BCB_WP239,Table 3 autoregressive shocks PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-003,model_parameter,rho_sp_target,rho_Sbar,Beta,0.50,0.25,BCB_WP239,Table 3 autoregressive shocks PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-004,model_parameter,phi_b,phi_B,Inv-Gamma,0.05,0.15,BCB_WP239,Table 3 fiscal rule PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-005,model_parameter,alpha_a_fx,vartheta_A_1,Beta,0.05,0.03,BCB_WP239,Table 3 administered price rule PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-006,model_parameter,alpha_a_mc,vartheta_A_2,Beta,0.20,0.05,BCB_WP239,Table 3 administered price rule PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-007,model_parameter,rho_admin,rho_A,Beta,0.50,0.25,BCB_WP239,Table 3 autoregressive shocks PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-008,model_parameter,rho_z_c,rho_C,Beta,0.50,0.25,BCB_WP239,Table 3 autoregressive shocks PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-009,model_parameter,rho_z_z,rho_Z,Beta,0.50,0.25,BCB_WP239,Table 3 autoregressive shocks PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-010,model_parameter,rho_z_i,rho_I,Beta,0.50,0.25,BCB_WP239,Table 3 autoregressive shocks PDF page 98 printed page 97,identified_candidate,true,Not flagged as nonidentified by WBS-066 and WP239 reports prior hyperparameters.
PRIOR-011,shock_stderr,stderr_risk_dom,epsilon_B,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-012,shock_stderr,stderr_z_i,epsilon_I,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-013,shock_stderr,stderr_z_c,epsilon_C,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-014,shock_stderr,stderr_eps_admin,epsilon_A,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-015,shock_stderr,stderr_z_p,epsilon_P,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-016,shock_stderr,stderr_pi,epsilon_PiC,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-017,shock_stderr,stderr_z_w,epsilon_W,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-018,shock_stderr,stderr_z_z,epsilon_Z,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-019,shock_stderr,stderr_z_q,epsilon_Q,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-020,shock_stderr,stderr_eps_risk,epsilon_Bstar,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-021,shock_stderr,stderr_z_g,epsilon_G,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-022,shock_stderr,stderr_eps_tax,epsilon_T,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-023,shock_stderr,stderr_eps_sp_target,epsilon_Sbar,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-024,shock_stderr,stderr_eps_monetary,epsilon_R,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-025,shock_stderr,stderr_z_px,epsilon_Pstar,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-026,shock_stderr,stderr_pi_star,epsilon_Pistar,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-027,shock_stderr,stderr_r_star,epsilon_Rstar,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
PRIOR-028,shock_stderr,stderr_q_m_star,epsilon_QMstar,Inv-Gamma,1.0,inf,BCB_WP239,Table 3 exogenous shocks PDF page 99 printed page 98,identified_candidate,true,Current WBS-058 shock has WP239 prior hyperparameters and was not excluded by WBS-067.
```

WBS-068 pass condition: every row eligible for WBS-069 has an explicit WP239
prior distribution, mean, standard deviation, source location, and WBS-067
rationale. Estimation remains blocked until later WBS steps.
