# WBS-071a Estimation Smoke Test

Status: `WBS-071a_COMPLETED`

WBS-071a ran the SAMBA classic estimation smoke path through
`src/diagnostics/run_dynare.py --mode estimation-smoke --timeout-seconds 240`.
The run used a temporary Dynare working directory, WBS-069 priors, WBS-070
measurement treatment, and `mh_replic=0`.

Result:
- status: passed
- mode_compute: 0
- mh_replic: 0
- observation count: 67
- observable columns: `y`, `c`, `i`, `g`, `q`, `r_t`
- finite likelihood reported: true
- nonfinite likelihood values: 0
- last finite log posterior or likelihood: -4472.9048

Artifact:
- `outputs/posterior/smoke/wbs071a_estimation_smoke.json`

No MH chain, pilot/full posterior sample, posterior mode output, backtesting
output, Redux file, or sovereign-extension file was created by WBS-071a.
