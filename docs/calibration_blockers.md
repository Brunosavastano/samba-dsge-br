# Calibration Blockers

Status: `BLOCKED_CALIBRATION_SOURCES`
Blocked scope: `WBS-055 / PR11 calibration.m`
Reason: calibration values must be sourced from SAMBA/public documentation, not defaults or memory.
Missing source count: 16 MVP-required parameters currently identified in `docs/01_equation_registry.md`.
Missing MON sources: `rho_r`, `phi_pi`, `phi_y`, `r_ss`.
Missing EXT sources: `psi_nfa`, `nfa_ss`, `rho_risk`.
Missing FISC sources: `rho_sp_target`, `phi_b`, `phi_y_sp`, `sp_ss`.
Missing ADMIN sources: `rho_a`, `alpha_a_target`, `alpha_a_fx`, `alpha_a_m`, `rho_admin`.
Ambiguity blocker: verify whether `rho_a` and `rho_admin` are distinct administered-price parameters or duplicate names.
`source_to_check` references in `docs/03_calibration_notes.md` are not confirmed numeric sources.
Do not create `model/samba_classic/calibration.m` until `missing_source` count is zero and the `rho_a`/`rho_admin` ambiguity is resolved.
