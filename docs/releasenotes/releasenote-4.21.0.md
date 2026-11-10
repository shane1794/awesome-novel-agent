# v4.21.0 Release Notes

> **Keywords:** Author confirmation gates: after volume and chapter outlines are planned, stop and wait for author confirmation instead of automatically writing the main text

---

## In One Sentence

Carrying out "humans forge the soul, AI does the brushwork": after the three soul-layer outputs (settings, volume outline, chapter outline) are done, novel-agent must stop, show the author a summary, and wait for the author's nod before continuing (PR #121). When the author says "continue" or "proceed", it advances only to the next confirmation point and stops. The main-text pipeline (prompt, main text, de-AI pass, acceptance, archive) still runs continuously as AI brushwork, and after archiving it asks as before about rewriting or the next chapter.

---

## What Changed in This Release

| Change | Description |
|------|------|
| **Author confirmation gates (dispatch contract)** | `skills/novel-dispatch.md` adds an authoritative section: once a settings, volume-outline, or chapter-outline order is DONE, it must stop and wait for author confirmation; without confirmation it writes no further order and advances no step. "Continue/proceed" means stop at the next confirmation point; "write it all yourself / don't wait for confirmation" grants a single pass, and the next gate still stops. Vague replies ("more or less", "do as you see fit") always count as unconfirmed, and the agent asks again |
| **novel-agent dispatch tree** | The THINK tree's volume-planning and chapter-planning branches gain confirmation gates isomorphic with setup (summary-presentation wording plus four branches: confirm, fully automatic, vague, wants changes). "Proceed based on the actual files" no longer bypasses a gate: when a volume outline already exists but was never confirmed by the author, it enters the confirmation gate instead of dispatching a chapter outline directly |
| **Breakpoint resume semantics** | The volume-outline and chapter-outline stages gain "equal value and order DONE means the output is written and waiting for author confirmation, so show the summary again and wait for confirmation; do not re-dispatch". After an interrupted restart, it neither re-runs a sub-agent nor skips confirmation (no new status fields; after confirmation the step advances and the chapter status stays put) |
| **Project-level instructions** | The SKILL.md dispatch rules and the three project instruction files in templates (CLAUDE.md / AGENTS.md / AGENTS.codex.md): the writing-flow chain gains "(author confirms)" markers, with a one-line soul-and-brushwork explanation visible at first glance to the author and the entry-point main agent |

---

## Background

Real user feedback (dsh session transcript, v4.19.0): after settings were confirmed, the author said "proceed", and the agent wrote the volume outline without showing it or pausing, then dispatched the chapter outline directly. Saying "continue" again ran chapter outline, prompt, main text, de-AI pass, and archiving in one breath. The root cause was that the old dispatch contract only set a confirmation gate at the setup stage; the volume-outline and chapter-outline breakpoint semantics were "order DONE means advance", so the whole pipeline did not ask the author anything until after archiving. The AI was making soul-layer decisions for the author.

## Compatibility

- Behavior change, but the status-file format is unchanged: `status.md` gains no new fields (the waiting-for-confirmation state is expressed by "chapter status equal value + order DONE"); existing projects need no action after upgrading.
- Existing initialized projects get the new dispatch contract by running `python tools/sync-project.py <project path>` (skill_version updates to 4.21.0).
- Authors who never said "write it all yourself" get two extra confirmation points (one volume-outline confirmation per volume + one chapter-outline confirmation per chapter); saying "write it all yourself" skips the current gate once.

## How It Was Verified

- Static checks all green: check-agents / check-conflicts / check-version / py_compile.
- `test_platforms.py` 253 passed, 0 failed (seven-platform init/sync E2E).
- dsh platform init spot check: the confirmation-gate text reaches the user project with the novel-agent SKILL.md (inlined SOP deployment) and the project-level CLAUDE.md/AGENTS.md.
- review-agent review: No findings; CI lint green.
- Still for the author: run one chapter on any platform and confirm that after volume-outline and chapter-outline DONE, it really stops, shows the summary, and waits for the author's nod (pay special attention to the "continue advances only one step" semantics on low-compliance model tiers).
