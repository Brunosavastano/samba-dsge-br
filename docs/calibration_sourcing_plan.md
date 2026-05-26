# Calibration Sourcing Plan

Status: `BLOCKED_CALIBRATION_SOURCES`

WBS-055 remains blocked until numeric calibration values are sourced from SAMBA/public documentation or approved project decisions. No generic New Keynesian defaults, provisional engineering values, or memory-derived values are allowed.

## Missing sources

| parameter | block | exact source needed | source_to_check |
|---|---|---|---|
| rho_r | MON | Numeric SAMBA/project value and locator | BCB_WP239 monetary policy rule and appendix locators from LM-MON-001 |
| phi_pi | MON | Numeric SAMBA/project value and locator | BCB_WP239 monetary policy rule and appendix locators from LM-MON-001 |
| phi_y | MON | Numeric SAMBA/project value and locator | BCB_WP239 monetary policy rule and appendix locators from LM-MON-001 |
| r_ss | MON | Numeric SAMBA/project value and locator | BCB_WP239 monetary policy rule and appendix locators from LM-MON-001 |
| psi_nfa | EXT | Numeric SAMBA/project value and locator | BCB_WP239 external sector and NFA/risk-premium locators from LM-EXT-001 |
| nfa_ss | EXT | Numeric SAMBA/project value and locator | BCB_WP239 external sector and NFA/risk-premium locators from LM-EXT-001 |
| rho_risk | EXT | Numeric SAMBA/project value and locator | BCB_WP239 risk-premium AR(1) locator from LM-EXT-001 |
| rho_sp_target | FISC | Numeric SAMBA/project value and locator | BCB_WP239 fiscal rule locators from LM-FISC-001 |
| phi_b | FISC | Numeric SAMBA/project value and locator | BCB_WP239 fiscal rule locators from LM-FISC-001 |
| phi_y_sp | FISC | Numeric SAMBA/project value and locator | BCB_WP239 fiscal rule locators from LM-FISC-001 |
| sp_ss | FISC | Numeric SAMBA/project value and locator | BCB_WP239 fiscal rule locators from LM-FISC-001 |
| rho_a | ADMIN | Numeric SAMBA/project value and locator; distinctness versus `rho_admin` | BCB_WP239 administered-price locators from LM-PRICE-ADMIN-001 |
| alpha_a_target | ADMIN | Numeric SAMBA/project value and locator | BCB_WP239 administered-price locators from LM-PRICE-ADMIN-001 |
| alpha_a_fx | ADMIN | Numeric SAMBA/project value and locator | BCB_WP239 administered-price locators from LM-PRICE-ADMIN-001 |
| alpha_a_m | ADMIN | Numeric SAMBA/project value and locator | BCB_WP239 administered-price locators from LM-PRICE-ADMIN-001 |
| rho_admin | ADMIN | Numeric SAMBA/project value and locator; distinctness versus `rho_a` | BCB_WP239 administered-price shock locator from EQ-PRICE-002 |

## Source review rules

- Treat BCB_WP239 as the primary source for classic SAMBA MVP calibration.
- Use BCB_WP578 only to confirm non-MVP Redux boundaries unless a later approved decision expands its role.
- If a parameter value is not explicitly found, keep `value`, `source`, and `source_location` blank and leave status `missing_source`.
- If `rho_a` and `rho_admin` are duplicates, update the registry/calibration notes before creating `calibration.m`.
