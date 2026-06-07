# WBS-073 Blockers

Status: `BLOCKED_WBS073_STRATEGY_PROPOSED_AFTER_FULL_MH_DIAGNOSTICS`

Current blockers:

- Guarded WBS-073 full-MH rerun started from a clean archived external workdir
  and completed Metropolis chains, but the wrapper hard-aborted during
  post-processing when `D:\` free space reached 49.937 GB, below the approved
  50 GB runtime threshold.
- Finite likelihood was reported and no NaN/Inf likelihood blocker appeared.
- Acceptance values: 0.30705, 0.18170, 0.13610, 0.12315.
- Average acceptance ratio: 0.187, below the approved 0.20 to 0.35 band.
- R-hat status: above_threshold; max R-hat: 4.054739157907651.
- R-hat was computed, so the blocker is not parser unavailability.

Answers for next WBS-073 decision:

- Did all 4 chains complete? Yes. Evidence: `mh_chains_completed: true` in
  `wbs073_full_mh_summary.json`, four acceptance lines in diagnostics, and
  four raw chain block artifacts recorded in the manifest.
- Are acceptance 0.187 and max R-hat 4.0547 based on complete chains? Yes for
  the chain draw artifacts, but the run still failed during post-processing via
  the disk guard, so these are operational diagnostics, not final posterior
  evidence.
- Primary blocker: mixed runtime + diagnostics blocker.

Proposed next strategy:

- Because chains completed but acceptance is below band, the next MH change
  should be a revised `mh_jscale` proposal only. No model equation, prior, data,
  calibration, observable, shock, sample, chain count, burn-in, or `mh_replic`
  change is justified by the current artifacts.
- Because disk abort occurred during post-processing, runtime handling should
  also be improved before rerun, preferably by sequential chains or chain
  batching if the wrapper can preserve manifest/R-hat diagnostics.

Options:

- A. Rerun same config with corrected runtime/disk handling. Changes only
  runtime/post-processing storage. Does not change model, priors, data, sample,
  `mh_jscale`, `mh_replic`, chains, or burn-in. Risk: likely repeats poor
  acceptance/R-hat diagnostics. Bruno approval required: yes. Recommended: no.
- B. Revised `mh_jscale` proposal. Changes only proposal scale to target the
  approved 0.20 to 0.35 acceptance band. Does not change model economics,
  priors, data, sample, `mh_replic`, chains, or burn-in. Risk: R-hat may remain
  high and require another convergence pass. Bruno approval required: yes.
  Recommended: yes.
- C. Sequential chains / chain batching. Changes execution layout only: one
  chain or batch at a time, separate external scratch dirs, cleanup between
  batches, final combined manifest/R-hat if artifacts support it. Does not
  change model economics or MH parameters by itself. Risk: wrapper complexity
  and R-hat aggregation must be tested. Bruno approval required: yes.
  Recommended: yes as runtime support for option B, not as a standalone fix.

WBS-073 remains blocked. Do not proceed to WBS-074, backtesting, Redux, or
sovereign-extension work.
