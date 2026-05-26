# Calibration Blockers

Status: `BLOCKED_CALIBRATION_VALUES`
Blocked scope: `WBS-055 / PR11 calibration.m`
Reason: `docs/03_calibration_notes.md` has `calibration_values_approved: false` and no numeric values.
Missing MON values/rationale: `rho_r`, `phi_pi`, `phi_y`, `r_ss`; needed by Taylor-rule calibration; no approved default in docs.
Missing EXT values/rationale: `psi_nfa`, `nfa_ss`, `rho_risk`; needed by external closure/risk calibration; no approved default in docs.
Missing FISC values/rationale: `rho_sp_target`, `phi_b`, `phi_y_sp`, `sp_ss`; needed by fiscal target rule; no approved default in docs.
Missing ADMIN values/rationale: `rho_a`, `alpha_a_target`, `alpha_a_fx`, `alpha_a_m`, `rho_admin`; needed by administered-price process; no approved default in docs.
Missing HH/FIRM values/rationale: `habit`, `lambda`, `q_k`, `wn`, `mc`, `m_int`; needed by household/firm calibration scaffolds; no approved default in docs.
Missing shock std values/rationale: `eps_monetary`, `eps_fiscal_g`, `eps_sp_target`, `eps_tax`, `eps_tfp`, `eps_pref`, `eps_investment`, `eps_price_free`, `eps_admin`, `eps_wage`, `eps_import_price`, `eps_risk`, `eps_foreign_y`, `eps_foreign_r`, `eps_foreign_pi`.
Do not create `model/samba_classic/calibration.m` until Bruno approves numeric values and rationale in `docs/03_calibration_notes.md`.
