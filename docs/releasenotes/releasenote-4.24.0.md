# v4.24.0 Release Notes

> **Keywords:** External-detection calibration loop: an author-triggered optional submission step with minimal-intervention fixes + pass-and-lock + lessons learned

---

## In One Sentence

When the author says "submit it" or "run it through an external detector", the agent fixes with minimal intervention: only the most machine-like passage is touched, everything else is left word-for-word untouched, the draft is locked and backed up as soon as it passes, and every round is recorded in the book's detection-battle archive. Platform-independent: the repo contains no automation scripts or keys for any detection platform; the submission method is entirely the author's own (a local tool or manual web submission).

## What Changed in This Release

| Change | Description |
|------|------|
| **detect-loop skill** | `skills/detect-loop.md`: trigger conditions, submission-adapter conventions (result-file fields: per-segment start/end, scores, original text), fix discipline (each round fixes only the highest-scoring segment, first and last sentences locked, equal-length fine-tuning, stop-loss after two rounds without improvement, author settings always win), locking (SHA256), and lessons learned (battle log + confirmed failure sentences into the regression library) |
| **Dispatch wiring** | `novel-dispatch.md` dispatch table adds an optional detect phase (author-triggered; does not advance chapter status or enter the breakpoint table); `novel-agent.md` THINK tree gains a global trigger branch |
| **Offline by default** | Not part of the default pipeline; when no local submission method exists, it ends gracefully with a notice and does not block the main flow |
| **Compliance boundary** | The repo holds zero detection-platform code, protocols, or keys; the adapter only defines the format contract for the input manuscript and the output result file |

## Compatibility

- Purely incremental: the default pipeline (draft, anti-ai, review, archive) behaves unchanged; if submission is never triggered, it is completely invisible.
- It connects naturally with the v4.22.0/v4.23.0 structural-heat-source knowledge, the check-chapter tool, and the three sandbox files (fixes are judged by structure type, re-run every round, and lessons go into the library).

## Tests

- check-agents / check-conflicts / check-version / py_compile / both test scripts all green (this release has no Python tool changes).
- A live submission walkthrough waits for the author to provide a detection route (change tasks 3.2 left as a to-do).
