# WBS-070 Finite Likelihood Blocker

Status: `RESOLVED_WBS070_LIKELIHOOD_FINITE`

- WBS-070 attempted a temporary Dynare likelihood smoke run through `src/diagnostics/run_dynare.py --mode likelihood-smoke`.
- Data source: `data/model_input/classic_mvp.csv`.
- Temporary transformations used only documented WBS-059 mappings: first log-difference and demean for `y,c,i,g`; percent deviation from sample mean for `q`; demeaned level for `r_t`.
- Diagnostic cause: the NaN appears only when `y,c,i,g` are observed together, while all singletons, pairs, and triples from that block produce finite likelihood values.
- Interpretation: mechanical stochastic singularity in the national-accounts measurement block, not empty data, NaN/Inf data, invalid priors, or missing `varobs`.
- Source-backed fix: add a temporary WBS-070 likelihood-smoke measurement error for observed `y` using WP239 Table 3 GDP measurement error `epsilon_Y_me = 0.08`.
- Dynare command uses the WBS-069 `priors.inc`, `mode_compute=0`, `mh_replic=0`, `diffuse_filter`, `kalman_algo=4`, and the temporary `y` measurement error.
- Result: finite initial log posterior/likelihood in the temporary smoke run.
- No posterior, MH, backtesting, Redux, or sovereign files were created.
- WBS-070 pass condition is satisfied for finite likelihood only; WBS-071 posterior mode remains a separate next WBS.
