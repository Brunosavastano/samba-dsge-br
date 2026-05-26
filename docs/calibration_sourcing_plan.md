# Calibration Sourcing Plan

Status: `BLOCKED_CALIBRATION_SOURCES`

WBS-055 remains blocked until numeric calibration values are sourced from SAMBA/public documentation or approved project decisions. No generic New Keynesian defaults, provisional engineering values, or memory-derived values are allowed.

## Reference record

- Official source: https://www.bcb.gov.br/pec/wps/ingl/wps239.pdf
- Local file: `docs/references/bcb_wp239_samba.pdf`
- SHA256: `8EC1FCF4CC37CEE968C4BF8D23D92DBE537F0401A25CA509BEFA84D8E0C1325E`
- Search method: downloaded the official PDF, extracted text with local PDF tools, and rendered relevant pages because several equation/table symbols are encoded as glyph names in plain text.
- Checked locations: Table 2 calibrated parameters, Table 3 estimated parameters, Appendix C.6 shock processes, and Section 2.5 shock process discussion.

## Source status after WP239 check

| status | count | parameters |
|---|---:|---|
| sourced_from_samba | 2 | `r_ss`, `nfa_ss` |
| estimated_not_calibrated | 9 | `rho_r`, `phi_pi`, `phi_y`, `psi_nfa`, `rho_risk`, `rho_sp_target`, `phi_b`, `alpha_a_fx`, `rho_admin` |
| missing_source | 2 | `sp_ss`, `alpha_a_target` |
| naming_conflict | 3 | `phi_y_sp`, `rho_a`, `alpha_a_m` |

## Remaining source work

| parameter | blocker type | exact source or decision needed | source_to_check |
|---|---|---|---|
| sp_ss | missing_source | Calibrated primary-surplus steady-state value or approved project treatment | BCB WP239 fiscal block, SAMBA classic supplementary material, or project decision |
| alpha_a_target | missing_source | Administered-price target pass-through coefficient or approved decision to remove from MVP calibration | BCB WP239 administered-price rule, SAMBA classic supplementary material, or project decision |
| phi_y_sp | naming_conflict | Confirm whether project `phi_y_sp` maps to WP239 `phi_S`, or rename/change registry role | BCB WP239 fiscal rule equations and Table 3 |
| rho_a | naming_conflict | Confirm whether `rho_a` is distinct from `rho_admin`; otherwise update registry to avoid duplicate persistence names | BCB WP239 Appendix C.6 C.58 and administered-price rule |
| alpha_a_m | naming_conflict | Confirm whether project imported-inflation pass-through maps to another SAMBA term or should be replaced by WP239 marginal-cost coefficient | BCB WP239 administered-price rule and Table 3 |

## Source review rules

- Treat BCB_WP239 as the primary source for classic SAMBA MVP calibration.
- Use BCB_WP578 only to confirm non-MVP Redux boundaries unless a later approved decision expands its role.
- If a parameter value is not explicitly found, keep `value`, `source`, and `source_location` blank and leave status `missing_source`.
- If WP239 reports a parameter under priors/posteriors/estimated parameters, mark it `estimated_not_calibrated` and do not copy the posterior or prior mean into `calibration.m`.
- If `rho_a` and `rho_admin` are duplicates, update the registry/calibration notes before creating `calibration.m`.
