# WBS-057 Blockers

Status: `BLOCKED_WBS057_EQUATION_SOURCES`

WBS-057 remains blocked before `model/samba_classic/samba_classic.mod`.

Missing exact formula count: 34.

Usable rows currently documented: MON Taylor rule, deterministic target treatment, UIP closure, risk AR(1), exchange-rate sign convention, and duplicate risk-shock mapping.

Main missing blocks: fiscal identities, administered-price WP239 formula, household equations, firm equations, aggregation identities, and most shock processes.

Reason: registry and literature map provide verified locators, but not exact Dynare-ready formulas for all MVP-required equations.

Do not create `samba_classic.mod`, `shocks.inc`, `observables.inc`, outputs, data, estimation, Redux, or sovereign extension while this status holds.

Exact next action: extract and record exact formulas from WP239 Appendix C into WBS-057 sourcing, then re-evaluate `.mod` readiness.
