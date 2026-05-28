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
| theta_admin | theta_admin | theta_A | ADMIN | Fraction/probability of administered-price firms allowed to adjust according to the administered-price rule | 0.25 | BCB_WP239 | Administered-price sector, administered-price rule discussion around C.22-C.23, PDF page 29 / printed page 28 | sourced_from_samba | true | WP239 states theta_A = 1/4 because administered prices are usually allowed to change once a year; do not confuse with CPI weight omega_A. |
| chi_admin | chi_admin | chi_A | ADMIN | Convergence parameter in administered-price rule | 0.8 | BCB_WP239 | Calibrated-parameters discussion, PDF page 49 / printed page 48 | sourced_from_samba | true | Administered-price rule convergence parameter for WBS-057. |

Naming blockers are resolved for WBS-055: legacy `rho_a`, `phi_y_sp`, `sp_ss`, `alpha_a_target`, and `alpha_a_m` are tracked as not required for the classic WP239 MVP, while `rho_admin` and `alpha_a_mc` are the canonical sourced names.

Administered-price CPI weight distinction: `omega_admin` maps to WP239 `omega_A` / `varpi_A`, value `0.3`, sourced from the WP239 calibrated-parameters discussion, PDF page 49 / printed page 48. It is the CPI weight of administered-price inflation and is not `theta_admin`; it is documented as sourced but not required for WBS-057 `calibration.m`.

## WBS-057 formula parameter and weight mappings

Status: `sourced_for_wbs057_formula_mapping`

These mappings are sourced from WP239 Appendix C and Tables 2/3 for equation mapping only. They do not update `model/samba_classic/calibration.m` and are not claimed as final empirical replication.

| mapping_group | project_names_and_values | source_location | used_by | mapping_status |
|---|---|---|---|---|
| expenditure shares | `share_c_y=0.62`; `share_g_y=0.20`; `share_i_y=0.17`; `share_x_y=0.13`; `share_m_y=0.12`; `tax_share_T=0.35`; `share_rule_thumb_c=0.40` | BCB_WP239 Table 2, PDF page 95 / printed page 94 | EQ-FISC-002; EQ-FISC-004; EQ-HH-002; EQ-HH-004; EQ-AGG-001; EQ-AGG-002; EQ-AGG-003 | sourced_for_wbs057_mapping |
| preference and trend parameters | `beta_tilde=0.989`; `eta_labor_inverse_elasticity=1.00`; `gross_bgp_growth=1.009`; `habit_persistence=0.74`; `intertemporal_eos_inverse=1.30` | BCB_WP239 Tables 2/3, PDF pages 95 and 97 / printed pages 94 and 96 | EQ-HH-001; EQ-HH-002; EQ-HH-003; EQ-FIRM-003; EQ-FISC-003 | sourced_for_wbs057_mapping |
| production and elasticity parameters | `eps_wage_eos=3`; `eps_input_c=11`; `eps_input_i=11`; `eps_input_g=11`; `eps_input_x=11`; `eps_imported_goods=11`; `capital_income_share=0.448`; `production_labor_share=0.8`; `capital_depreciation=0.015` | BCB_WP239 Table 2, PDF page 95 / printed page 94 | EQ-HH-003; EQ-FIRM-001; EQ-FIRM-002; EQ-FIRM-003; EQ-FIRM-004 | sourced_for_wbs057_mapping |
| sectoral domestic-cost weights | `domestic_cost_weight_c=0.8418`; `domestic_cost_weight_i=0.79`; `domestic_cost_weight_g=1.00`; `domestic_cost_weight_x=0.9` | BCB_WP239 Table 2, PDF page 95 / printed page 94 | EQ-FIRM-001; EQ-FIRM-002; EQ-FIRM-003; EQ-FIRM-004 | sourced_for_wbs057_mapping |
| external financing shares | `external_financing_share_c=0.5`; `external_financing_share_i=0.5`; `external_financing_share_x=0.5` | BCB_WP239 Table 2, PDF page 95 / printed page 94 | EQ-EXT-003 | sourced_for_wbs057_mapping |
| debt and external steady-state anchors | `nfa_ss=-0.68`; `b_ss=2.00`; `external_debt_lom_adjustment=0.0397`; `domestic_debt_lom_adjustment=0.53`; `pi_target_gross_ss=1.011`; `foreign_inflation_gross_ss=1.0064`; `foreign_rate_gross_ss=1.0074`; `country_risk_gross_ss=1.014` | BCB_WP239 Table 2, PDF page 96 / printed page 95 | EQ-EXT-003; EQ-FISC-003; EQ-AGG-002 | sourced_for_wbs057_mapping |
| imported-input and adjustment parameters | `domestic_imported_eos_c=1.09`; `domestic_imported_eos_i=0.83`; `domestic_imported_eos_x=0.95`; `brazil_exports_row_inputs_eos=0.66`; `investment_adjustment_cost=3.42`; `imports_adjustment_cost_c=0.76`; `imports_adjustment_cost_i=1.97`; `imports_adjustment_cost_x=3.12` | BCB_WP239 Table 3, PDF page 97 / printed page 96 | EQ-FIRM-003; EQ-FIRM-004 | sourced_for_wbs057_mapping |
| nominal rigidity parameters | `calvo_free_price=0.74`; `calvo_government_price=0.47`; `calvo_investment_price=0.65`; `calvo_export_price=0.77`; `calvo_import_price=0.64`; `calvo_wage=0.75`; `free_price_indexation=0.33`; `government_price_indexation=0.49`; `import_price_indexation=0.65`; `investment_price_indexation=0.55`; `export_price_indexation=0.35`; `wage_indexation=0.49` | BCB_WP239 Table 3, PDF page 97 / printed page 96 | EQ-HH-003; EQ-FIRM-002; EQ-FIRM-004 | sourced_for_wbs057_mapping |
| fiscal and auxiliary process parameters | `fiscal_surplus_reaction=0.49`; `fiscal_surplus_target_coeff=0.41`; `tax_rate_persistence=0.80`; `domestic_risk_premium_persistence=0.85`; `risk_premium_investor_aversion_coeff=0.03` | BCB_WP239 Tables 2/3, PDF pages 96 and 98 / printed pages 95 and 97 | EQ-FISC-002; EQ-FISC-004; EQ-HH-001; EQ-FIRM-003 | sourced_for_wbs057_mapping |

## Shock Standard Deviation Scaffold

The registry declares shock names, but shock standard deviations remain pending calibration. This includes `eps_monetary`, `eps_fiscal_g`, `eps_sp_target`, `eps_tax`, `eps_tfp`, `eps_pref`, `eps_investment`, `eps_price_free`, `eps_admin`, `eps_wage`, `eps_import_price`, `eps_risk`, `eps_foreign_y`, `eps_foreign_r`, and `eps_foreign_pi`.

`eps_pi_target` is documented only as a future-phase shock and remains off in the calibrated MVP.

## Steady-State Scaffold

Future steady-state notes must cover at least `y`, `c`, `i`, `g`, `x`, `m`, `q`, `r`, `pi`, `nfa`, `sp`, `b`, `y_gap`, `y_pot`, `pi_target`, `sp_target`, `risk`, `mc`, `q_k`, `wn`, `lambda`, and `m_int`.

Only WBS-055 sourced entries such as `r_ss` and `nfa_ss` are approved for the next `calibration.m` task. The broader steady-state system remains pending.

## Approved MVP steady-state assignments

Status: `WBS-056_READY_FOR_STEADY_STATE_M_BLOCKED_BY_TEST_CONTRACT`

Zero steady states below apply only to log-linear deviation variables and shock states. They do not assign economic levels for debt, NFA, inflation targets, interest rates, or risk premia. Nonzero level anchors must have explicit SAMBA sources.

| variable | value_or_expression | status | source | source_location | rationale | usable_in_steady_state_m |
|---|---|---|---|---|---|---|
| abs | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | docs/00b_modeling_decisions.md TREND-001; registry EQ-AGG-002 log-linear C.37-C.39 | Absorption is represented as a log-linear deviation in the MVP registry. | true |
| b | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | docs/00b_modeling_decisions.md TREND-001; registry EQ-FISC-001 C.31 and EQ-FISC-003 C.34 | Debt/GDP model variable is a log-linear deviation; level is not assigned to `b`. | true |
| b_ss | 2.00 | sourced_from_samba | BCB_WP239 | Table 2 calibrated parameters, PDF page 96 / printed page 95, net government debt-to-GDP ratio | Debt/GDP level anchor is sourced, not inferred. | true |
| c | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-HH-001/EQ-AGG-001 log-linear locators | Consumption is represented as a log-linear deviation. | true |
| c_rt | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-HH-004 | Rule-of-thumb consumption is represented as a log-linear deviation. | true |
| delta_q | 0 | zero_by_loglinear_convention | Gate0 EXT-001; BCB_WP239 | registry EQ-EXT-004 | Exchange-rate change is a deviation/change term; steady-state change is zero. | true |
| g | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-FISC-002/EQ-AGG-001 | Government consumption is represented as a log-linear deviation. | true |
| i | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-HH-001/EQ-FIRM-003/EQ-AGG-001 | Investment is represented as a log-linear deviation. | true |
| k | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-HH-001/EQ-FIRM-001/EQ-FIRM-003 | Capital is represented as a log-linear deviation. | true |
| labor | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-HH-003/EQ-FIRM-001 | Labor is represented as a log-linear deviation. | true |
| labor_rt | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-HH-004 | Rule-of-thumb labor is represented as a log-linear deviation. | true |
| lambda | 0 | zero_by_loglinear_convention | Gate0 STRUCT-001; BCB_WP239 | registry EQ-HH-001/EQ-HH-002 | Marginal utility/multiplier variable is represented as a log-linear deviation. | true |
| m | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-AGG-002/EQ-AGG-003 | Imports are represented as a log-linear deviation. | true |
| m_int | 0 | zero_by_loglinear_convention | Gate0 STRUCT-001; BCB_WP239 | registry EQ-FIRM-004/EQ-AGG-001 | Imported intermediate input is represented as a log-linear deviation. | true |
| mc | 0 | zero_by_loglinear_convention | Gate0 STRUCT-001; BCB_WP239 | registry EQ-FIRM-001/EQ-FIRM-002/EQ-PRICE-001 | Marginal cost is represented as a log-linear deviation. | true |
| nfa | 0 | zero_by_loglinear_convention | Gate0 EXT-001; BCB_WP239 | registry EQ-EXT-001/EQ-EXT-003/EQ-AGG-002 | NFA model variable is a deviation around `nfa_ss`; level is not assigned to `nfa`. | true |
| nx | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-EXT-003/EQ-AGG-002 | Net exports are represented as a log-linear deviation. | true |
| pi | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-FIRM-002 | Inflation variable is represented as a deviation. | true |
| pi_a | 0 | zero_by_loglinear_convention | Gate0 ADMIN-001; BCB_WP239 | registry EQ-PRICE-001/EQ-PRICE-003 | Administered inflation is represented as a deviation/process state. | true |
| pi_target | 0 | zero_by_loglinear_convention | Gate0 TARGET-001; BCB_WP239 | docs/00b_modeling_decisions.md TARGET-001; registry EQ-MON-002 C.29 | Inflation target enters as deterministic/exogenous deviation; no target level is invented. | true |
| pi_y | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-FISC-003/EQ-AGG-003 | GDP-deflator inflation is represented as a deviation. | true |
| q | 0 | zero_by_loglinear_convention | Gate0 EXT-001; BCB_WP239 | registry EQ-EXT-001/EQ-EXT-004/EQ-AGG-002 | Real exchange rate is represented as a log-linear deviation. | true |
| q_k | 0 | zero_by_loglinear_convention | Gate0 STRUCT-001; BCB_WP239 | registry EQ-HH-001/EQ-FIRM-003 | Tobins Q is represented as a log-linear deviation. | true |
| q_y | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-AGG-003 | GDP deflator relative price term is represented as a deviation. | true |
| r_t | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-MON-001 C.28 and EQ-EXT-001 | Policy-rate model variable is represented as a deviation; level is held in `r_ss`. | true |
| r_star | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-EXT-001 | Foreign interest-rate variable is represented as a deviation. | true |
| risk | 0 | zero_by_loglinear_convention | Gate0 EXT-001; BCB_WP239 | registry EQ-EXT-002 C.50 and EQ-SHOCK-013 | Risk-premium shock process is represented as a zero-mean AR(1) deviation. | true |
| sp | 0 | zero_by_loglinear_convention | Gate0 FISC-001; BCB_WP239 | registry EQ-FISC-002 C.30 | Realized primary surplus is represented as a deviation, not a level. | true |
| sp_target | 0 | zero_by_loglinear_convention | Gate0 FISC-001; BCB_WP239 | registry EQ-FISC-001 C.31 and EQ-SHOCK-004 | Primary-surplus target is represented as a deviation. | true |
| tax_rate | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-FISC-004 C.32 and EQ-SHOCK-005 | Tax-rate process is represented as a deviation. | true |
| technology | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-FIRM-001 | Technology enters as a deviation state in the log-linear MVP. | true |
| trend_growth | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-FISC-003/EQ-AGG-004 | Trend-growth term is represented as a deviation from deterministic trend. | true |
| wn | 0 | zero_by_loglinear_convention | Gate0 STRUCT-001; BCB_WP239 | registry EQ-HH-003/EQ-HH-004 | Real wage is represented as a log-linear deviation. | true |
| x | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-AGG-001/EQ-AGG-002/EQ-AGG-003 | Exports are represented as a log-linear deviation. | true |
| y | 0 | zero_by_loglinear_convention | Gate0 TREND-001; BCB_WP239 | registry EQ-FISC-002/EQ-FIRM-001/EQ-AGG-003/EQ-AGG-004 | Output is represented as a log-linear deviation. | true |
| y_gap | 0 | zero_by_loglinear_convention | Gate0 MON-001; Gate0 OBS-001 | docs/00b_modeling_decisions.md MON-001 and OBS-001; registry EQ-MON-001/EQ-AGG-004 | Output gap is a structural gap variable; deterministic steady state is zero. | true |
| y_pot | 0 | zero_by_loglinear_convention | Gate0 STRUCT-001; BCB_WP239 | registry EQ-AGG-004 | Potential output component is represented as a log-linear deviation. | true |

## Before Model Implementation

- Each calibrated parameter must have a source or documented rationale.
- Each shock standard deviation must link to a registry shock and a calibration note.
- Each steady-state object must be checked against the registry variables and future model residual tests.
- Measurement equations remain governed by the data dictionary and equation registry.
- Runtime verification must remain documented before any Dynare execution.
