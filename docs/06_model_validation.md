---
status: template
do_not_treat_as_validation_result: true
wbs: WBS-020
data_created: false
results_created: false
---

# Model Validation - samba-dsge-br

This document is a template. It is not a validation result and does not approve the model.

## Required future sections

```text
- calibrated and posterior IRFs versus replication targets;
- moment comparison;
- variance decomposition;
- historical decomposition;
- pseudo out-of-sample validation;
- AR(1), VAR/BVAR, and Focus benchmarks when available;
- RMSE, MAE, and CRPS;
- horizons 1, 4, 8, and 12.
```

## Gate policy

```yaml
validation_approved: false
earliest_validation_result_gate: Gate 6
requires_estimation_outputs: true
requires_backtesting_outputs: true
no_result_invention: true
```
