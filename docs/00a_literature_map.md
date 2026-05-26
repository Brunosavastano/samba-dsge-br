# Literature Map - samba-dsge-br

**Documento:** `docs/00a_literature_map.md`
**Status:** Gate 2a source skeleton
**Fonte canonica:** `samba_dsge_br_spec_standalone_consolidado.md`
**Criado em:** 2026-05-25

---

## 0. Gate status

```yaml
gate: Gate 2a
gate_status: source_locator_pass_partial
equation_registry_allowed: false
dynare_allowed: false
source_memory_allowed: false
precise_locators_complete: false
wp578_outline_verified: true
wp239_section_locator_partial: true
```

Gate 2b is not passed.

---

## 1. Source policy

```text
- Nao inventar secoes, equacoes, tabelas, parametros, priors ou resultados.
- Usar fonte primaria quando disponivel.
- Se a fonte foi citada no SPEC, mas ainda nao foi lida diretamente, marcar como pending_primary_source.
- Equation registry core so pode ser criado depois de mapear blocos contra fontes primarias.
- Linhas com locator TBD nao autorizam implementacao Dynare.
```

---

## 2. Canonical references

```csv
reference_id,paper,official_source,source_status,role_in_project
BCB_WP239,"Castro, Gouvea, Minella, Santos, Souza-Sobrinho. SAMBA: Stochastic Analytical Model with a Bayesian Approach. Banco Central do Brasil Working Paper 239, 2011.",https://www.bcb.gov.br/pec/wps/ingl/wps239.pdf,verified_official_bcb,Primary source for SAMBA classic MVP.
BCB_WP578,"Fasolo, Araujo, Jorge, Kornelius, Marinho. Brazilian Macroeconomic Dynamics Redux: Shocks, Frictions, and Unemployment in SAMBA Model. Banco Central do Brasil Working Paper 578, 2023.",https://www.bcb.gov.br/content/publicacoes/WorkingPaperSeries/WP578.pdf,verified_official_bcb,Primary source for Redux boundaries and future non-MVP work.
SMETS_WOUTERS,Smets-Wouters medium-scale DSGE reference from SPEC,TBD-primary-source,pending_primary_source,Auxiliary source for nominal rigidities and medium-scale DSGE structure.
ERCEG_HENDERSON_LEVIN,Erceg-Henderson-Levin wage rigidity reference from SPEC,TBD-primary-source,pending_primary_source,Auxiliary source for wage rigidity if needed.
SGU_DEBT_ELASTIC,Schmitt-Grohe-Uribe small open economy closure reference from SPEC,TBD-primary-source,pending_primary_source,Auxiliary source for NFA/debt-elastic external closure.
ISKREV_IDENTIFICATION,Iskrev local identification reference from SPEC,TBD-primary-source,pending_primary_source,Future identification phase.
KOMUNJER_NG_IDENTIFICATION,Komunjer-Ng local identification reference from SPEC,TBD-primary-source,pending_primary_source,Future identification phase.
LENZA_PRIMICERI_COVID,Lenza-Primiceri outlier treatment reference from SPEC,TBD-primary-source,pending_primary_source,Post-MVP COVID/outlier robustness only.
```

---

## 3. Verified locator notes

```text
- BCB_WP239 was read from the official BCB PDF. Section-level locators are partially verified, but exact equation/table locators remain pending because the official PDF text extraction uses an embedded font encoding that corrupts many headings/equations.
- BCB_WP578 was read from the official BCB PDF. The PDF outline provides exact section locators by PDF page.
- No equation, parameter, prior, data series ID, or result was copied into this map.
```

---

## 4. MVP block map

Rows below are source anchors with partial WP239 section locators. Exact equation/table/figure locators remain pending.

```csv
map_id,reference_id,model_block,project_use,section_locator,equation_table_figure,parameters_used,replication_target,status,notes
LM-CLASSIC-SCOPE-001,BCB_WP239,scope,Define SAMBA classic target for MVP,WP239 Introduction and Section 2 Model Overview; PDF pages 5-7,TBD,TBD,Classic calibrated MVP boundaries,partial_locator,Do not infer internal BCB implementation.
LM-MON-001,BCB_WP239,MON,Monetary policy rule benchmark,WP239 Section 2 Model Overview; policy overview text on PDF page 9; exact equation locator pending,TBD,TBD,Taylor forward-looking with explicit pi_target_t,pending_equation_locator,Gate 0 fixes the project rule form.
LM-EXT-001,BCB_WP239,EXT,Open economy and risk premium benchmark,WP239 Section 2 Model Overview; external finance/risk-premium discussion on PDF pages 6 and 9; exact equation locator pending,TBD,TBD,UIP with NFA/debt-elastic baseline and AR(1) risk_t,pending_equation_locator,q_t up means BRL real depreciation in this project.
LM-FISC-001,BCB_WP239,FISC,Fiscal rule and primary surplus target benchmark,WP239 Section 2 Model Overview; fiscal authority overview on PDF page 9; exact equation locator pending,TBD,TBD,sp_target feedback on debt/GDP and output gap,pending_equation_locator,Full debt identity deferred to equation registry.
LM-PRICE-ADMIN-001,BCB_WP239,ADMIN,Administered prices process benchmark,WP239 Introduction and Section 2 Model Overview; administered/regulated prices discussed on PDF pages 5 and 7; exact equation locator pending,TBD,TBD,pi_a own process with AR(1) and eps_admin,pending_equation_locator,Administrados are not a generic shock.
LM-HH-001,BCB_WP239,HH,Household block benchmark,WP239 Section 2.1 Households begins around PDF page 10; Section 2.1.1 Optimizing Households around PDF page 11,TBD,TBD,Euler consumption labor structure,pending_equation_locator,No equation copied until locator verified.
LM-FIRM-001,BCB_WP239,FIRM,Firm pricing investment benchmark,WP239 Section 2 Model Overview describes producers and pricing layers on PDF pages 7-9; exact subsection/equation locator pending,TBD,TBD,mc q_k price wage investment frictions,pending_equation_locator,STRUCT-001 variables must be covered later.
LM-AGG-001,BCB_WP239,AGG,Aggregation and market clearing benchmark,WP239 Section 2 and appendix equilibrium material; exact locator pending,TBD,TBD,Resource constraints and external aggregates,pending_equation_locator,Identities must close before mod work.
LM-MEAS-001,BCB_WP239,MEAS,Observable and measurement-equation benchmark,WP239 Section 3 Data and Estimation and appendix data material; exact locator pending,TBD,TBD,Draft measurement equations after data dictionary,pending_equation_locator,Final MEAS waits for Gate 1b.
```

---

## 5. Out-of-MVP map

```csv
map_id,reference_id,model_block,project_use,section_locator,equation_table_figure,parameters_used,replication_target,status,notes
LM-REDUX-SCOPE-001,BCB_WP578,REDUX_SCOPE,Document Redux exclusions from MVP,"WP578 The model, PDF page 8; Redux model sections continue through transformations on PDF page 35",TBD,TBD,Redux is out of MVP,verified_section_locator,Unemployment participation imported-consumption external SVAR and SMC stay out of MVP.
LM-LAB-REDUX-001,BCB_WP578,LAB,Future labor market extension,"WP578 Households, PDF page 9; Rule-of-Thumb Households and Labor Supply Aggregation, PDF page 12; Nominal Wage Setting, PDF page 14",TBD,TBD,Unemployment and participation only after MVP,deferred_out_of_mvp,Do not implement in classic MVP.
LM-IMPORT-REDUX-001,BCB_WP578,IMPORTS,Future imported consumption extension,"WP578 Demand for Imported Goods and Consumer Price Index, PDF page 15; First Stage Importers, PDF page 18",TBD,TBD,Imported goods bundle only after MVP,deferred_out_of_mvp,Do not implement in classic MVP.
LM-EXT-REDUX-001,BCB_WP578,EXT,Future external block extension,"WP578 Demand for Brazilian Exports and Rest of the World, PDF page 30; GDP Definition and Law of Motion for Net Foreign Assets, PDF page 33",TBD,TBD,External block enhancements only after MVP,deferred_out_of_mvp,Do not implement in classic MVP.
LM-SMC-REDUX-001,BCB_WP578,ESTIMATION,Future SMC estimation reference,"WP578 Priors, posteriors and SMC estimation, PDF page 42; Computational details, PDF page 91",TBD,TBD,Redux SMC only after Gate 6 and compute benchmark,deferred_out_of_mvp,Do not add SMC to MVP.
```

---

## 6. Acceptance criteria for completing Gate 2a

Gate 2a is not complete until:

```text
- BCB_WP239 has exact section/equation/table locators for classic MVP blocks.
- BCB_WP578 has exact locators for out-of-MVP Redux boundaries.
- Auxiliary references have primary sources verified or are removed/deferred.
- Every planned core registry block points to a source row.
- No equation or parameter is copied from memory.
```

Current status: partial source locator pass complete; exact WP239 equation/table locators and auxiliary primary sources pending.
