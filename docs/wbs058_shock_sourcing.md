# WBS-058 Shock Sourcing

Status: `BLOCKED_WBS058_SHOCK_STD_VALUES`

Scope: WBS-058 only. This file tracks shock declarations needed before creating `model/samba_classic/shocks.inc`. It does not authorize `observables.inc`, priors, data, outputs, estimation, Redux, or sovereign extensions.

## Current WBS-057 model shocks

These innovation shocks are used by `model/samba_classic/samba_classic.mod`. Each still lacks a sourced shock standard deviation or variance, so none is usable in `shocks.inc` yet.

| shock_name | process/state variable | persistence parameter | standard deviation parameter | source | source_location | usable_in_shocks_inc | notes |
|---|---|---|---|---|---|---|---|
| eps_monetary | z_r | none in WBS-057 model equation | std_pending_calibration | docs/01_equation_registry.md EQ-MON-003 and EQ-SHOCK-001; docs/03_calibration_notes.md Shock Standard Deviation Scaffold | WP239 Appendix C.6 equation C.60, PDF page 93 | false | Shock name and equation are sourced; standard deviation is not. |
| eps_risk | risk | rho_risk | std_pending_calibration | docs/01_equation_registry.md EQ-EXT-002 and EQ-SHOCK-013; docs/03_calibration_notes.md Shock Standard Deviation Scaffold | WP239 Appendix C.6 equation C.50, PDF page 92 | false | Persistence is sourced in calibration notes; standard deviation is not. |
| eps_sp_target | sp_target | rho_sp_target | std_pending_calibration | docs/01_equation_registry.md EQ-FISC-001 and EQ-SHOCK-004; docs/03_calibration_notes.md Shock Standard Deviation Scaffold | WP239 Appendix C.3 equation C.31, PDF page 89 | false | Persistence is sourced in calibration notes; standard deviation is not. |
| eps_tax | tax_rate | tax_rate_persistence | std_pending_calibration | docs/01_equation_registry.md EQ-FISC-004 and EQ-SHOCK-005; docs/03_calibration_notes.md WBS-057 formula parameter mappings and Shock Standard Deviation Scaffold | WP239 Appendix C.3 equation C.32, PDF page 89 | false | Persistence is sourced for WBS-057 mapping; standard deviation is not. |
| eps_admin | z_a | rho_admin | std_pending_calibration | docs/01_equation_registry.md EQ-PRICE-001, EQ-PRICE-002, and EQ-SHOCK-010; docs/03_calibration_notes.md Shock Standard Deviation Scaffold | WP239 Appendix C.6 equation C.58, PDF page 92 | false | Project model uses canonical `eps_admin`; the shock standard deviation remains unsourced. |

## Deferred shock-state processes

WBS-057 mapped these WP239 shock-state symbols but deferred their AR(1) process and variance work to WBS-058: `z_q`, `z_c`, `z_z`, `z_i`, `z_d`, `z_m`, and `z_p`, with persistence aliases `rho_z_q`, `rho_z_c`, `rho_z_z`, `rho_z_i`, `rho_z_d`, `rho_z_m`, and `rho_z_p`.

No sourced standard deviations are documented for these deferred processes in `docs/03_calibration_notes.md`, so they are not usable in `shocks.inc` yet.

## WBS-058 decision

`model/samba_classic/shocks.inc` must not be created until every shock declaration used by the WBS-057 model has a sourced standard deviation or variance and any remaining shock-name aliases are resolved in the registry.
