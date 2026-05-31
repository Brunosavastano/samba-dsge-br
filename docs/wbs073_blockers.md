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
- chain files present in repo: no
- committed full-MH artifacts: only summary, diagnostics, and manifest
- parser failure: not primary; parser did not run because the process timed out
- likely cause: approved timeout too short for sampling plus convergence diagnostics

Runtime estimate:
- WBS-072 pilot ran 4000 total draws in 1124.922 seconds without full diagnostics
- WBS-073 approved run requests 80000 total draws
- linear sampling-only estimate is about 22498 seconds
- actual 43200-second timeout occurred during convergence diagnostics, so a
  retry likely needs a longer bound, roughly 64800 to 86400 seconds, if approved

Next safe options:
- preferred: approve a longer timeout and rerun the same config, with timeout
  handling improved to preserve raw-artifact manifest before cleanup;
- alternative: resumable batches only if Dynare/wrapper continuation semantics
  are verified;
- alternative: sequential chains only if diagnostics remain comparable;
- any reduced draw/config proposal requires Bruno approval.

WBS-073 remains blocked. Do not proceed to WBS-074, backtesting, Redux, or
sovereign-extension work until the full-MH runtime/diagnostics blocker is
resolved and a completed WBS-073 summary is reviewed.
