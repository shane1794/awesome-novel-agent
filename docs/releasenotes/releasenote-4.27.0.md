# v4.27.0 Release Notes

> **Keywords:** Short-story list-scanning + text-teardown standalone tools: closing the "pick a topic, benchmark, write" loop

---

## In One Sentence

Short-story authors no longer pick topics by feel or imitate from impression: say "scan a list" and get a market report with freshness labels and writable directions; say "tear this story apart" and a hit story is broken down into recallable structural assets. The short-story loop closes as "pick a topic, benchmark, write".

## What Changed in This Release

| Change | Description |
|------|------|
| **short-scan (list scanning)** | Standalone tool: confirm the platform direction in three forms (deep scan / full-list overview / platform comparison), then three tiers of data sources (live collection from the runtime environment / author-provided / built-in knowledge, degrading tier by tier, with every degradation labeled "not verified live, candidate hypothesis only"), then seven dimensions of analysis (emotion distribution / genre hotspots / length / opening patterns / ending types / title patterns / character models), then a report with sample dates, confidence, next re-scan time, and a three-tier trend warning, then topic matching (complexity tiers plus a spread-risk fallback: a direction with no reversal must be backed by strong resonance, strong topicality, or strong aftertaste). Market knowledge is inlined as an appendix; platform-independent |
| **short-analyze (text teardown)** | Standalone tool: word-count routing (ask in the gray zone), then a genre yardstick (load the style pack by the short-genres registry slug for comparison), then continuation checks and original-text backup first, then a five-stage serial pipeline (structure / emotional line / reversal / characters / synthesis, with a completion marker per stage), then crash-safe writes (pre-stage markers plus non-empty checks, so half-finished work is never trusted), then five outputs under `analysis/{book title}/` (report / plot nodes / writing techniques / original-text backup / `_meta.json` structure counts), then three acceptance gates (the report's own AI-tone self-check, structure-count verification, strong-blocking scan) |
| **Deployment form** | `SHORT_STANDALONE_SKILLS` plus a shared `deploy_standalone_skills` helper across all platforms: both tools deploy as SKILL.md files under each platform's skills directory (claude/opencode create the skills directory first; codex/grok land in the standalone-tool directory; reasonix/zcode/dsh go from 6 to 8 inlined directories). They do not enter the short-agent dispatch chain and take no phase; the author triggers them directly |
| **Sync wiring** | Short-story sync idempotently re-deploys the standalone tools; `find_changes` compares expected content word by word after deployment conversion (project-side deletion or tampering is detected and sync restores it) |

## Design Points

- The teardown methodology is compressed and inlined into the SOP (about 300 lines) with no new knowledge directory; the tool is a self-contained unit
- `_meta.json.genre` aligns with the genre-registry slug (zhuiqi/shiqing/...), reserving automatic same-pack style loading for the writing stage
- Teardown performs read-only, transformative literary criticism on works the user legitimately holds; conventional fictional elements of popular genres are structured and broken down as usual

## Compatibility

- Purely incremental: zero changes to the long-form path (long-form projects do not contain the two tools, guarded by negative assertions); short-story product layout is unchanged
- Live list-scanning collection depends on runtime-environment capability; when unavailable it degrades with a label and introduces no repo dependencies

## Tests

- check-agents / check-conflicts / check-version / py_compile all green; test_platforms **535/535** (new: seven-platform standalone-tool deployment assertions, inline count 6 to 8, short-story sync E2E: sync restores a deleted tool, --check exit 0, long-form negative assertions)
- review-agent review: all 11 findings fixed (1xP0: short-story sync missing import crash; 2xP2: standalone-tool content comparison and slug routing; 8xP3); the "tamper, detect, restore" loop is verified live
- **To-do**: run one list scan and one teardown on a real machine (topic decisions and teardown quality are runtime behavior)
