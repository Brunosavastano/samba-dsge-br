# Equation Registry - samba-dsge-br

**Documento:** `docs/01_equation_registry.md`
**Status:** Gate 2b approved for minimum viable equation registry
**Fonte canonica:** `docs/00a_literature_map.md`
**Criado em:** 2026-05-26

---

## 0. Gate status

```yaml
gate: Gate 2b
wbs: WBS-044
gate_status: approved
gate2b_passed: true
dynare_allowed: false
model_file_allowed: false
dynare_blocker: "Runtime verification and calibration notes are required before model implementation."
model_file_blocker: "No model/ files before calibration notes and the next implementation gate."
source_memory_allowed: false
monetary_block_registered: true
external_block_registered: true
fiscal_block_registered: true
administered_prices_registered: true
household_block_registered: true
firm_block_registered: true
aggregation_block_registered: true
shock_block_registered: true
measurement_draft_registered: true
core_blocks_registered: true
decision_status: approved
approved_by: Bruno
approval_date: 2026-05-26
approval_basis: "Objective Gate 2b checklist authorized by Bruno: core blocks, variables, shocks, parameters, tests, and statuses are versioned and sourced."
registry_version: 0.11.3-wbs057-symbol-mapping
created_at: 2026-05-26
updated_at: 2026-05-26
```

Gate 2b is passed for the minimum viable equation registry. No Dynare, model file, calibration value, dataset, or result is approved by this gate update.

---

## 1. Registry policy

```text
- Do not register equations from memory.
- Every future equation entry must point to `docs/00a_literature_map.md`.
- Equation numbers may be used as locators, but formulas are entered only in the relevant WBS.
- Measurement equations remain draft until dataset generation and observables implementation finalize the measurement transforms.
- Dynare and `model/` files remain blocked until runtime verification and calibration notes are complete.
```

---

## 2. Entry schema

```csv
field,required,description
equation_id,yes,Stable unique ID using EQ-<BLOCK>-###.
block,yes,MON EXT FISC ADMIN HH FIRM AGG SHOCK MEAS or AUX.
title,yes,Short human-readable label; not a formula.
equation_type,yes,structural identity shock_process measurement_draft or auxiliary.
source_map_id,yes,Map row from docs/00a_literature_map.md.
source_reference_id,yes,Primary reference ID such as BCB_WP239.
source_locator,yes,Exact section equation table or figure locator.
variables,yes,Variables used by the equation or none.
parameters,yes,Parameters used by the equation or none.
shocks,yes,Shocks used by the equation or none.
tests,yes,Expected validation tests or none.
status,yes,draft sourced reviewed approved deferred or rejected.
gate,yes,WBS or gate that owns the entry.
notes,no,Short implementation notes.
```

---

## 3. Planned namespaces

```csv
namespace,block,source_map_id,next_wbs,status
EQ-MON,MON,LM-MON-001,WBS-035,registered_minimum_viable
EQ-EXT,EXT,LM-EXT-001,WBS-036,registered_minimum_viable
EQ-FISC,FISC,LM-FISC-001,WBS-037,registered_minimum_viable
EQ-PRICE,ADMIN,LM-PRICE-ADMIN-001,WBS-038,registered_minimum_viable
EQ-HH,HH,LM-HH-001,WBS-039,registered_minimum_viable
EQ-FIRM,FIRM,LM-FIRM-001,WBS-040,registered_minimum_viable
EQ-AGG,AGG,LM-AGG-001,WBS-041,registered_minimum_viable
EQ-SHOCK,SHOCK,LM-SHOCK-001,WBS-042,registered_minimum_viable
EQ-MEAS,MEAS,LM-MEAS-001,WBS-043,draft_registered_after_gate1b
```

---

## 4. Registry entries

WBS-035 through WBS-043 entries are registered.

```csv
equation_id,block,title,equation_type,source_map_id,source_reference_id,source_locator,variables,parameters,shocks,tests,status,gate,notes
EQ-MON-001,MON,Forward-looking Taylor rule,structural,LM-MON-001,BCB_WP239,WP239 Section 2.3.1 PDF pages 33-34; Appendix C.3 PDF page 89; main equation 61; log-linear equation C.28,r_t|r_lag|pi_expected|pi_target|y_gap,rho_r|phi_pi|phi_y|r_ss,eps_monetary,monetary_irf_sign_timing_magnitude_benchmark;smoothing_parameter_present;target_gap_present,sourced,WBS-035,Implements MON-001 contract without Dynare syntax.
EQ-MON-002,MON,Inflation target treatment,auxiliary,LM-MON-001,BCB_WP239,WP239 Section 2.3.1 PDF page 34; main equation 62; Appendix C.3 PDF page 89; log-linear equation C.29,pi_target,none,none,pi_target_explicit;eps_pi_target_absent_in_calibrated_mvp;deterministic_target_series_allowed,sourced,WBS-035,Implements TARGET-001 calibrated MVP treatment.
EQ-MON-003,MON,Monetary policy shock,shock_process,LM-MON-001,BCB_WP239,WP239 Appendix C.6 PDF page 93; shock equation C.60,monetary_policy_shock_state,none_for_mvp_monetary_shock_term,eps_monetary,shock_declared;irf_response_timing_defined;shock_not_used_for_target_changes,sourced,WBS-035,Shock naming remains registry-only until WBS-042 and Dynare remains blocked.
EQ-EXT-001,EXT,UIP with NFA debt-elastic risk premium,structural,LM-EXT-001,BCB_WP239,WP239 Section 2.4 PDF page 38; Section 2.7 PDF pages 41-42; Appendix C.4-C.5 PDF pages 90-91; log-linear equations C.37-C.47,q|delta_q_expected|r_t|pi_expected|r_star|pi_star|nfa|risk,psi_nfa|nfa_ss,risk,external_closure_explicit;nfa_debt_elastic_premium_present;uip_uses_expected_depreciation;sources_located,sourced,WBS-036,Implements EXT-001 baseline closure without Dynare syntax.
EQ-EXT-002,EXT,Risk premium AR1 process,shock_process,LM-EXT-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; risk-premium shock equation C.50,risk|risk_lag,rho_risk,eps_risk,ar1_process_present;eps_risk_declared;not_pure_ar1_closure_without_nfa,sourced,WBS-036,Risk_t is a shock process and not the sole external closure.
EQ-EXT-003,EXT,NFA law of motion locator,identity,LM-EXT-001,BCB_WP239,WP239 Section 2.7 PDF pages 41-42; main equations 78-80; Appendix C.4 PDF page 90; log-linear equations C.37-C.39,nfa|nx|external_loans|q|imports|exports,source_located_parameters_pending_calibration,none,nfa_state_declared;external_balance_identity_located;calibration_notes_required_before_dynare,sourced,WBS-036,Parameters are not invented; calibration remains future work.
EQ-EXT-004,EXT,Real exchange rate sign convention,auxiliary,LM-EXT-001,BCB_WP239,WP239 Section 2.4 PDF page 38; Appendix C.4-C.5 PDF pages 90-91,q|delta_q,none,none,q_up_means_brl_real_depreciation;delta_q_used_in_uip;exchange_rate_measurement_deferred_to_data_dictionary,sourced,WBS-036,Project convention follows EXT-001 approval.
EQ-FISC-001,FISC,Primary surplus target with debt feedback,structural,LM-FISC-001,BCB_WP239,WP239 Section 2.3 Government PDF pages 33-36; Appendix C.3 PDF page 89; main equation 64; log-linear equation C.31,sp_target|sp_target_lag|b|b_ss,rho_sp_target|phi_b,eps_sp_target,sp_target_separate_from_sp;debt_gdp_feedback_present;phi_b_positive_required;wp239_c31_no_output_gap_feedback;sp_ss_not_required_for_loglinear_target,sourced,WBS-037,Implements WP239 C.31 target rule. Legacy phi_y_sp and sp_ss are tracked as not required for the classic log-linear MVP.
EQ-FISC-002,FISC,Realized primary surplus and government spending instrument,structural,LM-FISC-001,BCB_WP239,WP239 Section 2.3 Government PDF pages 33-36; Appendix C.3 PDF page 89; main equations 63 and 65-68; log-linear equations C.30 and C.33,sp|sp_lag|sp_target|g|tax_rate|y,source_located_parameters_pending_calibration,none,sp_realized_distinct_from_sp_target;government_consumption_instrument_located;source_parameters_not_invented,sourced,WBS-037,Government spending is the fiscal instrument implied by the primary-surplus rule.
EQ-FISC-003,FISC,Public debt to GDP law of motion,identity,LM-FISC-001,BCB_WP239,WP239 Section 2.3 Government PDF pages 33-36; Appendix C.3 PDF page 89; log-linear equation C.34,b|b_lag|r_t|sp|y|pi_y|trend_growth,source_located_parameters_pending_calibration,none,b_represents_public_debt_gdp;debt_identity_located;identity_required_before_dynare,sourced,WBS-037,Debt identity must be reviewed before any model file is created.
EQ-FISC-004,FISC,Fiscal auxiliary tax and primary surplus locators,auxiliary,LM-FISC-001,BCB_WP239,WP239 Section 2.3 Government PDF pages 35-36; Appendix C.3 PDF page 89; main equations 65-68; log-linear equation C.32,tax_rate|nominal_tax_revenue|nominal_primary_surplus,source_located_parameters_pending_calibration,none,tax_auxiliary_located;no_regime_2016_2023_in_mvp;calibration_notes_required_before_dynare,sourced,WBS-037,Auxiliary fiscal identities are source-located but not calibrated here.
EQ-PRICE-001,ADMIN,Administered prices WP239 shock and price-rule parameters,structural,LM-PRICE-ADMIN-001,BCB_WP239,WP239 Appendix C.2 PDF page 88; administered price inflation equation C.22 and administered price rule C.23; Appendix C.6 PDF page 92 shock equation C.58; Table 3 PDF page 98 administered price rule parameters,pi_a|admin_price_shock_state|delta_q|mc,rho_admin|alpha_a_fx|alpha_a_mc|theta_admin|chi_admin,eps_admin,admin_process_own_equation;admin_shock_ar1_present;fx_coefficient_sourced;marginal_cost_coefficient_sourced;theta_admin_sourced;chi_admin_sourced;target_and_imported_pass_through_not_required_for_wp239_mvp;eps_admin_declared;not_generic_shock,sourced,WBS-038,Canonical persistence is rho_admin. Legacy rho_a and alpha_a_m are tracked as aliases or not required for the classic WP239 MVP. theta_admin maps to WP239 theta_A and is distinct from CPI weight omega_admin.
EQ-PRICE-002,ADMIN,Administered prices shock locator,shock_process,LM-PRICE-ADMIN-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; administered prices shock equation C.58,admin_price_shock_state|admin_price_shock_lag,rho_admin,eps_admin,admin_shock_source_located;shock_not_substitute_for_full_process;rho_admin_canonical_name;sourced_by_wbs055_taxonomy,sourced,WBS-038,Source locator for the WP239 administered-price shock process.
EQ-PRICE-003,ADMIN,Administered prices observable locator,measurement_draft,LM-PRICE-ADMIN-001,BCB_WP239,WP239 Table 1 PDF page 94,pi_a,none,none,table1_locator_present;measurement_deferred_to_gate1b;no_source_id_invention,sourced,WBS-038,Data source IDs and exact measurement equation remain blocked until Gate 1b.
EQ-HH-001,HH,Optimizing household intertemporal conditions,structural,LM-HH-001,BCB_WP239,WP239 Section 2.1.1 Optimizing Households PDF pages 11-17; Appendix C.1 PDF pages 84-86; main equations 1-15; log-linear equations C.1-C.10,c|c_lag|lambda|r_t|pi_expected|q_k|i|k,source_located_parameters_pending_calibration,preference_shock,lambda_mapped;q_k_mapped;euler_locator_present;parameters_not_calibrated_here,sourced,WBS-039,No formula is copied; exact calibration remains future work.
EQ-HH-002,HH,Consumption habit contract,structural,LM-HH-001,BCB_WP239,WP239 Section 2.1.1 Optimizing Households PDF pages 11-17; Appendix C.1 PDF pages 84-86,c|c_lag|habit_state|lambda,source_located_parameters_pending_calibration,preference_shock,consumption_habit_locator_present;habit_state_mapped;measurement_deferred_to_gate1b,sourced,WBS-039,Consumption-habit implementation details remain registry-to-Dynare work after Gate 2b.
EQ-HH-003,HH,Labor supply and real wage contract,structural,LM-HH-001,BCB_WP239,WP239 Section 2.1 Households PDF page 10; Section 2.1.1 PDF pages 11-17; Appendix C.1 PDF pages 84-86,labor|wn|lambda|wage_markup,source_located_parameters_pending_calibration,wage_markup_shock,wn_mapped;labor_supply_locator_present;variables_mapped,sourced,WBS-039,Nominal wage setting details remain source-located for later registry entries if needed.
EQ-HH-004,HH,Rule-of-thumb household contract,structural,LM-HH-001,BCB_WP239,WP239 Section 2.1.2 Rule-of-Thumb Households PDF page 18; Appendix C.1 PDF pages 84-86,c_rt|labor_rt|wn|tax_rate|transfers,source_located_parameters_pending_calibration,none,rule_of_thumb_locator_present;consumption_labor_variables_mapped;parameters_not_invented,sourced,WBS-039,Rule-of-thumb household variables are mapped without choosing calibration values.
EQ-FIRM-001,FIRM,Production and marginal cost contract,structural,LM-FIRM-001,BCB_WP239,WP239 Section 2.2 Firms PDF pages 18-32; Appendix C.2 PDF pages 86-88; main equations 22-60; log-linear equations C.11-C.27,y|mc|k|labor|m_int|technology,source_located_parameters_pending_calibration,technology_shock,mc_mapped;m_int_mapped;production_locator_present;parameters_not_calibrated_here,sourced,WBS-040,No formula is copied and calibration remains future work.
EQ-FIRM-002,FIRM,Price Phillips curve and markup contract,structural,LM-FIRM-001,BCB_WP239,WP239 Section 2.2 Firms PDF pages 18-32; Appendix C.2 PDF pages 86-88; main equations 22-60; log-linear equations C.11-C.27,pi|mc|price_markup|relative_price,source_located_parameters_pending_calibration,price_markup_shock,phillips_locator_present;mc_used_in_pricing;price_markup_shock_mapped;sources_located,sourced,WBS-040,Free-price implementation details remain registry-to-Dynare work after Gate 2b.
EQ-FIRM-003,FIRM,Investment and Tobins Q contract,structural,LM-FIRM-001,BCB_WP239,WP239 Section 2.2 Firms PDF pages 18-32; Appendix C.2 PDF pages 86-88; main equations 22-60; log-linear equations C.11-C.27,i|k|q_k|investment_adjustment_state,source_located_parameters_pending_calibration,investment_shock,q_k_mapped;investment_locator_present;capital_accumulation_locator_present;parameters_not_invented,sourced,WBS-040,Tobins Q and investment frictions are source-located only.
EQ-FIRM-004,FIRM,Imported intermediate inputs contract,structural,LM-FIRM-001,BCB_WP239,WP239 Section 2.2 Firms PDF pages 18-32; Appendix C.2 PDF pages 86-88; main equations 22-60; log-linear equations C.11-C.27,m_int|import_price|domestic_input|sectoral_output,source_located_parameters_pending_calibration,import_price_shock,m_int_mapped;imported_input_locator_present;external_linkage_mapped;sources_located,sourced,WBS-040,Intermediate imports are mapped without data extraction or source_id invention.
EQ-AGG-001,AGG,Final goods market clearing,identity,LM-AGG-001,BCB_WP239,WP239 Section 2.7 Market Clearing and GDP PDF pages 41-42; Appendix C.4 PDF pages 90-91; main equations 81-85; log-linear equations C.35-C.36,y_c|y_i|y_g|y_x|c|i|g|x|m_int,source_located_weights_pending_calibration,none,market_clearing_locator_present;final_goods_identities_mapped;weights_not_invented,sourced,WBS-041,Market-clearing identities are source-located only.
EQ-AGG-002,AGG,Absorption and net exports accounting,identity,LM-AGG-001,BCB_WP239,WP239 Section 2.7 PDF pages 41-42; Appendix C.4 PDF page 90; main equations 78-80; log-linear equations C.37-C.39,abs|c|i|g|nx|x|m|q|nfa,source_located_weights_pending_calibration,none,absorption_mapped;net_exports_mapped;nfa_link_mapped;identity_required_before_dynare,sourced,WBS-041,Absorption and NX links remain registry-only until model implementation is allowed.
EQ-AGG-003,AGG,Real GDP and GDP deflator identities,identity,LM-AGG-001,BCB_WP239,WP239 Section 2.7 PDF pages 41-42; Appendix C.5 PDF page 91; main equations 86-87; log-linear equations C.40-C.42,y|pi_y|q_y|c|i|g|x|m,source_located_weights_pending_calibration,none,real_gdp_identity_located;gdp_deflator_identity_located;inflation_aggregation_test_required,sourced,WBS-041,Weights and observable measurement remain future calibration/data work.
EQ-AGG-004,AGG,Output gap and potential output reporting locator,auxiliary,LM-AGG-001,BCB_WP239,WP239 Appendix C.3 PDF page 89 equation C.28; docs/00b MON-001 OBS-001 and STRUCT-001; measurement candidate in EQ-MEAS-015,y_gap|y_pot,none,none,y_gap_structural_variable_present;y_pot_structural_variable_present;not_required_for_wbs057_mod;measurement_deferred_to_data_dictionary,deferred,WBS-041,No separate WP239 potential-output equation is required for WBS-057. y_gap enters the model through EQ-MON-001; y_pot and measurement/reporting treatment remain later work.
EQ-SHOCK-001,SHOCK,Monetary policy innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF page 93; equation C.60,monetary_policy_shock_state,std_pending_calibration,eps_monetary,shock_name_declared;std_not_calibrated_here;linked_to_EQ-MON-003,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-002,SHOCK,Inflation target innovation disabled in calibrated MVP,shock_process,LM-MON-001,BCB_WP239,WP239 Section 2.3.1 PDF page 34; Appendix C.3 PDF page 89; equation C.29,pi_target,std_pending_future_phase,eps_pi_target,shock_name_declared;eps_pi_target_off_in_calibrated_mvp;target_is_deterministic_series;future_phase_only,deferred,WBS-042,Recorded from TARGET-001 but disabled for calibrated MVP.
EQ-SHOCK-003,SHOCK,Fiscal government spending innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF page 93; equation C.61,government_spending_shock_state,std_pending_calibration,eps_fiscal_g,shock_name_declared;std_not_calibrated_here;linked_to_EQ-FISC-002,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-004,SHOCK,Primary surplus target innovation,shock_process,LM-FISC-001,BCB_WP239,WP239 Appendix C.3 PDF page 89; equation C.31,sp_target,std_pending_calibration,eps_sp_target,shock_name_declared;std_not_calibrated_here;linked_to_EQ-FISC-001,sourced,WBS-042,Primary surplus target shock is distinct from realized surplus.
EQ-SHOCK-005,SHOCK,Tax rate innovation,shock_process,LM-FISC-001,BCB_WP239,WP239 Appendix C.3 PDF page 89; equation C.32,tax_rate,std_pending_calibration,eps_tax,shock_name_declared;std_not_calibrated_here;linked_to_EQ-FISC-004,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-006,SHOCK,Technology innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF pages 91-92; equations C.51-C.52,technology_state,std_pending_calibration,eps_tfp,shock_name_declared;transitory_and_permanent_technology_located;std_not_calibrated_here,sourced,WBS-042,SPEC name maps to WP239 technology shock locators without choosing calibration.
EQ-SHOCK-007,SHOCK,Preference innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF page 91; equation C.48,preference_shock_state,std_pending_calibration,eps_pref,shock_name_declared;std_not_calibrated_here;linked_to_EQ-HH-001,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-008,SHOCK,Investment innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; equation C.53,investment_shock_state,std_pending_calibration,eps_investment,shock_name_declared;std_not_calibrated_here;linked_to_EQ-FIRM-003,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-009,SHOCK,Free-price markup innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; equation C.57,price_markup_state,std_pending_calibration,eps_price_free,shock_name_declared;std_not_calibrated_here;linked_to_EQ-FIRM-002,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-010,SHOCK,Administered-price innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; equation C.58,admin_price_shock_state,std_pending_calibration,eps_price_admin,shock_name_declared;std_not_calibrated_here;linked_to_EQ-PRICE-001,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-011,SHOCK,Wage markup innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; equation C.56,wage_markup_state,std_pending_calibration,eps_wage,shock_name_declared;std_not_calibrated_here;linked_to_EQ-HH-003,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-012,SHOCK,Import price innovation,shock_process,LM-EXT-001,BCB_WP239,WP239 Appendix C.5 PDF page 91; equation C.44,import_price_state,std_pending_calibration,eps_import_price,shock_name_declared;std_not_calibrated_here;linked_to_EQ-FIRM-004,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-013,SHOCK,Risk premium innovation,shock_process,LM-SHOCK-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; equation C.50,risk,std_pending_calibration,eps_risk,shock_name_declared;std_not_calibrated_here;linked_to_EQ-EXT-002,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-014,SHOCK,Foreign output innovation,shock_process,LM-EXT-001,BCB_WP239,WP239 Appendix C.5 PDF page 91; equation C.43,foreign_output_state,std_pending_calibration,eps_foreign_y,shock_name_declared;std_not_calibrated_here;foreign_block_locator_present,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-015,SHOCK,Foreign interest rate innovation,shock_process,LM-EXT-001,BCB_WP239,WP239 Appendix C.5 PDF page 91; equation C.47,foreign_interest_state,std_pending_calibration,eps_foreign_r,shock_name_declared;std_not_calibrated_here;foreign_block_locator_present,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-016,SHOCK,Foreign inflation innovation,shock_process,LM-EXT-001,BCB_WP239,WP239 Appendix C.5 PDF page 91; equation C.45,foreign_inflation_state,std_pending_calibration,eps_foreign_pi,shock_name_declared;std_not_calibrated_here;foreign_block_locator_present,sourced,WBS-042,Dynare name reserved only; no model file created.
EQ-SHOCK-017,SHOCK,Commodity innovation deferred,shock_process,LM-SHOCK-001,BCB_WP239,SPEC Section 10.1 lists eps_commodity; WP239 equation locator not verified,commodity_shock_state,std_pending_source_locator,eps_commodity,shock_name_declared;source_locator_pending;not_enabled_for_mvp_until_source_verified,deferred,WBS-042,Registered as deferred to avoid inventing a WP239 equation.
EQ-MEAS-001,MEAS,Real GDP growth observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_gdp_real,y|br_gdp_real,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;no_source_id_invention;no_data_created,draft,WBS-043,Final growth or log-deviation mapping remains blocked until Gate 1b.
EQ-MEAS-002,MEAS,Headline IPCA inflation observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_ipca_headline,pi|br_ipca_headline,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;inflation_compounding_rule_required;no_data_created,draft,WBS-043,Monthly-to-quarterly treatment remains Gate 1b work.
EQ-MEAS-003,MEAS,Selic policy rate observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_selic,r|br_selic,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;interest_rate_average_or_effective_rule_pending;no_data_created,draft,WBS-043,Meta versus over and quarterly conversion remain Gate 1b decisions.
EQ-MEAS-004,MEAS,Real exchange rate observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_real_exchange_rate,q|br_real_exchange_rate,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;q_up_means_brl_real_depreciation;no_data_created,draft,WBS-043,Uses project sign convention only; source and conversion remain Gate 1b.
EQ-MEAS-005,MEAS,Private consumption observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_private_consumption,c|br_private_consumption,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;real_activity_transform_pending;no_data_created,draft,WBS-043,Final source and transformation remain Gate 1b.
EQ-MEAS-006,MEAS,Investment observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_investment,i|br_investment,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;real_activity_transform_pending;no_data_created,draft,WBS-043,Final source and transformation remain Gate 1b.
EQ-MEAS-007,MEAS,Government consumption observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_government_consumption,g|br_government_consumption,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;real_activity_transform_pending;no_data_created,draft,WBS-043,Final source and transformation remain Gate 1b.
EQ-MEAS-008,MEAS,Exports observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_exports,x|br_exports,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;real_activity_transform_pending;no_data_created,draft,WBS-043,Final source and transformation remain Gate 1b.
EQ-MEAS-009,MEAS,Imports observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_imports,m|br_imports,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;real_activity_transform_pending;no_data_created,draft,WBS-043,Final source and transformation remain Gate 1b.
EQ-MEAS-010,MEAS,Free-price inflation observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_ipca_free,pi_f|br_ipca_free,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;inflation_compounding_rule_required;no_data_created,draft,WBS-043,Optional composition remains blocked until source verification.
EQ-MEAS-011,MEAS,Administered-price inflation observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_ipca_administered,pi_a|br_ipca_administered,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;admin_process_not_generic_shock;no_data_created,draft,WBS-043,Connects to ADMIN process only after source and transformation verification.
EQ-MEAS-012,MEAS,Import price inflation observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_import_price_inflation,pi_m|br_import_price_inflation,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;imported_inflation_measure_pending;no_data_created,draft,WBS-043,Used by administered-price pass-through only when available.
EQ-MEAS-013,MEAS,Inflation target observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_inflation_target,pi_target|br_inflation_target,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;pi_target_deterministic_in_calibrated_mvp;eps_pi_target_off,draft,WBS-043,Calibrated MVP treats target as deterministic or exogenous series.
EQ-MEAS-014,MEAS,Risk premium observable draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_risk_premium,risk|br_risk_premium,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;risk_ar1_structural_process_present;no_data_created,draft,WBS-043,Observable candidate does not replace structural risk process.
EQ-MEAS-015,MEAS,Output gap observable candidate draft,measurement_draft,LM-MEAS-001,BCB_WP239,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94; docs/02_data_dictionary.md br_output_gap,y_gap|br_output_gap,measurement_transform_pending_gate1b,none,measurement_draft_until_gate1b;source_id_tbd_allowed_until_gate1b;y_gap_structural_variable_present;measurement_not_final,draft,WBS-043,Observed or semi-observed output gap remains future Gate 1b or later work.
```

---

## 5. WBS-057b Dynare symbol mappings

These mappings are assistant-reviewed registry aliases for WBS-057b only. They do not authorize `.mod`, `.inc`, data, outputs, estimation, Redux, or sovereign files.

```csv
wp239_symbol,canonical_project_name,dynare_name,type,used_in_equation_ids,wbs_assignment,mapping_status
cO_t,c_o,c_o,endogenous,EQ-HH-001;EQ-HH-002,WBS-057,mapped_to_registry
sB_t,risk_dom,risk_dom,endogenous/shock_state,EQ-HH-001;EQ-EXT-001;EQ-FIRM-003,WBS-057,mapped_to_registry
zQ_t,z_q,z_q,shock_state,EQ-EXT-001,WBS-057/WBS-058,mapped_to_registry
rho_Q,rho_z_q,rho_z_q,parameter,EQ-EXT-001,WBS-058,deferred_to_wbs058_shocks
rho_C,rho_z_c,rho_z_c,parameter,EQ-HH-001;EQ-HH-003,WBS-058,deferred_to_wbs058_shocks
rho_Z,rho_z_z,rho_z_z,parameter,EQ-HH-001;EQ-FIRM-003;EQ-FISC-003,WBS-058,deferred_to_wbs058_shocks
rho_I,rho_z_i,rho_z_i,parameter,EQ-FIRM-003,WBS-058,deferred_to_wbs058_shocks
rho_D,rho_z_d,rho_z_d,parameter,EQ-FIRM-001,WBS-058,deferred_to_wbs058_shocks
rho_M,rho_z_m,rho_z_m,parameter,EQ-FIRM-004,WBS-058,deferred_to_wbs058_shocks
rho_P,rho_z_p,rho_z_p,parameter,EQ-FIRM-002,WBS-058,deferred_to_wbs058_shocks
qF_t,q_f,q_f,endogenous,EQ-PRICE-001;EQ-FIRM-002,WBS-057,mapped_to_registry
qG_t,q_g,q_g,endogenous,EQ-FISC-002;EQ-AGG-003,WBS-057,mapped_to_registry
qI_t,q_i,q_i,endogenous,EQ-FIRM-003;EQ-AGG-003,WBS-057,mapped_to_registry
qMstar_t,q_m_star,q_m_star,endogenous,EQ-EXT-003;EQ-AGG-002;EQ-AGG-003,WBS-057,mapped_to_registry
qXstar_t,q_x_star,q_x_star,endogenous,EQ-FIRM-002;EQ-AGG-002;EQ-AGG-003,WBS-057,mapped_to_registry
zM_t,z_m,z_m,shock_state,EQ-FIRM-004,WBS-057/WBS-058,mapped_to_registry
piF_t,pi_f,pi_f,endogenous,EQ-FIRM-002;EQ-PRICE-001,WBS-057,mapped_to_registry
piH_t,pi_g|pi_i,pi_g|pi_i,template_alias_expanded,EQ-FIRM-002,WBS-057,alias_resolved
piM_t,pi_m,pi_m,endogenous,EQ-FIRM-002;EQ-FIRM-004,WBS-057,mapped_to_registry
piX_t,pi_x,pi_x,endogenous,EQ-FIRM-002,WBS-057,mapped_to_registry
vF_t,v_f,v_f,endogenous_aux,EQ-FIRM-002,WBS-057,mapped_to_registry
vH_t,v_g|v_i,v_g|v_i,template_alias_expanded,EQ-FIRM-002,WBS-057,alias_resolved
vM_t,v_m,v_m,endogenous_aux,EQ-FIRM-002,WBS-057,mapped_to_registry
vX_t,v_x,v_x,endogenous_aux,EQ-FIRM-002,WBS-057,mapped_to_registry
theta_A,theta_admin,theta_admin,parameter,EQ-PRICE-001,WBS-057,mapped_to_calibration
chi_A,chi_admin,chi_admin,parameter,EQ-PRICE-001,WBS-057,mapped_to_calibration
```
