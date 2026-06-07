# WBS-072 MH Pilot Diagnostics

Status: passed.

Command: `python src/diagnostics/run_dynare.py --mode mh-pilot --timeout-seconds 1800 --mh-jscale 0.337313`

Configuration:
- `mh_replic`: 2000 per chain
- chains: 2
- blocks: 2
- burn-in: 50 percent
- `mh_jscale`: 0.337313
- target acceptance band: 0.20 to 0.35

Result:
- finite likelihood reported: true
- last finite log posterior/likelihood: -467.763166
- chain acceptance ratios: 0.2725, 0.2920
- average acceptance ratio: 0.28225
- R-hat status: unavailable warning

This pilot is not final convergence evidence and does not support posterior
inference claims. WBS-073 full MH, backtesting, Redux, and sovereign-extension
artifacts remain forbidden until explicitly approved.
