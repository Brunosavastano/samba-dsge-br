# Calibration Notes - samba-dsge-br

---
status: calibration_notes_no_values
wbs: WBS-053
gate_dependency: Gate 2b
calibration_values_approved: false
steady_state_values_approved: false
priors_approved: false
dynare_allowed: false
model_files_allowed: false
no_parameter_value_invention: true
source_of_truth: docs/01_equation_registry.md
---

## Scope

These notes prepare the calibrated SAMBA classic MVP for later implementation. They do not approve numeric parameter values, steady-state values, priors, equations, Dynare code, MATLAB or Octave code, or model output.

WBS-053 is limited to a calibration rationale scaffold tied to the approved Gate 2b equation registry. Every future numeric value must be added in a later WBS with a source, rationale, and validation test.

## Calibration Policy

- Do not invent parameter values, steady-state values, shock standard deviations, priors, equations, or results.
- Use `docs/01_equation_registry.md` as the registry source for variables, parameters, shocks, and implementation blockers.
- Keep `eps_pi_target` disabled in the calibrated MVP; `pi_target` remains an exogenous or deterministic series.
- Keep `model/`, `.mod`, Dynare, MATLAB, and Octave model implementation blocked until the next approved model WBS.
- Treat this file as a checklist for future calibration work, not as calibrated model content.

## Parameter Rationale Scaffold

| Block | Registry anchors | Calibration rationale required later | Current status |
|---|---|---|---|
| Monetary policy | `rho_r`, `phi_pi`, `phi_y`, `r_ss` | Interest-rate smoothing, inflation response, output-gap response, and policy-rate steady state must be sourced and documented before use. | pending values |
| External closure | `psi_nfa`, `nfa_ss`, `rho_risk` | Debt-elastic risk premium and risk AR(1) persistence must be calibrated without replacing the NFA closure with a pure risk shock. | pending values |
| Fiscal rule | `rho_sp_target`, `phi_b`, `phi_y_sp`, `sp_ss` | Primary-surplus target persistence, debt/GDP feedback, output-gap feedback, and surplus target steady state must be justified. | pending values |
| Administered prices | `rho_a`, `alpha_a_target`, `alpha_a_fx`, `alpha_a_m`, `rho_admin` | Own AR(1), target pass-through, FX pass-through, imported-inflation pass-through, and administered-price shock persistence must be separately documented. | pending values |
| Households | `habit`, `lambda`, `q_k`, `wn` | Habit, marginal utility, Tobins Q, and real-wage calibration must follow registry locators and not be inferred from memory. | pending values |
| Firms | `mc`, `m_int`, `q_k` | Marginal cost, imported intermediate input, and investment/Q terms require source-linked calibration and steady-state consistency. | pending values |
| Aggregation | `y_gap`, `y_pot`, `nfa`, `m_int`, `pi_target`, `sp_target`, `risk` | Structural variables must map to measurement and steady-state notes before model implementation. | pending values |

## WBS-055 calibration source tracking

Status: `BLOCKED_CALIBRATION_SOURCES`

The rows below track all MVP-required parameters currently identified from actual parameter names in `docs/01_equation_registry.md`. Placeholder entries such as `source_located_parameters_pending_calibration`, `source_located_weights_pending_calibration`, `measurement_transform_pending_gate1b`, and `std_pending_calibration` are not treated as parameter names.

`source_to_check` is not a confirmed source for a numeric value. It is only the likely project/SAMBA reference location to inspect before sourcing a value.

| parameter | block | role | required_for_file | value | source | source_location | status | source_to_check |
|---|---|---|---|---|---|---|---|---|
| rho_r | MON | Taylor-rule interest-rate smoothing | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-MON-001 and EQ-MON-001 locators |
| phi_pi | MON | Taylor-rule inflation response | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-MON-001 and EQ-MON-001 locators |
| phi_y | MON | Taylor-rule output-gap response | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-MON-001 and EQ-MON-001 locators |
| r_ss | MON | Policy-rate steady-state term | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-MON-001 and EQ-MON-001 locators |
| psi_nfa | EXT | NFA/debt-elastic risk-premium sensitivity | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-EXT-001 and EQ-EXT-001 locators |
| nfa_ss | EXT | NFA steady-state anchor | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-EXT-001 and EQ-EXT-001 locators |
| rho_risk | EXT | Risk-premium AR(1) persistence | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-EXT-001 and EQ-EXT-002 locators |
| rho_sp_target | FISC | Primary-surplus target persistence | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-FISC-001 and EQ-FISC-001 locators |
| phi_b | FISC | Debt/GDP feedback in fiscal target rule | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-FISC-001 and EQ-FISC-001 locators |
| phi_y_sp | FISC | Output-gap feedback in fiscal target rule | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-FISC-001 and EQ-FISC-001 locators |
| sp_ss | FISC | Primary-surplus target steady-state term | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-FISC-001 and EQ-FISC-001 locators |
| rho_a | ADMIN | Administered-price inflation process persistence | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-PRICE-ADMIN-001 and EQ-PRICE-001 locators |
| alpha_a_target | ADMIN | Inflation-target pass-through in administered prices | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-PRICE-ADMIN-001 and EQ-PRICE-001 locators |
| alpha_a_fx | ADMIN | FX pass-through in administered prices | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-PRICE-ADMIN-001 and EQ-PRICE-001 locators |
| alpha_a_m | ADMIN | Imported-inflation pass-through in administered prices | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-PRICE-ADMIN-001 and EQ-PRICE-001 locators |
| rho_admin | ADMIN | Administered-price shock persistence | model/samba_classic/calibration.m |  |  |  | missing_source | BCB_WP239 via LM-PRICE-ADMIN-001 and EQ-PRICE-002 locators |

Naming blocker: `rho_a` and `rho_admin` both relate to administered-price persistence and nearby C.58 locators. They must be verified as distinct parameters or reconciled before `calibration.m` is created.

## Shock Standard Deviation Scaffold

The registry declares shock names, but shock standard deviations remain pending calibration. This includes `eps_monetary`, `eps_fiscal_g`, `eps_sp_target`, `eps_tax`, `eps_tfp`, `eps_pref`, `eps_investment`, `eps_price_free`, `eps_admin`, `eps_wage`, `eps_import_price`, `eps_risk`, `eps_foreign_y`, `eps_foreign_r`, and `eps_foreign_pi`.

`eps_pi_target` is documented only as a future-phase shock and remains off in the calibrated MVP.

## Steady-State Scaffold

Future steady-state notes must cover at least `y`, `c`, `i`, `g`, `x`, `m`, `q`, `r`, `pi`, `nfa`, `sp`, `b`, `y_gap`, `y_pot`, `pi_target`, `sp_target`, `risk`, `mc`, `q_k`, `wn`, `lambda`, and `m_int`.

No steady-state numeric value is approved in WBS-053.

## Before Model Implementation

- Each calibrated parameter must have a source or documented rationale.
- Each shock standard deviation must link to a registry shock and a calibration note.
- Each steady-state object must be checked against the registry variables and future model residual tests.
- Measurement equations remain governed by the data dictionary and equation registry.
- Runtime verification must remain documented before any Dynare execution.
