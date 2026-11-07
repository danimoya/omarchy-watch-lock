# Before a supported release

- [ ] Independent review of authentication and transparent-background failure handling.
- [ ] Actual standalone password unlock, failure/lockout, fingerprint and fallback on a disposable user session.
- [ ] No ordinary app exposure during screensaver crash/closure, output removal/addition or shell failure.
- [ ] Suspend/resume, closed lid, AC removal and the 50% battery boundary.
- [ ] Installation, upgrade, removal and restoring the prior lock provider on a fresh account.
- [ ] Multiple outputs, scaling/rotation and compositor errors.
- [x] Publish matching optional screensaver companion source: `danimoya/omarchy-animated-screensaver@7c42b13` (development snapshot, not a supported release).
- [ ] Mark a supported version only after recording the tested commit and completed checks.

The repository and tools-site listing are development previews. Directory
submission, acceptance and a supported release are separate steps.
