# Proposal: 2026-09-10-add-short-scan-analyze

## Why

The short-story pipeline (v4.25/v4.26) only covers "writing": the author does not know **which emotions are hot right now** (topics are picked by feel), and there is no **teardown pipeline for benchmarking hit stories** (imitation is by impression). The gifted short-story pack originally included two standalone tools, list scanning (story-short-scan) and text teardown (story-short-analyze), which were removed when v4.25 narrowed scope. This change adds those two pieces back: topics get market data, benchmarking gets structural assets, and the short-story loop closes as "pick a topic, benchmark, write".

## What Changes

### Main flow S: List scanning (standalone tool, outside the dispatch chain)

- Add `skills/short-scan.md`: confirm the platform and direction, then three-tier data sources (live collection from the runtime environment / author-provided screenshots, text, or links / built-in knowledge, degrading tier by tier, with every degradation labeled "not live-verified"), then seven-dimensional analysis (emotion-type distribution / genre hotspots / length distribution / opening patterns / ending types / title patterns / character models), then a report (sample date / trend confidence / next re-scan time / three-tier trend warnings), then topic matching (complexity tiers + spread-risk coverage: a direction with no reversal must be backed by strong resonance, strong topicality, or strong aftertaste)
- Built-in market knowledge (cross-platform tone comparison, per-platform synopsis formulas, genre hit formulas) is inlined into the SOP appendix and does not depend on a Node collection script

### Main flow A: Text teardown (standalone tool, outside the dispatch chain)

- Add `skills/short-analyze.md`: a five-stage serial pipeline: (1) structure + plot nodes (at least 4 segments including beginning, development, climax, and ending); (2) emotional curve (at least 5 nodes) + the six high-point dimensions; (3) reversal mechanism (at least 2 setups) + writing techniques (at least 5 items); (4) character functions + opening and ending; (5) overall assessment + structure counts. Each stage has a completion marker
- **Crash-safe writes**: a pre-stage marker, then non-empty plus minimum-length checks after completion, and only then is the marker cleared and the stage recorded as complete; on resume, an incomplete stage is re-run in full
- **Three acceptance gates**: the report's own AI-tone self-check (per `.claude/knowledge/short-anti-ai.md`, scanning only the analyst's wording and skipping quoted source text) / structure-count numeric checks / strong-blocking item scan
- Output lands in `analysis/{book title}/`: original-text backup + teardown report + plot nodes + writing techniques + `_meta.json` (genre identification + structure counts, for the writing stage to auto-load the matching genre style pack)
- Genre yardstick: after identifying the genre, compare against the reference section of `.claude/knowledge/short-genres/{genre}.md` to check "whether this story meets the standard"

### Deployment and wiring

- Both tools deploy as **standalone skills** to all 7 platforms (the `.platform/skills/` directories for claude/opencode, the standalone-tool skills directories for codex/grok, the inlined skills directories for reasonix/zcode/dsh), and MUST NOT enter the short-agent dispatch chain or take a phase
- The SKILL.md short-story branch adds a note about the optional tools

## Capabilities

### New Capabilities

- `short-story-scan`: short-story list scanning: platform-direction confirmation, three-tier data sources with degradation marking, one platform failing without stopping the scan, seven-dimensional analysis, reports with freshness and trend warnings, topic complexity tiers with spread-risk coverage
- `short-story-analyze`: short-story text teardown: word-count routing, genre yardstick and resume checks, original-text backup first, a five-stage serial pipeline with per-stage completion markers, crash-safe writes, a fixed file-tree output, three acceptance gates

### Modified Capabilities

(None. Both tools are new standalone tools and do not change any existing spec requirement.)

## Impact

- **Added**: `skills/short-scan.md`, `skills/short-analyze.md`; `tools/platforms.py` (short-story standalone-tool deployment manifest + an all-platform standalone-skill deployment helper); `tools/init.py` (short-story standalone-tool deployment step); `tools/sync-project.py` (short-story standalone-tool sync); `SKILL.md` (optional-tool note); `tools/test_platforms.py` (standalone-tool E2E assertions)
- **openspec**: two new mainline specs are added after the change is archived
- **No** new dependencies (still Python standard library + pyyaml; live list-scanning collection depends on runtime-environment capability, and degrades when unavailable)
- **PR status**: per the author's request, **reviewed but not merged**. The implementation is usable; the merge timing waits for a unified decision after live-testing the short-story main chain
