# Equation Registry - samba-dsge-br

**Documento:** `docs/01_equation_registry.md`
**Status:** Gate 2b MON and EXT entries partial
**Fonte canonica:** `docs/00a_literature_map.md`
**Criado em:** 2026-05-26

---

## 0. Gate status

```yaml
gate: Gate 2b
wbs: WBS-036
gate_status: external_block_registered
gate2b_passed: false
dynare_allowed: false
model_file_allowed: false
source_memory_allowed: false
monetary_block_registered: true
external_block_registered: true
core_blocks_registered: false
registry_version: 0.3.0-ext
created_at: 2026-05-26
updated_at: 2026-05-26
```

Gate 2b is not passed. Monetary-policy and external-block entries are registered through WBS-036.

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
EQ-FISC,FISC,LM-FISC-001,WBS-037,ready_for_registry_entry
EQ-PRICE,ADMIN,LM-PRICE-ADMIN-001,WBS-038,ready_for_registry_entry
EQ-HH,HH,LM-HH-001,WBS-039,ready_for_registry_entry
EQ-FIRM,FIRM,LM-FIRM-001,WBS-040,ready_for_registry_entry
EQ-AGG,AGG,LM-AGG-001,WBS-041,ready_for_registry_entry
EQ-SHOCK,SHOCK,LM-SHOCK-001,WBS-042,ready_for_registry_entry
EQ-MEAS,MEAS,LM-MEAS-001,WBS-043,draft_until_gate1b
```

---

## 4. Registry entries

WBS-035 monetary-policy and WBS-036 external-block entries are registered.

```csv
equation_id,block,title,equation_type,source_map_id,source_reference_id,source_locator,variables,parameters,shocks,tests,status,gate,notes
EQ-MON-001,MON,Forward-looking Taylor rule,structural,LM-MON-001,BCB_WP239,WP239 Section 2.3.1 PDF pages 33-34; Appendix C.3 PDF page 89; main equation 61; log-linear equation C.28,r_t|r_lag|pi_expected|pi_target|y_gap,rho_r|phi_pi|phi_y|r_ss,eps_monetary,monetary_irf_sign_timing_magnitude_benchmark;smoothing_parameter_present;target_gap_present,sourced,WBS-035,Implements MON-001 contract without Dynare syntax.
EQ-MON-002,MON,Inflation target treatment,auxiliary,LM-MON-001,BCB_WP239,WP239 Section 2.3.1 PDF page 34; main equation 62; Appendix C.3 PDF page 89; log-linear equation C.29,pi_target,none,none,pi_target_explicit;eps_pi_target_absent_in_calibrated_mvp;deterministic_target_series_allowed,sourced,WBS-035,Implements TARGET-001 calibrated MVP treatment.
EQ-MON-003,MON,Monetary policy shock,shock_process,LM-MON-001,BCB_WP239,WP239 Appendix C.6 PDF page 93; shock equation C.60,monetary_policy_shock_state,none_for_mvp_monetary_shock_term,eps_monetary,shock_declared;irf_response_timing_defined;shock_not_used_for_target_changes,sourced,WBS-035,Shock naming remains registry-only until WBS-042 and Dynare remains blocked.
EQ-EXT-001,EXT,UIP with NFA debt-elastic risk premium,structural,LM-EXT-001,BCB_WP239,WP239 Section 2.4 PDF page 38; Section 2.7 PDF pages 41-42; Appendix C.4-C.5 PDF pages 90-91; log-linear equations C.37-C.47,q|delta_q_expected|r_t|pi_expected|r_star|pi_star|nfa|risk,psi_nfa|nfa_ss,risk,external_closure_explicit;nfa_debt_elastic_premium_present;uip_uses_expected_depreciation;sources_located,sourced,WBS-036,Implements EXT-001 baseline closure without Dynare syntax.
EQ-EXT-002,EXT,Risk premium AR1 process,shock_process,LM-EXT-001,BCB_WP239,WP239 Appendix C.6 PDF page 92; risk-premium shock equation C.50,risk|risk_lag,rho_risk,eps_risk,ar1_process_present;eps_risk_declared;not_pure_ar1_closure_without_nfa,sourced,WBS-036,Risk_t is a shock process and not the sole external closure.
EQ-EXT-003,EXT,NFA law of motion locator,identity,LM-EXT-001,BCB_WP239,WP239 Section 2.7 PDF pages 41-42; main equations 78-80; Appendix C.4 PDF page 90; log-linear equations C.37-C.39,nfa|nx|external_loans|q|imports|exports,source_located_parameters_pending_calibration,none,nfa_state_declared;external_balance_identity_located;calibration_notes_required_before_dynare,sourced,WBS-036,Parameters are not invented; calibration remains future work.
EQ-EXT-004,EXT,Real exchange rate sign convention,auxiliary,LM-EXT-001,BCB_WP239,WP239 Section 2.4 PDF page 38; Appendix C.4-C.5 PDF pages 90-91,q|delta_q,none,none,q_up_means_brl_real_depreciation;delta_q_used_in_uip;exchange_rate_measurement_deferred_to_data_dictionary,sourced,WBS-036,Project convention follows EXT-001 approval.
```
