# WBS-071 Posterior Mode Result

Status: `WBS-071_COMPLETED`

- Command: `python src/diagnostics/run_dynare.py --mode posterior-mode --timeout-seconds 900`.
- Runtime: temporary Dynare working directory; no committed Dynare clutter.
- Estimation settings: `mode_compute=4`, `mh_replic=0`, `diffuse_filter`, `kalman_algo=4`.
- Data: WBS-052 approved model input transformed according to WBS-059 mappings.
- Measurement treatment: WBS-070 source-backed GDP measurement error, stderr `0.08`, from WP239 Table 3 measurement errors.
- Result: posterior mode run completed with exit code 0.
- Elapsed time: `518.562` seconds.
- Finite result: log data density (Laplace approximation) `-456.997406`.
- No MH chain, pilot/full posterior sample, backtesting output, Redux file, or sovereign-extension file was created.
- Next WBS: WBS-071a estimation smoke test.
