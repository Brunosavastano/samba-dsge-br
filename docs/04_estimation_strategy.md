---
status: blocked_wbs066_identification_solve
wbs: WBS-066
gate: Gate 4 preparation
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

Next safe task: diagnose the WBS-066 identification solve mismatch. Do not
start WBS-067, priors, estimation, posterior analysis, backtesting, Redux, or
sovereign extension while WBS-066 remains blocked.

## WBS-066 Attempted Result

WBS-066 local identification diagnostics were attempted against the existing
calibrated SAMBA classic MVP. A temporary Dynare probe with `steady; check;`
followed by `identification;` reported that the standalone model check passed:
26 eigenvalues were larger than one for 26 forward-looking variables, and the
order and rank conditions were verified.

The Dynare `identification;` command then stopped with `info = 3`, reporting
that `Current_params` does not solve because Blanchard and Kahn conditions are
not satisfied and there is no stable equilibrium. This is recorded as
`BLOCKED_WBS066_IDENTIFICATION_SOLVE`.

The attempt did not create priors, posterior outputs, backtesting outputs,
estimation artifacts, Redux files, or sovereign-extension files. The diagnostic
record is `outputs/identification/wbs066_identification_diagnostics.md`.
