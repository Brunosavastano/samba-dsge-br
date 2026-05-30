# WBS-071 Posterior Mode Blocker

Status: `BLOCKED_WBS071_POSTERIOR_MODE_TIMEOUT`

- WBS-071 attempted `python src/diagnostics/run_dynare.py --mode posterior-mode --timeout-seconds 90`.
- The wrapper ran Dynare in a temporary directory, used WBS-069 `priors.inc`, WBS-070 temporary GDP measurement error, `mode_compute=4`, and `mh_replic=0`.
- Dynare did not report a completed posterior mode before the timeout.
- Last captured optimizer trace: iteration 63, objective improved to approximately `438.5052461`.
- This is not a failed likelihood, data-empty, NaN/Inf-data, or prior-domain issue; WBS-070 likelihood-smoke already passed.
- No `outputs/posterior/`, MH chain, backtesting, Redux, or sovereign files were created.
- The leftover `octave-cli` process from the timeout was manually terminated before commit.
- WBS-071 remains blocked until posterior mode optimization is completed or an approved optimizer/settings treatment is documented.
- Do not proceed to WBS-071a estimation smoke or WBS-072 MH pilot.
