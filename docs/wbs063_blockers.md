# WBS-063 Blockers

Status: BLOCKED_WBS063_IRF_TARGETS.

- approved IRF targets: 0
- required approved IRF targets: 5
- blocker: `docs/05_replication_targets.md` remains a template with `targets_approved: false`.
- reason: WBS-063 requires sign, timing, magnitude, and benchmark checks, but no approved target rows exist.
- runtime note: IRF smoke through the Dynare wrapper passes in a temporary directory.
- generated outputs: none committed.

Next action:
- Resolve the WBS-063/WBS-074 target-ordering conflict by approving or sourcing five MVP IRF restrictions, or explicitly redefining WBS-063 as an IRF smoke-only check.
