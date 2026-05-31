# WBS-073 Blockers

Status: `BLOCKED_WBS073_FULL_MH_TIMEOUT`

Approved command:
- `python src/diagnostics/run_dynare.py --mode full-mh --timeout-seconds 43200`

Observed failure:
- wrapper return code: 124
- elapsed seconds: 43200
- failure type: approved timeout reached before full-MH diagnostics completed
- stdout tail: convergence diagnostics progressed through parameter 28
- stderr tail: FLTK/GL2PS warnings only
- acceptance ratio: not available from completed wrapper summary
- R-hat: unavailable because full-MH diagnostics did not finish

WBS-073 remains blocked. Do not proceed to WBS-074, backtesting, Redux, or
sovereign-extension work until the full-MH runtime/diagnostics blocker is
resolved and a completed WBS-073 summary is reviewed.
