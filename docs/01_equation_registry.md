# Equation Registry - samba-dsge-br

**Documento:** `docs/01_equation_registry.md`
**Status:** Gate 2b MON EXT FISC ADMIN HH FIRM AGG and SHOCK entries partial
**Fonte canonica:** `docs/00a_literature_map.md`
**Criado em:** 2026-05-26

---

## 0. Gate status

```yaml
gate: Gate 2b
wbs: WBS-042
gate_status: shock_block_registered
gate2b_passed: false
dynare_allowed: false
model_file_allowed: false
source_memory_allowed: false
monetary_block_registered: true
external_block_registered: true
fiscal_block_registered: true
administered_prices_registered: true
household_block_registered: true
firm_block_registered: true
aggregation_block_registered: true
shock_block_registered: true
core_blocks_registered: false
registry_version: 0.9.0-shock
created_at: 2026-05-26
updated_at: 2026-05-26
```

Gate 2b is not passed. Registry entries are registered through WBS-042.

---

## 1. Registry policy

```text
- Do not register equations from memory.
- Every future equation entry must point to `docs/00a_literature_map.md`.
- Equation numbers may be used as locators, but formulas are entered only in the relevant WBS.
- Measurement equations remain draft until Gate 1b source IDs are verified.
- Dynare and `model/` files remain blocked until Gate 2b passes.
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
EQ-MON,MON,LM-MON-001,WBS-035,registered_partial
EQ-EXT,EXT,LM-EXT-001,WBS-036,registered_partial
EQ-FISC,FISC,LM-FISC-001,WBS-037,registered_partial
EQ-PRICE,ADMIN,LM-PRICE-ADMIN-001,WBS-038,registered_partial
EQ-HH,HH,LM-HH-001,WBS-039,registered_partial
EQ-FIRM,FIRM,LM-FIRM-001,WBS-040,registered_partial
EQ-AGG,AGG,LM-AGG-001,WBS-041,registered_partial
EQ-SHOCK,SHOCK,LM-SHOCK-001,WBS-042,registered_partial
EQ-MEAS,MEAS,LM-MEAS-001,WBS-043,draft_until_gate1b
```

---

## 4. Registry entries

WBS-035 through WBS-042 entries are registered.

```csv
equation_id,block,title,equation_type,source_map_id,source_reference_id,source_locator,variables,parameters,shocks,tests,status,gate,notes
EQ-MON-001,MON,Forward-looking Taylor rule,structural,LM-MON-001,BCB_WP239,WP239 Section 2.3.1 PDF pages 33-34; Appendix C.3 PDF page 89; main equation 61; log-linear equation C.28,r_t|r_lag|pi_expected|pi_target|y_gap,rho_r|phi_pi|phi_y|r_ss,eps_monetary,monetary_irf_sign_timing_magnitude_benchmark;smoothing_parameter_present;target_gap_present,sourced,WBS-035,Implements MON-001 contract without Dynare syntax.
EQ-MON-002,MON,Inflation target treatment,auxiliary,LM-MON-001,BCB_WP239,WP239 Section 2.3.1 PDF page 34; main equation 62; Appendix C.3 PDF page 89; log-linear equation C.29,pi_target,none,none,pi_target_explicit;eps_pi_target_absent_in_calibrated_mvp;deterministic_target_series_allowed,sourced,WBS-035,Implements TARGET-001 calibrated MVP treatment.
EQ-MON-003,MON,Monetary policy shock,shock_process,LM-MON-001,BCB_WP239,WP239 Appendix C.6 PDF page 93; shock equation C.60,monetary_policy_shock_state,none_for_mvp_monetary_shock_term,eps_monetary,shock_declared;irf_response_timing_defined;shock_not_used_for_target_changes,sourced,WBS-035,Shock naming remains registry-only until WBS-042 and Dynare remains blocked.
EQ-EXT-001,EXT,UIP with NFA debt-elastic risk premium,structural,LM-EXT-001,BCB_WP239,WP239 Section 2.4 PDF page 38; Section 2.7 PDF pages 41-42; Appendix C.4-C.5 PDF pages 90-91; log-linear equations C.37-C.47,q|delta_q_expected|r_t|pi_expected|r_star|pi_star|nfa|risk,psi_nfa|nfa_ss,risk,external_closure_explicit;nfa_debt_elastic_premium_present;uip_uses_expected_depreciation;sources_located,sourced,WBS-036,Implements EXT-001 baseline closure without Dynare syntax.
EQ-EXT-002,EXT,Risk premium AR1 process,shock_process,LM-EXT-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; risk-premium shock equation C.50,risk|risk_lag,rho_risk,eps_risk,ar1_process_present;eps_risk_declared;not_pure_ar1_closure_without_nfa,sourced,WBS-036,Risk_t is a shock process and not the sole external closure.
EQ-EXT-003,EXT,NFA law of motion locator,identity,LM-EXT-001,BCB_WP239,WP239 Section 2.7 PDF pages 41-42; main equations 78-80; Appendix C.4 PDF page 90; log-linear equations C.37-C.39,nfa|nx|external_loans|q|imports|exports,source_located_parameters_pending_calibration,none,nfa_state_declared;external_balance_identity_located;calibration_notes_required_before_dynare,sourced,WBS-036,Parameters are not invented; calibration remains future work.
EQ-EXT-004,EXT,Real exchange rate sign convention,auxiliary,LM-EXT-001,BCB_WP239,WP239 Section 2.4 PDF page 38; Appendix C.4-C.5 PDF pages 90-91,q|delta_q,none,none,q_up_means_brl_real_depreciation;delta_q_used_in_uip;exchange_rate_measurement_deferred_to_data_dictionary,sourced,WBS-036,Project convention follows EXT-001 approval.
EQ-FISC-001,FISC,Primary surplus target with debt feedback,structural,LM-FISC-001,BCB_WP239,WP239 Section 2.3 Government PDF pages 33-36; Appendix C.3 PDF page 89; main equation 64; log-linear equation C.31,sp_target|sp_target_lag|b|b_ss|y_gap,rho_sp_target|phi_b|phi_y_sp|sp_ss,eps_sp_target,sp_target_separate_from_sp;debt_gdp_feedback_present;phi_b_positive_required;stabilizing_feedback_defined,sourced,WBS-037,Implements FISC-001 target rule without Dynare syntax.
EQ-FISC-002,FISC,Realized primary surplus and government spending instrument,structural,LM-FISC-001,BCB_WP239,WP239 Section 2.3 Government PDF pages 33-36; Appendix C.3 PDF page 89; main equations 63 and 65-68; log-linear equations C.30 and C.33,sp|sp_lag|sp_target|g|tax_rate|y,source_located_parameters_pending_calibration,none,sp_realized_distinct_from_sp_target;government_consumption_instrument_located;source_parameters_not_invented,sourced,WBS-037,Government spending is the fiscal instrument implied by the primary-surplus rule.
EQ-FISC-003,FISC,Public debt to GDP law of motion,identity,LM-FISC-001,BCB_WP239,WP239 Section 2.3 Government PDF pages 33-36; Appendix C.3 PDF page 89; log-linear equation C.34,b|b_lag|r_t|sp|y|pi_y|trend_growth,source_located_parameters_pending_calibration,none,b_represents_public_debt_gdp;debt_identity_located;identity_required_before_dynare,sourced,WBS-037,Debt identity must be reviewed before any model file is created.
EQ-FISC-004,FISC,Fiscal auxiliary tax and primary surplus locators,auxiliary,LM-FISC-001,BCB_WP239,WP239 Section 2.3 Government PDF pages 35-36; Appendix C.3 PDF page 89; main equations 65-68; log-linear equation C.32,tax_rate|nominal_tax_revenue|nominal_primary_surplus,source_located_parameters_pending_calibration,none,tax_auxiliary_located;no_regime_2016_2023_in_mvp;calibration_notes_required_before_dynare,sourced,WBS-037,Auxiliary fiscal identities are source-located but not calibrated here.
EQ-PRICE-001,ADMIN,Administered prices inflation process,structural,LM-PRICE-ADMIN-001,BCB_WP239,WP239 Section 2.5 Shocks PDF page 38; Appendix C.6 PDF page 92; administered prices shock equation C.58,pi_a|pi_a_lag|pi_target|delta_q|pi_m,rho_a|alpha_a_target|alpha_a_fx|alpha_a_m,eps_admin,admin_process_own_equation;ar1_persistence_present;pass_through_terms_declared;eps_admin_declared;not_generic_shock,sourced,WBS-038,Implements ADMIN-001 approved process; availability of pi_m and measurement remains Gate 1b work.
EQ-PRICE-002,ADMIN,Administered prices shock locator,shock_process,LM-PRICE-ADMIN-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; administered prices shock equation C.58,admin_price_shock_state|admin_price_shock_lag,rho_admin,eps_admin,admin_shock_source_located;shock_not_substitute_for_full_process;shock_name_harmonization_deferred_to_wbs042,sourced,WBS-038,Source locator for the WP239 administered-price shock process.
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
EQ-AGG-004,AGG,Output gap and potential output accounting,auxiliary,LM-AGG-001,BCB_WP239,WP239 Section 2.6 Aggregation PDF pages 38-40; Section 2.7 PDF pages 41-42; Appendix C.4-C.5 PDF pages 90-91,y|y_pot|y_gap|trend_growth,source_located_parameters_pending_calibration,none,y_gap_structural_variable_present;y_pot_structural_variable_present;measurement_deferred_to_data_dictionary,sourced,WBS-041,STRUCT-001 variables are mapped; measurement equation remains Gate 1b or later work.
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
```
