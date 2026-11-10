# Tasks: 2026-09-10-add-short-scan-analyze

## 1. Deployment mechanism

- [ ] 1.1 platforms.py: `SHORT_STANDALONE_SKILLS = ("short-scan", "short-analyze")` + `deploy_standalone_skills(project, skill_home, platform, names)` (`_convert_standalone_skill` + rewrite_refs to `<skills_dir>/<name>/SKILL.md`); `deploy_inline_skills(short)` mounts the standalone tools inside. Verify: inline platforms produce 8 skill directories on short init
- [ ] 1.2 init.py: the short flow deploys the standalone tools (all platforms use the same helper). Verify: 7-platform products contain both tools
- [ ] 1.3 sync-project.py: short sync_skills re-deploys the standalone tools; find_changes short branch adds the two-file comparison. Verify: tampering is detected / sync restores

## 2. List-scan SOP (skills/short-scan.md)

- [ ] 2.1 Flow body: platform-direction confirmation in three forms (S1), three-tier data sources with degradation marking (S2), one platform failing is skipped (S2.4)
- [ ] 2.2 Seven-dimensional analysis + platform tone comparison (S3); report template with the freshness trio and trend warnings (S4)
- [ ] 2.3 Topic matching: complexity tiers + spread-risk coverage (S5)
- [ ] 2.4 Appendix: built-in market knowledge (cross-platform tone table / platform synopsis formulas / genre hit formulas, compressed and inlined from the gifted pack's real-market-data.md)

## 3. Teardown SOP (skills/short-analyze.md)

- [ ] 3.1 Input and routing: obtaining the original text / word-count three tiers (A1); genre yardstick loading short-genres (A2)
- [ ] 3.2 Resume checks and original-text backup (A2.1 / A3)
- [ ] 3.3 Five-stage pipeline with per-stage completion markers (A4); crash-safe write protocol (A5)
- [ ] 3.4 Output file tree (five items under analysis/{book title}/) and the `_meta.json` schema (A6)
- [ ] 3.5 Three acceptance gates (A7)

## 4. Wiring and tests

- [ ] 4.1 SKILL.md short-story branch adds the optional-tool note (with the not-in-the-dispatch-chain statement). Verify: grep
- [ ] 4.2 test_platforms: seven-platform standalone-tool deployment assertions; inline count 6 to 8; claude/opencode/codex/grok skills-directory assertions; long-form regression without the two tools. Verify: all green
- [ ] 4.3 Full-chain regression: py_compile / check-agents / check-conflicts / test_platforms
- [ ] 4.4 Push the PR + review-agent review; **do not merge, per the author's request** (merge timing waits for a decision after live-testing the short-story main chain)
