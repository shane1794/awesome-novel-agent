# v4.19.0 Release Notes

> **Keywords:** Machine pre-screening: check-prose.py wired into the anti-AI flow, deterministic scripts in the Phase 2 pre-screen and the Phase 4 re-run

---

## In One Sentence

The main-text checking script `check-prose.py` introduced in v4.18.0 moves from "standalone tool" into the anti-AI pipeline proper (#117, tracking issue #116): **automatic deployment to six-platform projects at initialization, a scripted machine pre-screen before Phase 2 quantitative scoring, and a re-run for verification after the Phase 4 final draft**. Regex and statistics catch hard metrics the model eye misses or miscounts; the script only reports and never edits the main text, and if it cannot run, it degrades to the model eye (non-blocking).

---

## What Changed in This Release

| Change | Description |
|------|------|
| **Automatic six-platform deployment** | `init.py` adds `deploy_tools()`: initialization deploys the script to `<platform root>/tools/check-prose.py` (claude/opencode/reasonix/codex/zcode/dsh); `sync-project.py` adds `sync_tools()` to sync it, and **the script itself is included in the upgrade fingerprint**. Without that, existing projects would be short-circuited by sync because the fingerprint never changed, and would never receive the script |
| **Phase 2 machine pre-screen** (skills/anti-ai.md) | Before quantitative scoring, run the script: "needs changes" (hard failure, exit code 1: hard stop words, slang, model signposts, reversal sentences) merges into the Gate A/B hit list going into Phase 3; "needs human judgment" (warnings: semantic pivot sentence patterns, sentence-length rhythm, short-paragraph bursts, repeated openings, metaphor clustering, conjunction density) only marks candidate passages for "save the person before cleaning the sentences" and does not directly count as a violation |
| **Phase 4 machine re-run verification** | After edits, re-run the script on the `.anti-ai.md` main-text section (excluding the acceptance-report section, whose quoted counterexamples would false-positive); it passes only when "needs changes" reaches zero. False-positive protection exemptions apply the same way (hits on the exemption list are marked `[SKIP: false-positive protection]`); the edit statistics gain a "script verification" row and the acceptance checklist gains a matching row |
| **Degradation iron rule** | The script only reports and never edits the main text; thresholds follow anti-ai.md, and script warnings never escalate into a hard Gate; if the script is missing, Python is unavailable (on Windows try `python`/`py` first), or the shell cannot execute, degrade to the model eye and mark the report "script verification not run" (non-blocking) |
| **Engineering fixes** | agents/anti-ai.md Input Sources gains a script entry and its flow lines are synced; the ARCHITECTURE.md pipeline diagram adds the machine pre-screen and re-run steps; the AGENTS.md tool-list wording is updated (no longer "standalone tool, not a pipeline stage") |

---

## Compatibility

- Purely new deployment artifacts plus prompt-text changes, with no schema or workflow-structure changes; new projects ship with the script on initialization.
- **Existing projects**: running `python tools/sync-project.py <project path>` deploys the script (the script is in the fingerprint, so the upgrade is always detected); skill_version will update to 4.19.0.
- Environments without Python or with shell disabled automatically degrade to the model eye, with the report visibly marked "script verification not run", without blocking the flow.
- The anti-ai agent gains a new behavior of running shell commands (running the Python script); its `tools:` allowlist already includes Bash, so no configuration is needed.
- The script uses only the standard library; on Windows run it with `python` or `py` (noted in the skill).

---

## How It Was Verified

- Red then green: `test_platforms.py` adds 8 assertions (six-platform deployment + content identical to source + sync recovery + fingerprint awareness); 8 FAIL before implementation, **213 passed, 0 failed** after
- Static checks all green: check-agents / check-conflicts / check-version / check-yaml / check-python / py_compile
- E2E run: script references in opencode/zcode/codex products are all auto-rewritten with the platform prefix; the deployed script returns exit code 1 and outputs "needs changes" when run on "worth noting is"
- review-agent review closed: 2 P3 items (ARCHITECTURE pipeline diagram lagging, Windows python3 adaptation) fixed before merging (f177516)
- Still for the author: run one chapter on any AI terminal (focus on the degradation path: delete the script inside the project, run a chapter, and the report should say "script verification not run" rather than erroring)
