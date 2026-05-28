# WBS-063 IRF Diagnostics

Status: blocked on approved IRF restrictions.

Runtime check:
- `python src/diagnostics/run_dynare.py --mode irfs` runs `stoch_simul(order=1, irf=20, nograph, noprint)` in a temporary working directory.
- The IRF smoke run passed locally.
- No IRF output directory, posterior output, identification output, backtesting output, priors, Redux, or sovereign files were created.

Restriction audit:
- WBS-063 requires five IRFs to pass sign, timing, magnitude, and benchmark checks.
- `docs/05_replication_targets.md` is still a template with `targets_approved: false`.
- The template explicitly says target filling starts no earlier than WBS-074 and requires Gate 3 model outputs.
- No approved WBS-063 target rows exist with `expected_sign`, `timing_window`, `magnitude_band`, and `benchmark_source`.

Conclusion:
- Dynare can run the calibrated model IRF smoke in sandbox.
- WBS-063 cannot be completed without approved IRF restrictions.
- Do not proceed to WBS-064 or Gate 3 approval until the IRF target contradiction is resolved.
