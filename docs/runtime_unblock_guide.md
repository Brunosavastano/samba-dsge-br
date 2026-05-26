# Runtime Unblock Guide

## Current Blocker

Status: `BLOCKED_BY_RUNTIME`

Blocked scope: `WBS-054 / PR11`.

The next planned task creates `model/samba_classic/`, but Dynare implementation must not start until a valid Dynare runtime path is available and verified.

## Required Runtime Options

Option A: Octave + Dynare.

Option B: MATLAB + Dynare.

Recommended minimum path: Option A, unless the project will standardize on MATLAB.

## What Must Be Installed Or Added To PATH

- `dynare` command must resolve from the project shell.
- Either `octave` or `matlab` must resolve from the project shell.
- If Dynare is installed but not on PATH, expose its executable path before continuing.

## Verification Commands After Installation

Run these commands from `C:\Users\bruno\Desktop\Codex\SAMBA`:

```text
python --version
dynare --version
octave --version
matlab -batch "disp(version)"
```

At least one of `octave` or `matlab` must be available, and `dynare --version` must succeed.

## What Codex Should Do After Runtime Is Available

Re-run runtime verification, update `docs/runtime_verification.md`, then continue to WBS-054 only if the runtime gate passes. Do not create `.mod`, `.m`, `.inc`, fake outputs, estimation files, Redux, or sovereign extension as part of the unblock step.

