## 1. detect-loop skill

- [x] 1.1 Write `skills/detect-loop.md`: trigger conditions, adapter interface (manuscript path in / per-segment result file out / threshold parameters), minimal-intervention fix discipline, locking and lessons-learned flow, compliance statement (verify: check each item against the spec; wording checked against the author-communication reference table)
- [x] 1.2 Attach a result-file format example (format only, no real platform protocol) (verify: the example can be referenced directly by the flow)
- [x] 1.3 `python tools/check-agents.py` (verify: exit 0)

## 2. Dispatch wiring

- [x] 2.1 Add a detect-loop optional phase row to the `skills/novel-dispatch.md` dispatch table, plus author-trigger semantics and a breakpoint-resume note (verify: format matches existing phase rows)
- [x] 2.2 Add a detect-loop branch to the `agents/novel-agent.md` THINK tree (verify: `check-agents.py` exit 0; no conflict with the dispatch table)

## 3. Wrap-up and release

- [x] 3.1 Full checks: `check-agents.py` + `check-conflicts.py` + `py_compile` + `test_platforms.py` (verify: all green)
- [ ] 3.2 One live walkthrough: local submission tool (author-provided) through the full fix-highest-window, lock, distill flow (verify: the battle log gains one round, regression strings enter the library, check-chapter re-run exits 0)
  - Verified 2026-08-31 for trigger and degradation semantics: a headless Claude session correctly recognized the "submit it" intent, ended gracefully with a plain-language explanation to the author when no local tool existed, and wrote no files beyond its authority; the full live external test still waits for the author to provide a detection route
- [x] 3.3 Release `chore: bump version to v4.24.0`, updating `VERSION` and `docs/releasenotes/releasenote-4.24.0.md` (verify: `check-version.py` passes)
