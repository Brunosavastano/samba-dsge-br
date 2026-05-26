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

Official reference checked: BCB WP239, local file `docs/references/bcb_wp239_samba.pdf`, SHA256 `8EC1FCF4CC37CEE968C4BF8D23D92DBE537F0401A25CA509BEFA84D8E0C1325E`.

For rows with status `estimated_not_calibrated`, numeric posterior/prior values may be mentioned in notes as evidence that WP239 estimates the parameter. They are not approved calibration values and must not be copied to `calibration.m`.

| parameter | project_name | samba_name_if_different | block | role | value | source | source_location | status | notes |
|---|---|---|---|---|---|---|---|---|---|
| rho_r | rho_r | gamma_R | MON | Taylor-rule interest-rate smoothing |  | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, Taylor rule row | estimated_not_calibrated | Posterior mean 0.79 found; WP239 treats it as estimated, not calibrated. |
| phi_pi | phi_pi | gamma_Pi | MON | Taylor-rule inflation response |  | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, Taylor rule row | estimated_not_calibrated | Posterior mean 2.43 found; WP239 treats it as estimated, not calibrated. |
| phi_y | phi_y | gamma_Y | MON | Taylor-rule output-gap response |  | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, Taylor rule row | estimated_not_calibrated | Posterior mean 0.16 found; WP239 treats it as estimated, not calibrated. |
| r_ss | r_ss | R_bar | MON | Policy-rate steady-state term | 1.0314 | BCB_WP239 | Table 2 calibrated parameters, PDF page 96 / printed page 95, domestic nominal interest rate | sourced_from_samba | Calibrated steady-state quarterly gross nominal interest rate. |
| psi_nfa | psi_nfa | varphi_B_star | EXT | NFA/debt-elastic risk-premium sensitivity |  | BCB_WP239 | Table 3 estimated parameters, PDF page 97 / printed page 96, risk premium NFA coefficient | estimated_not_calibrated | Posterior mean 0.02 found; WP239 treats it as estimated, not calibrated. |
| nfa_ss | nfa_ss | B_star_y | EXT | NFA steady-state anchor | -0.68 | BCB_WP239 | Table 2 calibrated parameters, PDF page 96 / printed page 95, net foreign assets-to-GDP ratio | sourced_from_samba | Calibrated quarterly-GDP NFA ratio. |
| rho_risk | rho_risk | rho_B_star | EXT | Risk-premium AR(1) persistence |  | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, country risk premium row; Appendix C.6 C.50, PDF page 92 / printed page 91 | estimated_not_calibrated | Posterior mean 0.73 found; WP239 treats it as estimated, not calibrated. |
| rho_sp_target | rho_sp_target | phi_S_bar | FISC | Primary-surplus target persistence |  | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, fiscal rule row | estimated_not_calibrated | Posterior mean 0.41 found for primary surplus target coefficient; WP239 treats it as estimated, not calibrated. |
| phi_b | phi_b | phi_B | FISC | Debt/GDP feedback in fiscal target rule |  | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, fiscal rule row | estimated_not_calibrated | Posterior mean 0.02 found; WP239 treats it as estimated, not calibrated. |
| phi_y_sp | phi_y_sp |  | FISC | Output-gap feedback in fiscal target rule |  |  |  | naming_conflict | WP239 Table 3 has phi_S as primary surplus reaction coefficient with posterior mean 0.49; registry role says output-gap feedback, so mapping is not verified. |
| sp_ss | sp_ss |  | FISC | Primary-surplus target steady-state term |  |  |  | missing_source | Exact calibrated primary-surplus target steady-state value not found in WP239 Table 2 or Table 3 search. |
| rho_a | rho_a |  | ADMIN | Administered-price inflation process persistence |  |  |  | naming_conflict | WP239 C.58 and Table 3 have rho_A for administered-price shock persistence; registry also has rho_admin, so distinctness is unresolved. |
| alpha_a_target | alpha_a_target |  | ADMIN | Inflation-target pass-through in administered prices |  |  |  | missing_source | No exact WP239 administered-price target pass-through coefficient found in the checked calibrated or estimated tables. |
| alpha_a_fx | alpha_a_fx | vartheta_A_1 | ADMIN | FX pass-through in administered prices |  | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, administered price rule row | estimated_not_calibrated | Posterior mean 0.05 found; WP239 treats it as estimated, not calibrated. |
| alpha_a_m | alpha_a_m |  | ADMIN | Imported-inflation pass-through in administered prices |  |  |  | naming_conflict | WP239 Table 3 has vartheta_A_2 as a marginal-cost coefficient with posterior mean 0.20, not an imported-inflation coefficient. |
| rho_admin | rho_admin | rho_A | ADMIN | Administered-price shock persistence |  | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, administered prices row; Appendix C.6 C.58, PDF page 92 / printed page 91 | estimated_not_calibrated | Posterior mean 0.37 found; WP239 treats it as estimated, not calibrated. |

Naming blockers: `rho_a` versus `rho_admin`, `phi_y_sp` versus WP239 `phi_S`, and `alpha_a_m` versus WP239 `vartheta_A_2` must be resolved before `calibration.m` is created.

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
