# WBS-073 Runtime Diagnostics

Status: `BLOCKED_WBS073_FULL_MH_TIMEOUT`

Scope: diagnosis only. No full MH rerun, WBS-074, backtesting, Redux, sovereign
extension, equation, prior, data, calibration, or `mh_jscale` change was made.

## Existing WBS-073 Artifacts

Only lightweight committed artifacts are present under `outputs/posterior/full/`:

| artifact | size_bytes | sha256 |
|---|---:|---|
| `wbs073_full_mh_summary.json` | 1148 | `C5EF7F38E841B3AD24D1049C599E1777C4513CC0AD6E3BA700F86F4599B3ADBA` |
| `wbs073_full_mh_diagnostics.md` | 761 | `39AF44D247C63A14E44D1549EC33BD18FC8AFA9030A1178378568DC34E57E41C` |
| `wbs073_full_mh_manifest.json` | 789 | `C48AA87DEF1DBE2227CDAD61A298DDF925AB5DBDD195A37F0F6904BFCE865790` |

Raw chain files present in repo: no.

R-hat/convergence files present in repo: no.

Partial diagnostics available: yes, but only as the timeout summary/diagnostic
tail. The stdout tail says convergence diagnostics progressed through parameter
28 before the approved timeout killed the process.

Acceptance lines found in committed artifacts: no. The wrapper did not reach
the post-process parser because the Dynare process timed out.

## Cause Classification

Most likely cause: timeout too short for the approved config plus convergence
diagnostics.

Evidence:
- WBS-073 approved config: 20000 draws per chain x 4 chains = 80000 draws.
- WBS-072 pilot: 2000 draws per chain x 2 chains = 4000 draws, elapsed
  1124.922 seconds, no full convergence diagnostics.
- Linear draw scaling from WBS-072 implies about 22498 seconds for sampling
  alone, before full diagnostics.
- WBS-073 timed out at 43200 seconds with stdout tail in convergence diagnostics
  through parameter 28, suggesting sampling likely reached the diagnostic phase.

Parser failure: not the primary cause. The parser only runs after Dynare
returns; the wrapper received a `TimeoutExpired` path and therefore had no
completed stdout/stderr to parse.

Raw artifacts generated but not summarized: possible during the temporary run,
but not recoverable from current artifacts. The wrapper ran in a temporary
directory and cleaned it after timeout, so no raw chain manifest is available.

Chains did not finish: not proven. The convergence-diagnostic tail implies
chains probably produced enough files for diagnostics to start, but the current
committed artifacts do not independently prove chain completion.

## Runtime Feasibility Estimate

Conservative retry timeout should cover sampling plus convergence diagnostics.
Using WBS-072 elapsed time and the observed WBS-073 timeout point, a same-config
retry should be budgeted above 43200 seconds. A practical bound is 64800 to
86400 seconds if Bruno approves a longer run.

## Recommended Next Safe Action

Preferred: increase timeout and rerun the same approved WBS-073 config, while
improving timeout handling so the wrapper preserves a manifest of raw temporary
chain files before cleanup if timeout occurs.

Alternative: split WBS-073 into resumable batches only if Dynare/current wrapper
support is documented and the chain continuation semantics are verified.

Alternative: run chains sequentially only if the wrapper can preserve the same
approved chain count and produce comparable diagnostics.

Any reduction of `mh_replic`, chain count, blocks, or `mh_jscale` is a revised
proposal requiring Bruno approval.
