# Calibration Notes - samba-dsge-br

---
status: calibration_source_taxonomy_ready
wbs: WBS-055
gate_dependency: Gate 2b
calibration_values_approved: true
steady_state_values_approved: false
priors_approved: false
dynare_allowed: false
model_files_allowed: calibration_m_only
no_parameter_value_invention: true
source_of_truth: docs/01_equation_registry.md
---

## Scope

These notes prepare the calibrated SAMBA classic MVP for later implementation. They approve only source-tracked WBS-055 numeric baseline assignments marked `usable_in_mvp_calibration_m: true`; they do not approve steady-state values beyond sourced entries, priors, equations, Dynare code, MATLAB or Octave code, or model output.

WBS-053 created the calibration rationale scaffold tied to the approved Gate 2b equation registry. WBS-055 adds source-tracked baseline assignments for the current MVP-required parameters only.

## Calibration Policy

- Do not invent parameter values, steady-state values, shock standard deviations, priors, equations, or results.
- Use `docs/01_equation_registry.md` as the registry source for variables, parameters, shocks, and implementation blockers.
- Keep `eps_pi_target` disabled in the calibrated MVP; `pi_target` remains an exogenous or deterministic series.
- Keep `.mod`, Dynare execution, MATLAB, and Octave model implementation blocked until the next approved model WBS. WBS-055 source taxonomy now permits a later `calibration.m` implementation using only rows marked usable.
- Treat this file as a checklist for future calibration work, not as calibrated model content.

## Parameter Rationale Scaffold

| Block | Registry anchors | Calibration rationale required later | Current status |
|---|---|---|---|
| Monetary policy | `rho_r`, `phi_pi`, `phi_y`, `r_ss` | Interest-rate smoothing, inflation response, output-gap response, and policy-rate steady state must be sourced and documented before use. | pending values |
| External closure | `psi_nfa`, `nfa_ss`, `rho_risk` | Debt-elastic risk premium and risk AR(1) persistence must be calibrated without replacing the NFA closure with a pure risk shock. | pending values |
| Fiscal rule | `rho_sp_target`, `phi_b` | Primary-surplus target persistence and debt/GDP feedback must use WP239 point estimates. Legacy `phi_y_sp` and `sp_ss` are not required by WP239 C.31. | source taxonomy ready |
| Administered prices | `rho_admin`, `alpha_a_fx`, `alpha_a_mc` | Administered-price persistence, FX coefficient, and marginal-cost coefficient must use WP239 point estimates. Legacy target/import pass-through terms are not required by the WP239 classic MVP. | source taxonomy ready |
| Households | `habit`, `lambda`, `q_k`, `wn` | Habit, marginal utility, Tobins Q, and real-wage calibration must follow registry locators and not be inferred from memory. | pending values |
| Firms | `mc`, `m_int`, `q_k` | Marginal cost, imported intermediate input, and investment/Q terms require source-linked calibration and steady-state consistency. | pending values |
| Aggregation | `y_gap`, `y_pot`, `nfa`, `m_int`, `pi_target`, `sp_target`, `risk` | Structural variables must map to measurement and steady-state notes before model implementation. | pending values |

## WBS-055 calibration source tracking

Status: `WBS-055_READY_FOR_CALIBRATION_M`

The rows below track all MVP-required parameters currently identified from actual parameter names in `docs/01_equation_registry.md`. Placeholder entries such as `source_located_parameters_pending_calibration`, `source_located_weights_pending_calibration`, `measurement_transform_pending_gate1b`, and `std_pending_calibration` are not treated as parameter names.

Official reference checked: BCB WP239, local file `docs/references/bcb_wp239_samba.pdf`, SHA256 `8EC1FCF4CC37CEE968C4BF8D23D92DBE537F0401A25CA509BEFA84D8E0C1325E`.

Posterior means below are allowed as MVP baseline assignments only because the point values are explicitly reported in WP239 Table 3. They must be labeled as posterior means, not as Table 2 calibrated values.

| parameter | canonical_project_name | aliases | block | role | value | source | source_location | status | usable_in_mvp_calibration_m | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| rho_r | rho_r | gamma_R | MON | Taylor-rule interest-rate smoothing | 0.79 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, Taylor rule row | sourced_from_samba_posterior_mean | true | Use as MVP baseline assignment from posterior mean, not as a Table 2 calibrated value. |
| phi_pi | phi_pi | gamma_Pi | MON | Taylor-rule inflation response | 2.43 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, Taylor rule row | sourced_from_samba_posterior_mean | true | Use as MVP baseline assignment from posterior mean, not as a Table 2 calibrated value. |
| phi_y | phi_y | gamma_Y | MON | Taylor-rule output-gap response | 0.16 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, Taylor rule row | sourced_from_samba_posterior_mean | true | Use as MVP baseline assignment from posterior mean, not as a Table 2 calibrated value. |
| r_ss | r_ss | R_bar | MON | Policy-rate steady-state term | 1.0314 | BCB_WP239 | Table 2 calibrated parameters, PDF page 96 / printed page 95, domestic nominal interest rate | sourced_from_samba_calibration | true | Calibrated steady-state quarterly gross nominal interest rate. |
| psi_nfa | psi_nfa | varphi_B_star | EXT | NFA/debt-elastic risk-premium sensitivity | 0.02 | BCB_WP239 | Table 3 estimated parameters, PDF page 97 / printed page 96, risk premium NFA coefficient | sourced_from_samba_posterior_mean | true | Use as MVP baseline assignment from posterior mean, not as a Table 2 calibrated value. |
| nfa_ss | nfa_ss | B_star_y | EXT | NFA steady-state anchor | -0.68 | BCB_WP239 | Table 2 calibrated parameters, PDF page 96 / printed page 95, net foreign assets-to-GDP ratio | sourced_from_samba_calibration | true | Calibrated quarterly-GDP NFA ratio. |
| rho_risk | rho_risk | rho_B_star | EXT | Risk-premium AR(1) persistence | 0.73 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, country risk premium row; Appendix C.6 C.50, PDF page 92 / printed page 91 | sourced_from_samba_posterior_mean | true | Country risk premium AR(1) posterior mean. |
| rho_sp_target | rho_sp_target | rho_S | FISC | Primary-surplus target persistence | 0.76 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, autoregressive shocks primary surplus row; Appendix C.3 C.31, PDF page 89 / printed page 88 | sourced_from_samba_posterior_mean | true | WP239 C.31 uses rho_S on the target for the primary surplus-to-GDP ratio. |
| phi_b | phi_b | phi_B | FISC | Debt/GDP feedback in fiscal target rule | 0.02 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, fiscal rule row | sourced_from_samba_posterior_mean | true | Government debt coefficient posterior mean. |
| phi_y_sp | phi_y_sp | deprecated | FISC | Legacy output-gap feedback in fiscal target rule |  |  |  | not_required_for_mvp | false | WP239 C.31 has no output-gap term in the primary-surplus target rule; registry removes it from the classic MVP. |
| sp_ss | sp_ss | deprecated | FISC | Legacy primary-surplus target steady-state term |  |  |  | not_required_for_mvp | false | WP239 C.31 is log-linear and has no intercept or steady-state target parameter to calibrate for WBS-055. |
| rho_a | rho_admin | rho_a deprecated; rho_A | ADMIN | Deprecated duplicate administered-price persistence name |  |  |  | not_required_for_mvp | false | Canonical project name is rho_admin, sourced from WP239 rho_A. |
| alpha_a_target | alpha_a_target | deferred extension | ADMIN | Inflation-target pass-through in administered prices |  |  |  | not_required_for_mvp | false | No WP239 target pass-through coefficient was found; excluded from the classic MVP calibration taxonomy. |
| alpha_a_fx | alpha_a_fx | vartheta_A_1 | ADMIN | FX coefficient in administered price rule | 0.05 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, administered price rule row | sourced_from_samba_posterior_mean | true | Use as MVP baseline assignment from posterior mean, not as a Table 2 calibrated value. |
| alpha_a_m | alpha_a_mc | alpha_a_m deprecated | ADMIN | Legacy imported-inflation pass-through in administered prices |  |  |  | not_required_for_mvp | false | WP239 Table 3 has a marginal-cost coefficient, not an imported-inflation coefficient. |
| alpha_a_mc | alpha_a_mc | vartheta_A_2 | ADMIN | Marginal-cost coefficient in administered price rule | 0.20 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, administered price rule row | sourced_from_samba_posterior_mean | true | Canonical replacement for the legacy alpha_a_m imported-inflation mapping. |
| rho_admin | rho_admin | rho_A | ADMIN | Administered-price shock persistence | 0.37 | BCB_WP239 | Table 3 estimated parameters, PDF page 98 / printed page 97, administered prices row; Appendix C.6 C.58, PDF page 92 / printed page 91 | sourced_from_samba_posterior_mean | true | Canonical administered-price AR(1) persistence for the classic MVP. |

Naming blockers are resolved for WBS-055: legacy `rho_a`, `phi_y_sp`, `sp_ss`, `alpha_a_target`, and `alpha_a_m` are tracked as not required for the classic WP239 MVP, while `rho_admin` and `alpha_a_mc` are the canonical sourced names.

## Shock Standard Deviation Scaffold

The registry declares shock names, but shock standard deviations remain pending calibration. This includes `eps_monetary`, `eps_fiscal_g`, `eps_sp_target`, `eps_tax`, `eps_tfp`, `eps_pref`, `eps_investment`, `eps_price_free`, `eps_admin`, `eps_wage`, `eps_import_price`, `eps_risk`, `eps_foreign_y`, `eps_foreign_r`, and `eps_foreign_pi`.

`eps_pi_target` is documented only as a future-phase shock and remains off in the calibrated MVP.

## Steady-State Scaffold

Future steady-state notes must cover at least `y`, `c`, `i`, `g`, `x`, `m`, `q`, `r`, `pi`, `nfa`, `sp`, `b`, `y_gap`, `y_pot`, `pi_target`, `sp_target`, `risk`, `mc`, `q_k`, `wn`, `lambda`, and `m_int`.

Only WBS-055 sourced entries such as `r_ss` and `nfa_ss` are approved for the next `calibration.m` task. The broader steady-state system remains pending.

## Before Model Implementation

- Each calibrated parameter must have a source or documented rationale.
- Each shock standard deviation must link to a registry shock and a calibration note.
- Each steady-state object must be checked against the registry variables and future model residual tests.
- Measurement equations remain governed by the data dictionary and equation registry.
- Runtime verification must remain documented before any Dynare execution.
