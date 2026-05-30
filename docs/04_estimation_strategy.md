---
status: wbs067_parameter_classification_completed
wbs: WBS-067
gate: Gate 4 completed
identification_run_created: true
identification_outputs_created: true
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

Next safe task: WBS-068, create a priors table with source and rationale only.
Do not create `priors.inc`, start estimation, create posterior outputs, run
backtesting, Redux, or sovereign extension before the relevant later WBS.

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
