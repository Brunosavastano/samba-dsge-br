# WBS-073 Full MH Diagnostics

Status: failed.

Command: `C:\Users\bruno\AppData\Local\Microsoft\WinGet\Links\dynare.CMD samba_classic.mod noclearall nolog`

Configuration:
- `mh_replic`: 20000 per chain
- chains: 4
- Dynare `mh_nblocks`: 4
- approved blocks metadata: 2
- burn-in: 0.5
- `mh_jscale`: 0.337313

Diagnostics:
- finite likelihood reported: True
- acceptance values: [0.30705, 0.18170000000000003, 0.1361, 0.12315]
- average acceptance ratio: 0.187
- R-hat status: above_threshold
- max R-hat: 4.054739157907651
- raw chain artifacts committed: False

This is full-MH operational validation, not final publication-grade posterior evidence.
WBS-074, backtesting, Redux, and sovereign-extension work remain forbidden until explicitly approved.
