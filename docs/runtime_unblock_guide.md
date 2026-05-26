# Runtime Unblock Guide

## Current Blocker

Status: `UNBLOCKED_FOR_WBS_054`

Blocked scope: `WBS-054 / PR11`.

The next planned task creates `model/samba_classic/`. Runtime is now available through Octave 11.1.0 and Dynare 7.0.

## Required Runtime Options

Option A: Octave + Dynare.

Option B: MATLAB + Dynare.

Recommended minimum path: Option A, now installed and verified.

## What Must Be Installed Or Added To PATH

- `dynare` command resolves from the project shell through a user PATH wrapper.
- `octave` command resolves from the project shell.
- Dynare is loaded in Octave through `C:\Users\bruno\.octaverc`.

## Verification Commands After Installation

Run these commands from `C:\Users\bruno\Desktop\Codex\SAMBA`:

```text
python --version
dynare --version
octave --version
matlab -batch "disp(version)"
```

At least one of `octave` or `matlab` must be available, and `dynare --version` must succeed. This is satisfied by Octave 11.1.0 and Dynare 7.0.

## What Codex Should Do After Runtime Is Available

Continue to WBS-054 only. Do not create `.mod`, `.m`, `.inc`, fake outputs, estimation files, Redux, or sovereign extension as part of WBS-054.
