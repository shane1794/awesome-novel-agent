## 1. Structural-heat knowledge file

- [x] 1.1 Write `knowledge/anti-ai/structural-heat.md`: seven laws + at least 13 high-risk structures, book names removed, each item carrying measured scores, reference paths using the post-deployment base (verify: manually check the content list)
- [x] 1.2 Compare the pack's module 4 against `knowledge/anti-ai/common-rules.md` / `anti-ai-writing.md`, list the incremental entries, and merge them (additions only) (verify: git diff shows only added lines, each traceable to its source)
- [x] 1.3 Run `python tools/check-agents.py` and `python tools/check-conflicts.py` (verify: both exit 0)

## 2. Chapter check tool (red first, then green)

- [x] 2.1 Write the `tools/test_check_chapter.py` failing cases: positive/negative cases per check, exit codes 0/1/2, regression library and whitelist missing/hit, CRLF input (verify: no implementation exists yet, so the tests are red)
- [x] 2.2 Implement `tools/check-chapter.py`: hard items (label-style sandwiches / nested double quotes / half-width quotes / dash-ellipsis / word-for-word word-count reconciliation / regression strings) + warning items (broad sandwiches / question-answer in one paragraph / weak adverbs / word counts awaiting manual check / narrow trailing-label set) + platform-convention word counting + external-file reading (verify: 2.1 all green)
- [x] 2.3 `python -m py_compile tools/*.py` and `python tools/test_check_chapter.py` (verify: zero compile errors, test exit code 0)

## 3. Deployment wiring

- [x] 3.1 Add `check-chapter.py` to the deployment manifests in `tools/init.py` and `tools/sync-project.py` (deployed to `<platform root>/tools/`, same mechanism as check-prose.py) (verify: the file exists after init in a temp directory)
- [x] 3.2 `tools/test_platforms.py` E2E assertions that the new tool exists in seven-platform output (verify: `python tools/test_platforms.py` exit code 0)

## 4. Wrap-up and release

- [x] 4.1 Full checks: `check-agents.py` + `check-conflicts.py` + `py_compile` + both test scripts (verify: all green)
- [x] 4.2 Run check-chapter once on an initialized project on at least one AI terminal (verify: per the repo contribution guide)
  - Live test in a headless Claude session on 2026-08-31: init a temp project, and the deployed product runs; an anti-ai session actually ran both scripts, with check-chapter exiting 1 and correctly hitting a sandwich defect, and 5 warnings listed one by one (see PR test/ai-terminal-verification)
- [x] 4.3 Release `chore: bump version to v4.22.0`, updating `VERSION` and `docs/releasenotes/releasenote-4.22.0.md` (verify: `check-version.py` passes)
