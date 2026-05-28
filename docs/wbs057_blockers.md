# WBS-057 Blockers

Status: `BLOCKED_WBS057_SYMBOL_MAPPING`

Assistant-reviewed symbol mappings were applied, but `samba_classic.mod` must not be created until WBS-057 parameter values are sourced.

Source checked: WP239 Appendix C, WP239 Tables 2-3, equation registry, calibration notes, `calibration.m`, and `steady_state.m`.

Remaining WBS-057 symbol blockers: 2.

- `theta_admin`: maps from WP239 `theta_A`, but no sourced numeric value exists in `docs/03_calibration_notes.md` or `calibration.m`.
- `chi_admin`: maps from WP239 `chi_A`, but no sourced numeric value exists in `docs/03_calibration_notes.md` or `calibration.m`.

Deferred to WBS-058 shock processes: `rho_z_q`, `rho_z_c`, `rho_z_z`, `rho_z_i`, `rho_z_d`, `rho_z_m`, `rho_z_p`; shock states `z_q` and `z_m` may appear in WBS-057 equations.

Deferred to WBS-059 observables: 0 rows among the WBS-057 symbol blockers.

Next task: source or formally defer `theta_admin` and `chi_admin` before any `.mod`, `.inc`, output, data, estimation, Redux, or sovereign work.
