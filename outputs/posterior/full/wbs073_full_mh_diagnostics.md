# WBS-073 Full MH Diagnostics

Status: failed.

Command: `python src/diagnostics/run_dynare.py --mode full-mh --timeout-seconds 43200`

Configuration:
- `mh_replic`: 20000 per chain
- chains: 4
- Dynare `mh_nblocks`: 4
- approved blocks metadata: 2
- burn-in: 0.5
- `mh_jscale`: 0.337313
- timeout seconds: 43200

Observed failure:
- wrapper return code: 124
- elapsed seconds: 43200
- failure: approved timeout reached before full-MH diagnostics completed
- stdout tail: convergence diagnostics progressed through parameter 28
- R-hat status: unavailable timeout

This is a WBS-073 blocker. It is not final publication-grade posterior
evidence. WBS-074, backtesting, Redux, and sovereign-extension work remain
forbidden until WBS-073 is resolved and reviewed.
