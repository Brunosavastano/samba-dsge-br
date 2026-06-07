# WBS-057 Blockers

Status: `WBS-057_COMPLETED`

Formula text, symbol mappings, and WBS-057 administered-price parameters are sourced.

Remaining true WBS-057 source blockers: 0.

Remaining executable formula-text blockers: 0.

Remaining WBS-057 symbol blockers: 0.

Deferred to WBS-058 shock processes: `rho_z_q`, `rho_z_c`, `rho_z_z`, `rho_z_i`, `rho_z_d`, `rho_z_m`, `rho_z_p`; shock states `z_q` and `z_m` may appear in WBS-057 equations.

Deferred to WBS-059 observables: 0 rows among the WBS-057 symbol blockers.

WBS-057 artifact created: `model/samba_classic/samba_classic.mod`.

Dynare parse: passed in a temporary directory with `dynare samba_classic.mod noclearall nolog`.

Next task: WBS-058 `shocks.inc`; do not create `observables.inc`, outputs, data, estimation, Redux, or sovereign work.
