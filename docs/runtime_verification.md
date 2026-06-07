# Runtime Verification

Date: 2026-05-26
Last re-run: 2026-05-26 for WBS-054 unblock

Commands attempted:

```text
python --version
dynare --version
octave --version
matlab -batch "disp(version)"
```

Results:

| Runtime | Status | Exact result |
|---|---|---|
| Python | available | `Python 3.12.6` |
| Dynare | available | `7.0` |
| Octave | available | `GNU Octave (x86_64-w64-mingw32) version 11.1.0` |
| MATLAB | unavailable | `matlab : O termo 'matlab' nao e reconhecido como nome de cmdlet, funcao, arquivo de script ou programa operavel.` |

Installed runtime:

- Octave 11.1.0 is installed at `C:\Program Files\GNU Octave\Octave-11.1.0`.
- Dynare 7.0 is installed at `C:\dynare\7.0`.
- User Octave startup file `C:\Users\bruno\.octaverc` adds `C:\dynare\7.0\matlab` to the Octave path.
- User PATH wrappers were added under `C:\Users\bruno\AppData\Local\Microsoft\WinGet\Links` for `octave`, `octave-cli`, and `dynare`.

Runtime gate status: Octave + Dynare available; MATLAB unavailable but not required for the Octave runtime path.
