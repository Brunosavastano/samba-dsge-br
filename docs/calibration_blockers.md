# Calibration Blockers

Status: `BLOCKED_CALIBRATION_SOURCES`
Blocked scope: `WBS-055 / PR11 calibration.m`
Reference checked: BCB WP239 official PDF, SHA256 `8EC1FCF4CC37CEE968C4BF8D23D92DBE537F0401A25CA509BEFA84D8E0C1325E`.
Reason: most WBS-055 parameters in WP239 are estimated/posterior values, not calibrated values.
Sourced SAMBA calibration values: 2 (`r_ss`, `nfa_ss`).
Remaining `missing_source` count: 2 (`sp_ss`, `alpha_a_target`).
`estimated_not_calibrated` count: 9 (`rho_r`, `phi_pi`, `phi_y`, `psi_nfa`, `rho_risk`, `rho_sp_target`, `phi_b`, `alpha_a_fx`, `rho_admin`).
Naming conflicts: 3 (`phi_y_sp`, `rho_a`, `alpha_a_m`).
`rho_a` versus `rho_admin` remains unresolved because WP239 has `rho_A` for administered-price shock persistence, not a separate approved `rho_a`.
Do not create `model/samba_classic/calibration.m` until missing sources are zero, estimated parameters have an approved MVP treatment, and naming conflicts are resolved.
