## Why

Source constraints (the previous two changes) can push the number of external AI detection fix rounds to a minimum, but cannot guarantee zero: slice boundaries are decided by the whole text's distribution, detectors keep upgrading, and re-testing the same text fluctuates. An optional calibration step triggered manually by the author is needed: submit to an external detector, fix by per-segment results, lock the version when it passes, and distill each round's lessons into the project's battle log and regression library.

## What Changes

- Add `skills/detect-loop.md`: a platform-independent SOP for the external-detection calibration loop (submit to an external AI detector, read per-segment results, fix only the highest-scoring segment, keep boundaries stable with equal-length fine-tuning, lock the version when it passes, distill the battle log and regression strings).
- `skills/novel-dispatch.md` dispatch table gains an author-triggered optional phase (it only starts when the author says "submit it / run it through detection"; it does not enter the default pipeline).
- Engineering integration is described as an adapter: the repo contains no detection-platform automation scripts, reverse-engineered protocols, or keys; how a local tool connects is described inside the skill.
- State the compliance boundary explicitly: the SOP only serves the author's voluntary calibration of their own manuscript; it does not package detector evasion or bypass platform risk controls.

## Capabilities

### New Capabilities

- `detect-loop`: an author-triggered external-detection calibration loop, the flow contract for submission, per-segment fixes, locking, and lessons learned.

### Modified Capabilities

(No existing spec.)

## Impact

- Added: `skills/detect-loop.md`.
- Changed: `skills/novel-dispatch.md` (optional phase row + breakpoint-resume semantics note).
- Depends on: `wire-source-constraints-into-pipeline` merged first (reuses `sandbox/detect-battles.md` and `sandbox/prose-regressions.txt`, plus the check-chapter re-run).
- Explicitly not added: detection-platform automation scripts, interface-reversing docs, key templates, browser-fingerprint schemes.
