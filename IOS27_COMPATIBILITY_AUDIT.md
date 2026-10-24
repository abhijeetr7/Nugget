# Nugget iOS 27 compatibility audit (offline source review)

Audited repository revision: `26e0c50ec114ca3a4ff6ab2fb4ae309abfd39fa1` (2026-09-24).

## Findings

1. `README.md` explicitly warns not to use Nugget on iOS 27 because Apple patched the partial-restore method and use may result in data loss.
2. `src/devicemanagement/constants.py`: `MAX_VERSION = "26.9"`; `Device.supported()` is the version gate and therefore rejects iOS 27.
3. The same file's `Device.has_bookrestore()` returns true only through iOS 26.1 (with one explicit build exception). iOS 27 does not match a known BookRestore support case.
4. `src/devicemanagement/device_manager.py`: `start_restore()` checks `get_current_device_supports_restore()` before starting restore work. This is the important top-level safety guard.
5. `src/restore/restore.py`: `has_sparserestore_capability()` only enables SparseRestore for versions below iOS 18.1 / selected iOS 18.0 builds. It is not an iOS 27 method. `restore_files()` constructs restore records and calls `perform_restore()`; this is a sensitive destructive path and must not be run against iOS 27 while unsupported.
6. `src/restore/bookrestore.py`: BookRestore performs device-side work through lockdown/AFC and process control. Merely extending the version range would not establish that Apple's patched restore behavior can be safely bypassed.
7. iOS 26.2+ MobileGestalt/AI-enabler tweaks are separately documented as unsupported in `README.md`; adding general iOS 27 restore support would not automatically make those features work.

## Code changes in this audit branch

- Added `Device.restore_support_reason()` to make unsupported versions report a specific reason.
- Kept the maximum verified version at 26.9; iOS 27+ remains blocked.
- Changed the restore guard to surface that reason before restore begins.
- Added offline unit tests for the version gate. They do not connect to or modify a device.

## What is not yet solved

This change is **not iOS 27 restore support**. The repository does not contain a verified replacement for the partial-restore mechanism Apple patched. To implement genuine support, the new mechanism must first be identified and validated independently, then exercised with non-destructive tests and a disposable test device before the supported version range can be expanded. Do not remove the guard or raise `MAX_VERSION` as a workaround.
