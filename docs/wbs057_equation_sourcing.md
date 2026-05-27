# WBS-057 Equation Sourcing

Status: `BLOCKED_WBS057_EQUATION_SOURCES`

Policy: WBS-057 may create `model/samba_classic/samba_classic.mod` only after each MVP-required model equation has an exact formula sourced from WP239 Appendix C or an approved project decision. Registry locators alone are not exact formulas.

| equation_id | block | source | source_location | status | usable_in_samba_classic_mod | notes |
|---|---|---|---|---|---|---|
| EQ-MON-001 | MON | approved project decision; BCB_WP239 locator | docs/00b_modeling_decisions.md MON-001; WP239 C.28 locator | sourced_project_decision | true | Taylor rule form is explicitly approved. |
| EQ-MON-002 | MON | approved project decision | docs/00b_modeling_decisions.md TARGET-001 | sourced_project_decision | true | `pi_target` is deterministic/exogenous; no target shock in calibrated MVP. |
| EQ-MON-003 | MON | BCB_WP239 locator | WP239 C.60 locator | missing_formula | false | Monetary shock equation is located but exact Dynare-ready formula is not recorded. |
| EQ-EXT-001 | EXT | approved project decision; BCB_WP239 locator | docs/00b_modeling_decisions.md EXT-001; WP239 C.37-C.47 locators | sourced_project_decision | true | UIP/NFA closure form is explicitly approved. |
| EQ-EXT-002 | EXT | approved project decision | docs/00b_modeling_decisions.md EXT-001 | sourced_project_decision | true | Risk AR(1) is explicitly approved. |
| EQ-EXT-003 | EXT | BCB_WP239 locator | WP239 equations 78-80; C.37-C.39 locators | missing_formula | false | NFA law and external accounting are located but not recorded as exact formulas. |
| EQ-EXT-004 | EXT | approved project decision | docs/00b_modeling_decisions.md EXT-001 | loglinear_convention | true | Sign convention only; not a separate model equation. |
| EQ-FISC-001 | FISC | BCB_WP239 locator | WP239 equation 64; C.31 locator | missing_formula | false | Exact WP239 C.31 formula must be recorded; SPEC formula conflicts with later registry taxonomy. |
| EQ-FISC-002 | FISC | BCB_WP239 locator | WP239 equations 63 and 65-68; C.30 and C.33 locators | missing_formula | false | Realized surplus/government spending equations are not recorded exactly. |
| EQ-FISC-003 | FISC | BCB_WP239 locator | WP239 C.34 locator | missing_formula | false | Debt law of motion is located but not recorded exactly. |
| EQ-FISC-004 | FISC | BCB_WP239 locator | WP239 C.32 locator | missing_formula | false | Fiscal auxiliary identities are not recorded exactly. |
| EQ-PRICE-001 | ADMIN | BCB_WP239 locator | WP239 C.58 and Table 3 locators | missing_formula | false | Administered-price formula must use canonical `rho_admin`, `alpha_a_fx`, `alpha_a_mc`; exact formula is not recorded. |
| EQ-PRICE-002 | ADMIN | BCB_WP239 locator | WP239 C.58 locator | missing_formula | false | Shock-process formula is located but not recorded exactly. |
| EQ-PRICE-003 | ADMIN | BCB_WP239 locator | WP239 Table 1 locator | not_required_for_mvp | false | Measurement/observable row; WBS-059 owns observables. |
| EQ-HH-001 | HH | BCB_WP239 locator | WP239 C.1-C.10 locators | missing_formula | false | Intertemporal household equations are located but not recorded exactly. |
| EQ-HH-002 | HH | BCB_WP239 locator | WP239 C.1-C.10 locators | missing_formula | false | Habit equation details are not recorded exactly. |
| EQ-HH-003 | HH | BCB_WP239 locator | WP239 C.1-C.10 locators | missing_formula | false | Labor/real-wage equation details are not recorded exactly. |
| EQ-HH-004 | HH | BCB_WP239 locator | WP239 rule-of-thumb household locators | missing_formula | false | Rule-of-thumb household equations are not recorded exactly. |
| EQ-FIRM-001 | FIRM | BCB_WP239 locator | WP239 C.11-C.27 locators | missing_formula | false | Production/marginal-cost equations are located but not recorded exactly. |
| EQ-FIRM-002 | FIRM | BCB_WP239 locator | WP239 C.11-C.27 locators | missing_formula | false | Phillips/markup equations are not recorded exactly. |
| EQ-FIRM-003 | FIRM | BCB_WP239 locator | WP239 C.11-C.27 locators | missing_formula | false | Investment/Tobin's Q equations are not recorded exactly. |
| EQ-FIRM-004 | FIRM | BCB_WP239 locator | WP239 C.11-C.27 locators | missing_formula | false | Imported input equations are not recorded exactly. |
| EQ-AGG-001 | AGG | BCB_WP239 locator | WP239 C.35-C.36 locators | missing_formula | false | Final goods market-clearing identities are not recorded exactly. |
| EQ-AGG-002 | AGG | BCB_WP239 locator | WP239 C.37-C.39 locators | missing_formula | false | Absorption/net-export accounting identities are not recorded exactly. |
| EQ-AGG-003 | AGG | BCB_WP239 locator | WP239 C.40-C.42 locators | missing_formula | false | GDP/GDP-deflator identities are not recorded exactly. |
| EQ-AGG-004 | AGG | BCB_WP239 locator; approved project decision | WP239 aggregation locators; STRUCT-001 | missing_formula | false | Output-gap/potential-output accounting needs exact formula before `.mod`. |
| EQ-SHOCK-001 | SHOCK | BCB_WP239 locator | WP239 C.60 locator | missing_formula | false | Shock process located, exact formula not recorded. |
| EQ-SHOCK-002 | SHOCK | approved project decision | docs/00b_modeling_decisions.md TARGET-001 | not_required_for_mvp | false | Inflation-target shock is off in calibrated MVP. |
| EQ-SHOCK-003 | SHOCK | BCB_WP239 locator | WP239 C.61 locator | missing_formula | false | Shock process located, exact formula not recorded. |
| EQ-SHOCK-004 | SHOCK | BCB_WP239 locator | WP239 C.31 locator | missing_formula | false | Primary-surplus-target shock source is located but formula not recorded. |
| EQ-SHOCK-005 | SHOCK | BCB_WP239 locator | WP239 C.32 locator | missing_formula | false | Tax shock source is located but formula not recorded. |
| EQ-SHOCK-006 | SHOCK | BCB_WP239 locator | WP239 C.51-C.52 locators | missing_formula | false | Technology shock process formulas are not recorded exactly. |
| EQ-SHOCK-007 | SHOCK | BCB_WP239 locator | WP239 C.48 locator | missing_formula | false | Preference shock formula is not recorded exactly. |
| EQ-SHOCK-008 | SHOCK | BCB_WP239 locator | WP239 C.53 locator | missing_formula | false | Investment shock formula is not recorded exactly. |
| EQ-SHOCK-009 | SHOCK | BCB_WP239 locator | WP239 C.57 locator | missing_formula | false | Free-price markup shock formula is not recorded exactly. |
| EQ-SHOCK-010 | SHOCK | BCB_WP239 locator | WP239 C.58 locator | missing_formula | false | Administered-price shock formula is not recorded exactly. |
| EQ-SHOCK-011 | SHOCK | BCB_WP239 locator | WP239 C.56 locator | missing_formula | false | Wage-markup shock formula is not recorded exactly. |
| EQ-SHOCK-012 | SHOCK | BCB_WP239 locator | WP239 C.44 locator | missing_formula | false | Import-price shock formula is not recorded exactly. |
| EQ-SHOCK-013 | SHOCK | approved project decision | docs/00b_modeling_decisions.md EXT-001 | sourced_project_decision | true | Risk AR(1) duplicates EQ-EXT-002 concept. |
| EQ-SHOCK-014 | SHOCK | BCB_WP239 locator | WP239 C.43 locator | missing_formula | false | Foreign-output shock formula is not recorded exactly. |
| EQ-SHOCK-015 | SHOCK | BCB_WP239 locator | WP239 C.47 locator | missing_formula | false | Foreign-interest shock formula is not recorded exactly. |
| EQ-SHOCK-016 | SHOCK | BCB_WP239 locator | WP239 C.45 locator | missing_formula | false | Foreign-inflation shock formula is not recorded exactly. |
| EQ-SHOCK-017 | SHOCK | registry deferred | source locator pending | not_required_for_mvp | false | Commodity shock remains deferred/out of MVP. |
| EQ-MEAS-001..EQ-MEAS-015 | MEAS | registry draft | WBS-043 measurement drafts | not_required_for_mvp | false | Measurement equations are WBS-059/observables work, not WBS-057. |

Current result: `samba_classic.mod` remains blocked because MVP-required rows still have `missing_formula`.
