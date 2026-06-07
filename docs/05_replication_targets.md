---
status: template
wbs: WBS-020
do_not_treat_as_validation_result: true
data_created: false
results_created: false
---

# Replication Targets - samba-dsge-br

This document is a template. It does not approve replication targets, data, model results, priors, or calibration values.

WBS-063 adds a narrow set of source-backed calibrated-MVP IRF restrictions in
`docs/wbs063_irf_targets.md`. These are not Gate 6 replication targets and do not
approve posterior IRF, moment, validation, backtesting, Redux, or sovereign work.

## Target schema

Every future target row must include:

```csv
target_id,target_type,model_object,shock_or_moment,expected_sign,timing_window,magnitude_band,benchmark_source,status,gate
```

Required IRF fields:

```text
- expected_sign
- timing_window
- magnitude_band
- benchmark_source
```

## Gate policy

```yaml
targets_approved: false
wbs063_mvp_irf_targets_approved: true
earliest_target_fill_wbs: WBS-074
requires_gate3_model_outputs: true
no_source_or_result_invention: true
```
