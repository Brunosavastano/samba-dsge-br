# WBS-058 Blockers

Status: `BLOCKED_WBS058_SHOCK_STD_VALUES`

WBS-058 remains blocked. `model/samba_classic/shocks.inc` was not created.

Required sourced standard deviations or variances are missing for:

- `eps_monetary`
- `eps_risk`
- `eps_sp_target`
- `eps_tax`
- `eps_admin`

Deferred WBS-058 shock-state processes also lack sourced standard deviations: `z_q`, `z_c`, `z_z`, `z_i`, `z_d`, `z_m`, and `z_p`.

Exact source needed: WP239/SAMBA public reference or approved project document with numeric standard deviation or variance values for each WBS-058 shock declaration.

Next action: source shock standard deviations before creating `shocks.inc`.
