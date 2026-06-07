# WBS-059 Observable Sourcing

Status: `WBS-059_COMPLETED`

Scope: WBS-059 only. This file maps assistant-verified WP239 Section 3.1 observables to the current SAMBA classic MVP model. It does not authorize priors, estimation, outputs, Redux, or sovereign files.

Source guidance: WP239 Section 3.1 "Data and shocks". Nonstationary real variables are first log-differenced and demeaned; level/rate variables are demeaned; the real effective exchange rate is a percent difference from its sample mean; CPI-related inflation rates subtract the inflation target; import relative price is linearly detrended. Measurement errors are not added in WBS-059.

## Observable mapping

| observable_id | WP239 observable description | canonical model variable | data dictionary entry | transformation/scaling | measurement equation id | status | notes |
|---|---|---|---|---|---|---|---|
| br_gdp_real | GDP growth | y | br_gdp_real | first log-difference, demeaned | EQ-MEAS-001 | usable_in_observables_inc | Endogenous model variable exists and WBS-052 data exists. |
| br_private_consumption | household consumption growth | c | br_private_consumption | first log-difference, demeaned | EQ-MEAS-005 | usable_in_observables_inc | Endogenous model variable exists and WBS-052 data exists. |
| br_investment | investment growth | i | br_investment | first log-difference, demeaned | EQ-MEAS-006 | usable_in_observables_inc | Endogenous model variable exists and WBS-052 data exists. |
| br_government_consumption | government consumption growth | g | br_government_consumption | first log-difference, demeaned | EQ-MEAS-007 | usable_in_observables_inc | Endogenous model variable exists and WBS-052 data exists. |
| br_real_exchange_rate | real effective exchange rate | q | br_real_exchange_rate | percent difference from sample mean; q up means BRL real depreciation | EQ-MEAS-004 | usable_in_observables_inc | Endogenous model variable exists and WBS-052 data exists. |
| br_selic | nominal policy interest rate | r_t | br_selic | demeaned level or deviation from steady state | EQ-MEAS-003 | usable_in_observables_inc | Data dictionary variable `r` maps to model policy-rate variable `r_t`. |
| br_exports | exports growth | x | br_exports | first log-difference, demeaned | EQ-MEAS-008 | missing_model_variable | Current `.mod` declares `x` as `varexo`, so it is not used in `varobs`. |
| br_imports | imports growth | m | br_imports | first log-difference, demeaned | EQ-MEAS-009 | missing_model_variable | Current `.mod` declares `m` as `varexo`, so it is not used in `varobs`. |
| br_ipca_headline | CPI inflation | pi | br_ipca_headline | inflation relative to `pi_target` | EQ-MEAS-002 | missing_model_variable | Current `.mod` declares `pi` as `varexo`; no measurement error added in WBS-059. |
| br_employment | employed people growth | labor | none | first log-difference, demeaned | none | missing_data_mapping | Model has `labor`, but no data dictionary/source entry is approved. |
| br_real_wage | real wage growth | wn | none | first log-difference, demeaned | none | missing_data_mapping | Model has `wn`, but no data dictionary/source entry is approved. |
| br_risk_premium | country risk premium | risk | br_risk_premium | demeaned level | EQ-MEAS-014 | missing_data_mapping | Data dictionary source remains TBD. |
| br_inflation_target | inflation target | pi_target | br_inflation_target | demeaned or target-deviation mapping | EQ-MEAS-013 | missing_model_variable | Current `.mod` declares `pi_target` as `varexo`; data dictionary source remains TBD. |
| br_ipca_free | free price inflation | pi_f | br_ipca_free | inflation relative to `pi_target` | EQ-MEAS-010 | missing_data_mapping | Source is verified, but WBS-052 did not generate this data file. |
| br_ipca_administered | administered price inflation | pi_a | br_ipca_administered | inflation relative to `pi_target` | EQ-MEAS-011 | missing_data_mapping | Source is verified, but WBS-052 did not generate this data file. |
| br_export_price_inflation | export price inflation | pi_x | none | inflation transform to be finalized | none | missing_data_mapping | Model variable exists, but no data dictionary/source entry is approved. |
| br_primary_surplus | primary surplus-to-GDP | sp | none | demeaned level or GDP-ratio deviation | none | missing_data_mapping | Model variable exists, but no data dictionary/source entry is approved. |
| br_primary_surplus_target | primary surplus target-to-GDP | sp_target | none | demeaned level or GDP-ratio target deviation | none | missing_data_mapping | Model variable exists, but no data dictionary/source entry is approved. |
| world_imports_growth | world imports growth | none | none | first log-difference, demeaned | none | missing_model_variable | No canonical `y_star` or world import demand endogenous variable exists in the current `.mod`. |
| br_import_price_inflation | relative price of imports | q_m_star | br_import_price_inflation | linear detrend | EQ-MEAS-012 | missing_model_variable | Current `.mod` declares `q_m_star` as `varexo`; data dictionary source remains TBD. |
| foreign_inflation | foreign/world inflation | pi_star | none | demeaned level | none | missing_model_variable | Current `.mod` declares `pi_star` as `varexo`; no data dictionary entry is approved. |
| foreign_risk_aversion | foreign investor risk aversion | none | none | demeaned level | none | missing_model_variable | No canonical `risk_global` or `v_star` variable exists in the current `.mod`. |
| foreign_interest_rate | foreign/world nominal interest rate | r_star | none | demeaned level | none | missing_model_variable | Current `.mod` declares `r_star` as `varexo`; no data dictionary entry is approved. |

## WBS-059 include

`model/samba_classic/observables.inc` contains only:

```text
varobs y c i g q r_t;
```

These declarations are for the first MVP smoke/pilot layer. They do not create data, do not add measurement errors, and do not start estimation.
