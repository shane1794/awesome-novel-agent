# v4.17.0 Release Notes

> **Keywords:** Full rollout of the architecture review + main-text quality governance

---

## In One Sentence

Based on the architecture review (P1/P2/P3) and a review of the main-text prompt chain, this release completes a round of systematic governance: "fixing broken references and the packaging manifest, single-sourcing the version number, deduplicating platform adapters, single-sourcing the dispatch contract, layered adjudication of rule tiers, strict matching of distilled style, single-source point of view, and aligning dialogue-density acceptance", eliminating the drift of multiple copies so that each convention is maintained in exactly one place, and making "strictly match the style once it has been learned, and keep the point of view consistent across the whole book once it has been set" a hard guarantee of main-text consistency.

---

## What Changed in This Release

| Change | Description |
|------|------|
| **Fixed broken deployment references** | 14 bare `knowledge/...` references (roleplay-sandbox, 7 format-spec files, 2 agent main texts) changed to the `.claude/knowledge/` deployment base; check-agents adds post-deployment layout reference checks, orphaned-knowledge detection, and skill.json completeness assertions (the product manifest is produced by actually running init.deploy_knowledge, guarding against model drift) |
| **Single-sourced the version number** | VERSION is the single authority; ARCHITECTURE, status templates, init seeds, and skill.json are aligned in four places; added `check-version.py` to CI; skill.json gains the knowledge/ packaging manifest, and the platform list is completed to 6 |
| **Deduplicated platform adapters** | The three reasonix/zcode/dsh converters are merged with deploy (single-sourced as `convert_agent_to_platform`); the exec_agents and sub-agent rosters converge on module-level constants; init/sync/find_changes share them in three places, with byte-for-byte verification against the HEAD baseline showing zero behavior change |
| **Made empty genre shells explicit** | The genre selection list marks "archive/anti-AI rules to be added" plus a deployment warning; urban-cultivation/high-martial genuinely merge their anti-AI rules per their reuse declarations; orphaned knowledge is wired in (3 setting guides into the updater) |
| **Single-sourced the dispatch contract** | novel-dispatch.md stands as the single authority (order type list, volume-completion decision, breakpoint semantics); the novel-agent THINK tree holds the execution details; ARCHITECTURE/SKILL/README summaries mark the authority source; AGENTS.md path conventions switch to post-deployment paths |
| **Layered adjudication of rule tiers (B7)** | The compliance tier (red lines, word counts, T1, cognition, senses, prompt layers 1-5) never yields; the quality tier (within writing-spec level) is traded off as "style > author memory preferences > base iron rules > genre baseline"; compression order is decided by the quality tier (cut environment, passersby, and transitions first; keep emotional passages) |
| **Governed drifting main text** | In the distilled state (a style card has been learned), the "style suggestions (may deviate)" wording is removed and strict matching keeps deviation at 20% or less; the duplicated "webnovel style baseline" name is split apart; cognitive verbs, causality, and temperature are no longer double-injected; the point-of-view type is defined at the setting stage and passed through the whole chain (chapter outlines only set the POV character); anti-ai acceptance adds a 12-sentence dialogue-density exception and evaluates distilled text by its share of prompt rendering |
| **Prevented terminology regression (C5)** | check-conflicts adds must-not-appear assertions: 7 legacy terms (4-layer/9-layer/Goals/hooks.md/genre_profile and others) plus anti-pattern sentences banned at the injection side; the emotion-externalization quick reference is merged (D4) |
| **Self-tested the check scripts** | check-version gains 11 assertions (mini-repo injection); install.ps1 gets a pwsh smoke test (actually run by CI on Ubuntu, exposing and fixing a Linux pwsh path-joining problem) |
| **Plain language for the author** | The author-communication spec: all author-visible content uses plain language, plugging three leaks of internal terms (parallel contributions) |
| **Converged and cleaned up docs** | Eight P3 doc-drift items (README bilingual, CONTRIBUTING, install.ps1 platform alignment, etc.); the audit recheck table marks 15/18 fixed; deleted the implemented landing-page design draft and the superpowers plan doc (11 files) |

---

## Compatibility

- Pure prompt-text and tool-script changes. init/sync behavior is unchanged (six-platform E2E byte-for-byte verification); new projects take effect directly.
- Existing initialized projects take effect after running `python tools/sync-project.py <project path>` to sync agents, knowledge, and scaffolding (skill_version will update to 4.17.0).
- `check-version.py` / `check-agents.py` are new or extended checks that must run in CI; they can also be run manually locally.
- New knowledge file `author-communication.md` enters project knowledge with deployment.

---

## How It Was Verified

- `check-agents.py` / `check-conflicts.py` (including C5 must-not-appear) / `check-version.py` / `py_compile` all green
- `test_platforms.py` 198 passed, 0 failed (six-platform init/sync E2E + install.ps1 pwsh smoke test + check-version 11 assertions)
- `test_style_rules.py` 125 / `test_style_distill.py` 84 all green
- Three-platform (reasonix/zcode/dsh) skills products differ from baseline by byte-for-byte diff only in expected differences
- Mimosa deep security scan: 0 findings (seal generated); all findings from two rounds of review-agent review fixed
