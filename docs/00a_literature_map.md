# Literature Map - samba-dsge-br

**Documento:** `docs/00a_literature_map.md`
**Status:** Gate 2a source locator pass
**Fonte canonica:** `samba_dsge_br_spec_standalone_consolidado.md`
**Criado em:** 2026-05-25

---

## 0. Gate status

```yaml
gate: Gate 2a
gate_status: source_locator_pass_complete
equation_registry_allowed: true
dynare_allowed: false
source_memory_allowed: false
precise_locators_complete: true
wp578_outline_verified: true
wp239_visual_locator_pass: true
wp239_equation_table_locators_verified: true
auxiliary_primary_sources_deferred: true
```

Gate 2a is passed for equation-registry anchoring. Gate 2b is not passed.

---

## 1. Source policy

```text
- Nao inventar secoes, equacoes, tabelas, parametros, priors ou resultados.
- Usar fonte primaria quando disponivel.
- Se a fonte foi citada no SPEC, mas ainda nao foi lida diretamente, marcar como pending_primary_source.
- Equation registry core so pode ser criado depois de mapear blocos contra fontes primarias.
- Linhas sem locator primario nao autorizam implementacao Dynare.
```

---

## 2. Canonical references

```csv
reference_id,paper,official_source,source_status,role_in_project
BCB_WP239,"Castro, Gouvea, Minella, Santos, Souza-Sobrinho. SAMBA: Stochastic Analytical Model with a Bayesian Approach. Banco Central do Brasil Working Paper 239, 2011.",https://www.bcb.gov.br/pec/wps/ingl/wps239.pdf,verified_official_bcb,Primary source for SAMBA classic MVP.
BCB_WP578,"Fasolo, Araujo, Jorge, Kornelius, Marinho. Brazilian Macroeconomic Dynamics Redux: Shocks, Frictions, and Unemployment in SAMBA Model. Banco Central do Brasil Working Paper 578, 2023.",https://www.bcb.gov.br/content/publicacoes/WorkingPaperSeries/WP578.pdf,verified_official_bcb,Primary source for Redux boundaries and future non-MVP work.
SMETS_WOUTERS,Smets-Wouters medium-scale DSGE reference from SPEC,deferred_not_required_for_gate2a,deferred_auxiliary,Auxiliary source for nominal rigidities if BCB_WP239 is insufficient later.
ERCEG_HENDERSON_LEVIN,Erceg-Henderson-Levin wage rigidity reference from SPEC,deferred_not_required_for_gate2a,deferred_auxiliary,Auxiliary source for wage rigidity if BCB_WP239 is insufficient later.
SGU_DEBT_ELASTIC,Schmitt-Grohe-Uribe small open economy closure reference from SPEC,deferred_not_required_for_gate2a,deferred_auxiliary,Auxiliary source for NFA/debt-elastic external closure if BCB_WP239 is insufficient later.
ISKREV_IDENTIFICATION,Iskrev local identification reference from SPEC,deferred_post_mvp,deferred_auxiliary,Future identification phase.
KOMUNJER_NG_IDENTIFICATION,Komunjer-Ng local identification reference from SPEC,deferred_post_mvp,deferred_auxiliary,Future identification phase.
LENZA_PRIMICERI_COVID,Lenza-Primiceri outlier treatment reference from SPEC,deferred_post_mvp,deferred_auxiliary,Post-MVP COVID/outlier robustness only.
```

---

## 3. Verified locator notes

```text
- BCB_WP239 was read from the official BCB PDF. Text extraction corrupts many headings/equations, so exact locators below are based on visual inspection of rendered official-PDF pages.
- BCB_WP578 was read from the official BCB PDF. The PDF outline provides exact section locators by PDF page.
- No equation, parameter, prior, data series ID, or result was copied into this map.
- Auxiliary references are deferred because BCB_WP239 is the primary source for the classic MVP registry.
```

---

## 4. MVP block map

Rows below are source anchors with visually verified WP239 locators. Equation numbers are cited only as locators.

```csv
map_id,reference_id,model_block,project_use,section_locator,equation_table_figure,parameters_used,replication_target,status,notes
LM-CLASSIC-SCOPE-001,BCB_WP239,scope,Define SAMBA classic target for MVP,WP239 Introduction PDF pages 5-7; Section 2 Model Overview PDF pages 7-9; Appendix A-C PDF pages 71-93; Tables 1-5 PDF pages 94-101,Section 2 equations (1)-(87); Appendix C equations (C.1)-(C.61); Tables 1-5,none,Classic calibrated MVP boundaries,verified_locator,Do not infer internal BCB implementation.
LM-MON-001,BCB_WP239,MON,Monetary policy rule benchmark,WP239 Section 2.3.1 Monetary Policy PDF pages 33-34; Appendix C.3 Government PDF page 89; Appendix C.6 Shocks PDF page 93,Main equations (61)-(62); log-linear equations (C.28)-(C.29); shock equation (C.60),none,Taylor forward-looking with explicit pi_target_t,verified_locator,Gate 0 fixes the project rule form.
LM-EXT-001,BCB_WP239,EXT,Open economy and risk premium benchmark,WP239 Section 2.4 Rest of the World PDF page 38; Section 2.7 Market Clearing and GDP PDF pages 41-42; Appendix C.4-C.5 PDF pages 90-91; Appendix C.6 PDF page 92,Main NFA and external equations (78)-(80); log-linear equations (C.37)-(C.47); risk-premium shock equation (C.50),none,UIP with NFA/debt-elastic baseline and AR(1) risk_t,verified_locator,q_t up means BRL real depreciation in this project.
LM-FISC-001,BCB_WP239,FISC,Fiscal rule and primary surplus target benchmark,WP239 Section 2.3 Government PDF pages 33-36; Appendix C.3 Government PDF page 89; Appendix C.6 Shocks PDF page 93,Main equations (63)-(68); log-linear equations (C.30)-(C.34); fiscal shock equation (C.61),none,sp_target feedback on debt/GDP and output gap,verified_locator,Full debt identity deferred to equation registry.
LM-PRICE-ADMIN-001,BCB_WP239,ADMIN,Administered prices process benchmark,WP239 Section 2.5 Shocks PDF page 38; Appendix C.6 Shocks PDF page 92; Table 1 PDF page 94,Administered prices shock equation (C.58); Table 1 data series locator,none,pi_a own process with AR(1) and eps_admin,verified_locator,Administrados are not a generic shock.
LM-HH-001,BCB_WP239,HH,Household block benchmark,WP239 Section 2.1 Households PDF page 10; Section 2.1.1 Optimizing Households PDF pages 11-17; Section 2.1.2 Rule-of-Thumb Households PDF page 18; Appendix C.1 Households PDF pages 84-86,Main equations (1)-(21); log-linear equations (C.1)-(C.10),none,Euler consumption labor structure,verified_locator,No equation copied into this map.
LM-FIRM-001,BCB_WP239,FIRM,Firm pricing investment benchmark,WP239 Section 2.2 Firms PDF pages 18-32; Appendix C.2 Firms PDF pages 86-88,Main equations (22)-(60); log-linear equations (C.11)-(C.27),none,mc q_k price wage investment frictions,verified_locator,STRUCT-001 variables must be covered in registry.
LM-AGG-001,BCB_WP239,AGG,Aggregation and market clearing benchmark,WP239 Section 2.6 Aggregation PDF pages 38-40; Section 2.7 Market Clearing and GDP PDF pages 41-42; Appendix C.4 Resource Constraints and External Sector PDF pages 90-91,Main equations (72)-(87); log-linear equations (C.35)-(C.42),none,Resource constraints and external aggregates,verified_locator,Identities must close before mod work.
LM-SHOCK-001,BCB_WP239,SHOCK,AR(1) shock process benchmark,WP239 Section 2.5 Shocks PDF page 38; Appendix C.6 Shocks - AR(1) Processes PDF pages 91-93,Log-linear shock equations (C.48)-(C.61),none,Named shocks for registry status and tests,verified_locator,No shock equation is copied into this map.
LM-MEAS-001,BCB_WP239,MEAS,Observable and measurement-equation benchmark,WP239 Section 3 Data and Estimation PDF pages 43-53; Table 1 PDF page 94,Table 1 data series locator; measurement equations deferred to data dictionary and registry,none,Draft measurement equations after data dictionary,verified_locator,Final MEAS waits for Gate 1b.
```

---

## 5. Out-of-MVP map

```csv
map_id,reference_id,model_block,project_use,section_locator,equation_table_figure,parameters_used,replication_target,status,notes
LM-REDUX-SCOPE-001,BCB_WP578,REDUX_SCOPE,Document Redux exclusions from MVP,"WP578 The model, PDF page 8; Redux model sections continue through transformations on PDF page 35",not_applicable_for_mvp_boundary,none,Redux is out of MVP,verified_section_locator,Unemployment participation imported-consumption external SVAR and SMC stay out of MVP.
LM-LAB-REDUX-001,BCB_WP578,LAB,Future labor market extension,"WP578 Households, PDF page 9; Rule-of-Thumb Households and Labor Supply Aggregation, PDF page 12; Nominal Wage Setting, PDF page 14",not_applicable_for_mvp_boundary,none,Unemployment and participation only after MVP,deferred_out_of_mvp,Do not implement in classic MVP.
LM-IMPORT-REDUX-001,BCB_WP578,IMPORTS,Future imported consumption extension,"WP578 Demand for Imported Goods and Consumer Price Index, PDF page 15; First Stage Importers, PDF page 18",not_applicable_for_mvp_boundary,none,Imported goods bundle only after MVP,deferred_out_of_mvp,Do not implement in classic MVP.
LM-EXT-REDUX-001,BCB_WP578,EXT,Future external block extension,"WP578 Demand for Brazilian Exports and Rest of the World, PDF page 30; GDP Definition and Law of Motion for Net Foreign Assets, PDF page 33",not_applicable_for_mvp_boundary,none,External block enhancements only after MVP,deferred_out_of_mvp,Do not implement in classic MVP.
LM-SMC-REDUX-001,BCB_WP578,ESTIMATION,Future SMC estimation reference,"WP578 Priors, posteriors and SMC estimation, PDF page 42; Computational details, PDF page 91",not_applicable_for_mvp_boundary,none,Redux SMC only after Gate 6 and compute benchmark,deferred_out_of_mvp,Do not add SMC to MVP.
```

---

## 6. Acceptance criteria for completing Gate 2a

Gate 2a completion checks:

```text
- BCB_WP239 has exact section/equation/table locators for classic MVP blocks.
- BCB_WP578 has exact locators for out-of-MVP Redux boundaries.
- Auxiliary references have primary sources verified or are removed/deferred.
- Every planned core registry block points to a source row.
- No equation or parameter is copied from memory.
```

Current status: Gate 2a passed for equation-registry anchoring. Equation registry core may start; Dynare remains blocked until Gate 2b passes.
