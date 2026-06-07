# WBS-058 Shock Sourcing

Status: `WBS-058_COMPLETED`

Scope: WBS-058 only. This file tracks WP239 Table 3 posterior means used as Dynare `stderr` values in `model/samba_classic/shocks.inc`. It does not authorize `observables.inc`, priors, data, outputs, estimation, Redux, or sovereign extensions.

Source for all usable rows below: WP239 Table 3, p. 98.

| wp239_symbol | dynare_shock_name | process/state variable | standard deviation | source | source_location | status | usable_in_shocks_inc | notes |
|---|---|---|---:|---|---|---|---|---|
| epsilon_B | risk_dom | risk_dom | 0.57 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Domestic risk-premium wedge used directly by WBS-057 shell. |
| epsilon_I | z_i | z_i | 3.54 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Investment shock state used in WBS-057 equations. |
| epsilon_C | z_c | z_c | 8.80 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Preference shock state used in WBS-057 equations. |
| epsilon_A | eps_admin | z_a | 1.40 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Administered-price innovation in the current model. |
| epsilon_P | z_p | z_p | 0.79 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Price-markup shock state used in WBS-057 equations. |
| epsilon_PiC | pi | pi | 0.14 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | CPI inflation is a current WBS-057 exogenous input. |
| epsilon_W | z_w | z_w | 1.38 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Wage-markup shock state used in WBS-057 equations. |
| epsilon_Z | z_z | z_z | 0.17 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Trend/permanent-technology shock state used in WBS-057 equations. |
| epsilon_Q | z_q | z_q | 0.80 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Real-exchange-rate shock state used in WBS-057 equations. |
| epsilon_Bstar | eps_risk | risk | 0.38 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Country risk-premium innovation. |
| epsilon_G | z_g | z_g | 1.73 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Government-spending shock state used in WBS-057 equations. |
| epsilon_T | eps_tax | tax_rate | 0.48 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Tax-rate innovation. |
| epsilon_Sbar | eps_sp_target | sp_target | 0.29 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Primary-surplus target innovation. |
| epsilon_R | eps_monetary | z_r | 0.32 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Monetary-policy innovation. |
| epsilon_Pstar | z_px | z_px | 3.89 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Export-price shock term used in WBS-057 equations. |
| epsilon_Pistar | pi_star | pi_star | 0.85 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Foreign inflation exogenous input used in WBS-057 equations. |
| epsilon_Rstar | r_star | r_star | 0.19 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Foreign interest-rate exogenous input used in WBS-057 equations. |
| epsilon_QMstar | q_m_star | q_m_star | 1.85 | BCB_WP239 | WP239 Table 3, p. 98 | sourced_from_samba_posterior_mean_for_shock_stderr | true | Foreign-currency import-price relative-price input used in WBS-057 equations. |

## WP239 shocks not used in current WBS-058 declarations

| wp239_symbol | value | status | notes |
|---|---:|---|---|
| epsilon_M | 9.01 | not_required_for_current_wbs058 | Current WBS-057 shell does not declare `z_m` as a Dynare exogenous shock. |
| epsilon_D | 1.13 | not_required_for_current_wbs058 | Current WBS-057 shell does not declare `z_d` as a Dynare exogenous shock. |
| epsilon_Ystar | 2.87 | not_required_for_current_wbs058 | Foreign output shock is not used by the current WBS-057 shell. |
| epsilon_Vstar | 6.54 | not_required_for_current_wbs058 | Foreign risk-aversion shock is not used by the current WBS-057 shell. |
| epsilon_Mstar | 18.73 | not_required_for_current_wbs058 | Foreign imports shock is not used by the current WBS-057 shell. |
| epsilon_Iest | 0.69 | not_required_for_current_wbs058 | Not required by current WBS-057 shell. |
| epsilon_Y_me | 0.08 | not_required_for_current_wbs058 | Measurement error; WBS-059/measurement work only if required later. |
| epsilon_PiC_me | 0.12 | not_required_for_current_wbs058 | Measurement error; WBS-059/measurement work only if required later. |

## WBS-058 decision

`model/samba_classic/shocks.inc` uses only the WP239 Table 3 posterior means mapped above as Dynare `stderr` values. No priors, observables, data, outputs, estimation, Redux, or sovereign files are created by WBS-058.
