# WBS-070 Finite Likelihood Blocker

Status: `BLOCKED_WBS070_LIKELIHOOD_NAN`

- WBS-070 attempted a temporary Dynare likelihood smoke run through `src/diagnostics/run_dynare.py --mode likelihood`.
- Data source: `data/model_input/classic_mvp.csv`.
- Temporary transformations used only documented WBS-059 mappings: first log-difference and demean for `y,c,i,g`; percent deviation from sample mean for `q`; demeaned level for `r_t`.
- Dynare command used the WBS-069 `priors.inc`, `mode_compute=0`, `mh_replic=0`, `diffuse_filter`, and `kalman_algo=4`.
- Result: Dynare returned `Likelihood is not a number (NaN)` during initial estimation checks.
- No posterior, MH, backtesting, Redux, or sovereign files were created.
- WBS-070 remains blocked until the NaN source is resolved with a source-backed measurement/data/filter treatment.
- Do not proceed to WBS-071 posterior mode.
