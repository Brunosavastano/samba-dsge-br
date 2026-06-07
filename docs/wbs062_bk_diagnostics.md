# WBS-062 BK Diagnostics

Status: WBS-062 completed after source-backed timing correction.

Initial BK failure:
- Dynare `steady; check;` reported 26 eigenvalues larger than 1 in modulus for 28 forward-looking variables.
- Order condition was not verified.
- WBS-061 residuals had already passed with max residual 0.0.

Lead-lag incidence summary:
- Forward-looking candidates included `q`, `nfa`, `c_o`, `q_k`, `i`, `k`, `wn`, price/wage Phillips variables, and Dynare auxiliary exogenous lead variables.
- The two-variable mismatch matched stock laws written at t+1 in WP239: NFA and capital.

Candidate classifications:
- `nfa`: source_backed_timing_fix. WP239 Appendix C.4 equation C.39 writes the NFA law with next-period stock notation. Dynare requires `predetermined_variables nfa` for this end-of-period stock convention.
- `k`: source_backed_timing_fix. WP239 Appendix C.1 equation C.7 writes capital accumulation with next-period capital. Dynare requires `predetermined_variables k` for this end-of-period stock convention.
- Other forward-looking variables: not_an_issue for WBS-062. Their leads come from sourced expectation terms, Phillips curves, UIP/Tobin's Q/investment blocks, or Dynare auxiliary exogenous lead handling.

Applied fix:
- Added `predetermined_variables nfa k;` to `model/samba_classic/samba_classic.mod`.
- No calibration values changed.
- No equations were deleted.
- No IRFs, outputs, estimation, Redux, or sovereign files were created.

Post-fix BK result:
- `python src/diagnostics/run_dynare.py --mode bk` passed.
- Dynare reported 26 eigenvalues larger than 1 in modulus for 26 forward-looking variables.
- Dynare reported that order and rank conditions are verified.
