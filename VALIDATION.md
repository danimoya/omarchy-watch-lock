# Validation record

Target source baseline: installed Omarchy 4.5.0-3, Hyprland 0.56.2, Qt 6.12.0.
The current upstream lock/PAM and fingerprint implementation was copied from
the package, with the provenance retained. This fresh standalone plugin has
not replaced the maintainer's active lock provider.

Checks and their results are recorded below after execution. Native secure
standalone lock/unlock and the full release matrix remain pending; screenshots
use a non-authenticating fixture and do not establish those results.

## 2026-11-07 checks

- `python3 -m unittest discover -s tests -v`: eight CLI/coverage cases pass; the
  native service check is opt-in because PanelWindow requires a Wayland backend.
- `WATCH_LOCK_NATIVE_CHECK=1 python3 -m unittest discover -s tests -p test_native_load.py -v`:
  passes on the installed Wayland session with fake compositor/stranded-lock
  commands. The full service loaded without requesting a lock or authentication.
- `node --test tests/policy.mjs`: ten cases pass, covering mode eligibility,
  idempotence, opaque-lock disclosure prevention, sleep/system-lock handling,
  invalid runtime state, idle-background guards and absence of IPC unlock paths.
- `python3 preview/render.py`: rendered both actual QML panel states over the
  invented app fixture. Pointer hover reaches 100% opacity; pointer exit reaches
  5%. Both 1600×900 PNGs were visually inspected and contain no PNG text/EXIF chunks.
- Plugin manifest validation, Bash syntax and QML syntax formatting pass.
- Source scan found no enrollment files, credentials, private lock-product code,
  machine home paths or server addresses in the publication tree.
- The active desktop's lock provider was not replaced. Actual standalone PAM
  unlock, fingerprint hardware, recovery, suspend and the release matrix remain
  pending. This is published as a development preview, without a supported tag.
