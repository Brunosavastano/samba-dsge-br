# WBS-059 Observable Sourcing

Status: `BLOCKED_WBS059_MEASUREMENT_MAPPING`

Scope: WBS-059 only. This file reviews whether approved Gate 1b data can be mapped into `model/samba_classic/observables.inc`. It does not authorize priors, estimation, outputs, Redux, or sovereign files.

## Decision

No observable is currently marked `usable_in_observables_inc`.

The WBS-052 dataset exists, but the current data columns are levels, decimal rates, annual percent rates, or index averages while the WBS-057 model is log-linear around deterministic steady state. Direct `varobs` would require finalized measurement equations and scaling/deviation transforms. The registry still marks measurement rows as `measurement_draft` with `measurement_transform_pending_gate1b`.

| observable_id | data column or series name | model variable | measurement equation id | transformation | status | notes |
|---|---|---|---|---|---|---|
| br_gdp_real | y | y | EQ-MEAS-001 | real activity level to model log-deviation/growth not finalized | missing_mapping | Data exists in WBS-052; direct `varobs y` is not approved because the model variable is a log-linear deviation. |
| br_ipca_headline | pi | pi | EQ-MEAS-002 | monthly compounded quarterly decimal rate to model inflation deviation not finalized | missing_mapping | Data exists in WBS-052; `pi` is currently exogenous in the `.mod`, not an endogenous observable. |
| br_selic | r | r_t | EQ-MEAS-003 | annual percent-rate level to model policy-rate deviation not finalized | missing_mapping | Data exists in WBS-052; direct `varobs r_t` is not approved without scaling/deviation mapping. |
| br_real_exchange_rate | q | q | EQ-MEAS-004 | real exchange-rate index average to model log-deviation not finalized | missing_mapping | Data exists in WBS-052; direct mapping needs log/deviation treatment and sign convention confirmation. |
| br_private_consumption | c | c | EQ-MEAS-005 | real activity level to model log-deviation/growth not finalized | missing_mapping | Data exists in WBS-052; direct `varobs c` is not approved. |
| br_investment | i | i | EQ-MEAS-006 | real activity level to model log-deviation/growth not finalized | missing_mapping | Data exists in WBS-052; direct `varobs i` is not approved. |
| br_government_consumption | g | g | EQ-MEAS-007 | real activity level to model log-deviation/growth not finalized | missing_mapping | Data exists in WBS-052; direct `varobs g` is not approved. |
| br_exports | x | x | EQ-MEAS-008 | real activity level to model log-deviation/growth not finalized | missing_mapping | Data exists in WBS-052; `x` is currently exogenous in the `.mod`, so direct `varobs` is not safe. |
| br_imports | m | m | EQ-MEAS-009 | real activity level to model log-deviation/growth not finalized | missing_mapping | Data exists in WBS-052; `m` is currently exogenous in the `.mod`, so direct `varobs` is not safe. |
| br_ipca_free | br_ipca_free | pi_f | EQ-MEAS-010 | monthly inflation to model sectoral inflation deviation not finalized | missing_data | Source is verified, but no WBS-052 data file exists for this auxiliary series. |
| br_ipca_administered | br_ipca_administered | pi_a | EQ-MEAS-011 | monthly inflation to model administered inflation deviation not finalized | missing_data | Source is verified, but no WBS-052 data file exists for this auxiliary series. |
| br_import_price_inflation | br_import_price_inflation | pi_m | EQ-MEAS-012 | source and inflation transform not finalized | missing_data | Source remains TBD in the data dictionary. |
| br_inflation_target | br_inflation_target | pi_target | EQ-MEAS-013 | target source and deterministic/exogenous measurement not finalized | missing_data | Source remains TBD in the data dictionary. |
| br_risk_premium | br_risk_premium | risk | EQ-MEAS-014 | risk proxy source and deviation transform not finalized | missing_data | Source remains TBD in the data dictionary. |
| br_output_gap | br_output_gap | y_gap | EQ-MEAS-015 | output-gap measurement equation not finalized | missing_data | Source remains TBD; `y_gap` measurement is explicitly future work. |

## Requirement to unblock

Before `observables.inc` can be created, each selected observable needs a finalized measurement mapping from the approved data column to a declared Dynare endogenous model variable, including scaling and deviation/log transformation.
