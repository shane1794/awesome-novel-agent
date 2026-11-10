## Context

- Prerequisites: `add-zhuque-source-defense` (knowledge + tools) and `wire-source-constraints-into-pipeline` (pipeline wiring + skeleton) are merged; `sandbox/detect-battles.md`, `sandbox/prose-regressions.txt`, and `sandbox/locked-lines.txt` are already project skeleton files.
- The closed-loop lessons from the source pack (per-segment results, fix the highest window, lock, distill) are verified effective, but its engineering carriers (CDP scripts, captcha solving, fingerprint farms, interface-reversing docs) must not enter the repo.
- The dispatch contract lives in `skills/novel-dispatch.md` (order type list + breakpoint-resume semantics); agent details live in the `agents/novel-agent.md` THINK tree.

## Goals / Non-Goals

**Goals:**

- Put the loop's "flow knowledge" in the repo and keep its "engineering carriers" local: the skill teaches the method and carries no tools.
- Connect seamlessly with the existing dispatch, degradation, and locking semantics.

**Non-Goals:**

- Do not implement any detection-platform integration code.
- Do not make detect-loop a default pipeline stage.
- Do not auto-rewrite to a perfect score (rewriting still runs under anti-ai semantics; this skill only sets the fix discipline).

## Decisions

1. **Minimal order-type extension.**
   One new order type, `detect-loop-order.md`, with one "author-triggered" row added to the dispatch table; the `agents/novel-agent.md` THINK tree gains one matching branch. The alternative, "merge it into the anti-ai phase as Phase 5", was rejected: it would turn an optional stage into a default path and dilute anti-ai's exit-code and report contract.
2. **Platform-independent adapter interface.**
   The skill only specifies three things: the submission entry point (a local command or the author manually submitting on a website), the result file (per segment: start/end positions, score, text), and the decision-threshold parameters. The source pack's CDP, captcha, and quota scripts and reversing docs are tools for bypassing platform risk controls, so they are **not kept, not migrated, and never enter the repo** (local copies deleted 2026-08-31); the repo keeps only the result-file format contract, and the author provides the connection method through legitimate means (such as an official API or manual web submission).
3. **Fix discipline as its own section, reusing anti-ai's execution semantics.**
   "Fix only the highest-scoring segment / keep boundaries stable / equal-length fine-tuning / stop-loss" is rewriting discipline, written into the skill for any executor (the anti-ai agent or an agent assisting after the author's manual edits) to follow; the specific Gate fixes still follow anti-ai.md.
4. **Locking semantics reuse the archives snapshot convention.**
   Lock snapshots land in `archives/` (or a location the author specifies), with the hash recorded in the battle-log file; no new locking infrastructure is added.
5. **The compliance statement is written into the skill body.**
   Purpose limits (the author's own manuscript, voluntary calibration) and asset isolation (no automation scripts in the repo) are acceptance items, so later contributors do not accidentally commit local tools.

## Risks / Trade-offs

- Making it platform-independent leaves the skill vague about "how exactly to submit", which may feel abstract to first-time users. Mitigation: the skill includes a "minimal result-file example for a local integration tool" (a pure format example, not any real platform protocol).
- Numeric discipline such as "stop-loss after two consecutive rounds under 0.05" comes from a single measured project and may not fit other detectors. Mitigation: thresholds are parameterized, and the skill marks their source and scope.
- Author-trigger semantics depend on the dispatch layer accurately recognizing natural language. Mitigation: it uses the same mechanism as the existing "author confirmation gate", so the risk is controlled.
