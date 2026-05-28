# WBS-057 Blockers

Status: `BLOCKED_WBS057_SYMBOL_MAPPING`

Formula text is transcribed, and true WBS-057 source/formula blockers are 0, but `samba_classic.mod` must not be created until all WP239 symbols have canonical project/Dynare mappings and sourced values.

Source checked: WP239 Appendix C, WP239 Tables 2-3, equation registry, calibration notes, `calibration.m`, and `steady_state.m`.

Remaining unresolved symbol rows: 26.

- Missing canonical names: `cO_t`, `sB_t`, `zQ_t`, `piF_t`, `piH_t`, `piM_t`, `piX_t`, `vF_t`, `vH_t`, `vM_t`, `vX_t`.
- Missing sourced values: `rho_Q`, `rho_C`, `rho_Z`, `rho_I`, `rho_D`, `rho_M`, `rho_P`, `theta_A`, `chi_A`.
- Ambiguous symbols: `qF_t`, `qG_t`, `qI_t`, `qMstar_t`, `qXstar_t`, `zM_t`.

Deferred to WBS-058 `shocks.inc`: 11 rows.

Deferred to WBS-059 `observables.inc`: 0 rows among the 27 unresolved WBS-057a items.

Exact missing mapping/value: canonical Dynare names and/or sourced parameter values for the rows above.
Next task: resolve these symbol mappings before any `.mod`, `.inc`, output, data, estimation, Redux, or sovereign work.
