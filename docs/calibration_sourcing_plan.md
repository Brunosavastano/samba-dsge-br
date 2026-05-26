# Calibration Sourcing Plan

Status: `WBS-055_READY_FOR_CALIBRATION_M`

WBS-055 source taxonomy is ready for `calibration.m`. No generic New Keynesian defaults, provisional engineering values, or memory-derived values are allowed.

## Reference record

- Official source: https://www.bcb.gov.br/pec/wps/ingl/wps239.pdf
- Local file: `docs/references/bcb_wp239_samba.pdf`
- SHA256: `8EC1FCF4CC37CEE968C4BF8D23D92DBE537F0401A25CA509BEFA84D8E0C1325E`
- Search method: downloaded the official PDF, extracted text with local PDF tools, and rendered relevant pages because several equation/table symbols are encoded as glyph names in plain text.
- Checked locations: Table 2 calibrated parameters, Table 3 estimated parameters, Appendix C.6 shock processes, and Section 2.5 shock process discussion.

## Source status after WP239 taxonomy refinement

| status | count | parameters |
|---|---:|---|
| sourced_from_samba_calibration | 2 | `r_ss`, `nfa_ss` |
| sourced_from_samba_posterior_mean | 10 | `rho_r`, `phi_pi`, `phi_y`, `psi_nfa`, `rho_risk`, `rho_sp_target`, `phi_b`, `alpha_a_fx`, `alpha_a_mc`, `rho_admin` |
| not_required_for_mvp | 5 | `phi_y_sp`, `sp_ss`, `rho_a`, `alpha_a_target`, `alpha_a_m` |
| missing_source | 0 | none |
| estimated_in_samba_no_point_value_found | 0 | none |
| naming_conflict | 0 | none |

## Resolved mappings

| item | resolution |
|---|---|
| posterior means | Explicit WP239 Table 3 posterior means are allowed as MVP baseline assignments only when copied with source and locator. |
| `rho_sp_target` | Maps to WP239 `rho_S` posterior mean 0.76, not to `phi_bar_S`. |
| `phi_y_sp` | Not required for the WP239 classic MVP because C.31 has no output-gap term. |
| `sp_ss` | Not required for WBS-055 because C.31 is log-linear and has no intercept. |
| `rho_a` | Deprecated alias; canonical project name is `rho_admin`, mapped to WP239 `rho_A`. |
| `alpha_a_target` | Not required for the WP239 classic MVP because no target pass-through coefficient was found. |
| `alpha_a_m` | Deprecated imported-inflation mapping; WP239 Table 3 uses marginal-cost coefficient `vartheta_A_2`, mapped to `alpha_a_mc`. |

## Remaining source work

No unresolved WBS-055 calibration source blockers remain. The next task is to implement `model/samba_classic/calibration.m` using only rows in `docs/03_calibration_notes.md` where `usable_in_mvp_calibration_m` is `true`.

## Source review rules

- Treat BCB_WP239 as the primary source for classic SAMBA MVP calibration.
- Use BCB_WP578 only to confirm non-MVP Redux boundaries unless a later approved decision expands its role.
- If a parameter value is not explicitly found and the parameter remains required, keep `value`, `source`, and `source_location` blank and leave status `missing_source`.
- If WP239 reports a posterior mean or mode and the row is marked usable, copy only that point value with status `sourced_from_samba_posterior_mean` or `sourced_from_samba_posterior_mode`.
- Do not call posterior mean rows calibrated Table 2 values.
