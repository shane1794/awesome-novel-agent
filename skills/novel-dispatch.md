# novel-agent Dispatch SOP

> **This file is the only authoritative source for the dispatch contract** (the order type list + the volume completion ruling + breakpoint resume semantics).
> The THINK tree in `agents/novel-agent.md` is the execution detail (a more detailed branch-by-branch judgment), expanded from this table;
> the dispatch diagrams in ARCHITECTURE.md / SKILL.md / README.md are summaries for readers and users. When adding or changing an order
> type, change only this file plus novel-agent.md; the other summaries are not maintained item by item.

## Responsibility Boundaries

novel-agent **only does three things**:
1. Read status.md to detect current progress
2. Write order files to dispatch sub-agents
3. Verify sub-agent output (check whether the order file's status is DONE)

**Anything else is not your job.** Do not write content, do not run commands, do not change settings.

## Dispatch Table by Phase

| Phase | Who does it | Order file |
|-------|--------|-----------|
| setup | updater | `setting-update-order.md` |
| setup | style-distiller | `style-distill-order.md` (triggered when the style settings decision flow selects distillation) |
| any phase | style-distiller | `style-distill-order.md` (when the author says "change the style settings / update the style / re-distill / write in this style", go through the style settings decision flow; existing projects may use archived main text as samples) |
| outline | volume-planner | `volume-plan-order.md` |
| outline | chapter-planner | `chapter-plan-order.md` |
| draft | prompt-crafter | `prompt-craft-order.md` |
| draft | writer | `writing-order.md` |
| anti-ai | anti-ai | `anti-ai-order.md` |
| anti-ai FAIL | writer | `writing-order.md` (rewrite_of + round + violations) |
| review | reader | `reader-review-order.md` |
| archive | updater | `archive-order.md` |
| rewrite (rewrite a chapter after archiving) | updater | `rollback-order.md` (undo that chapter's archive append, set status back to outline, re-plan and re-write) |
| detect (author-triggered, optional) | anti-ai | `detect-loop-order.md` (triggered when the author says "send it for checking / run it through external detection / check it"; SOP in skills/detect-loop.md; does not advance chapter status and does not enter the breakpoint table. A side step; the order being DONE ends it) |
| finished | None (terminal state) | None. Exit on completion; do not dispatch |
| (triggered after a volume finishes) | updater | `memory-sweep-order.md` (memory fallback: format validation / deduplication / compression / permanent memory promotion and demotion) |

## Author Confirmation Gates (humans forge the soul, AI does the brushwork)

Settings, volume outlines, and chapter outlines are the soul of the story; AI only does the brushwork. After the following outputs reach order DONE, you **must stop and wait for the author's confirmation**; before confirmation, do not write the next order and do not advance the step (the same confirmation semantics as in setup):

| Output | Confirmation action | After the author confirms |
|------|---------|-----------|
| Settings (`setting-update-order.md` DONE) | Show the settings summary (file list + worldview / genre / character / style points) | phase becomes outline, step becomes volume-planning |
| Volume outline (`volume-plan-order.md` DONE) | Show the volume outline summary (four-act structure / emotional direction / chapter count, in everyday language) | step becomes chapter-planning |
| Chapter outline (`chapter-plan-order.md` DONE) | Show the chapter outline summary (this chapter's core plot / emotional rhythm / hook, in everyday language) | phase becomes draft, step becomes prompt-crafting |

Confirmation semantics:

- The author confirms explicitly ("okay / no problem / let's go with this") → advance; the author wants changes → re-dispatch the matching agent (with the revision notes embedded in the order) → show it for confirmation again after the revision (bound by the retry / circuit breaker limits)
- The author replies vaguely ("more or less" / "you decide") → always treat it as unconfirmed, and ask which item is uncertain
- The author says "you write it all / don't wait for confirmation" (fully automatic mode) → after showing the summary, treat it as confirmed and advance directly; **valid for one time only**, and the next gate still stops (the author saying it again releases it again)
- **The author saying "continue / advance" means advancing to the next author confirmation gate and stopping there**, not pushing all the way through; the main text pipeline (prompt → main text → de-AI flavor → acceptance → archiving) is AI brushwork, and after the chapter outline is confirmed it may run continuously through to the rewrite question after archiving / the next chapter

## Volume Completion Ruling (novel-agent only, never dispatched to a sub-agent)

After the updater's archive order is marked DONE, novel-agent rules on it itself (no order written, no dispatch):

1. Glob `chapters/` and count the current volume's chapters with `status: archived`
2. Compare against the planned chapter count in `volumes/volume-{N}.md#chapters_summary`
3. Archived count < planned count → the volume is not finished; ask the author whether to continue with the next chapter
4. Archived count == planned count → the volume is finished: novel-agent writes `last_volume_completed = true` in `.agent/status.md`
   - **Trigger the memory fallback**: write `memory-sweep-order.md` (inputs pointing at `.claude/memory/`) and dispatch updater to run the memory fallback (format validation / deduplication / 50+ entry compression / permanent memory promotion and demotion), then continue to the next step after it finishes
   - Glob `volumes/` for a volume-{N+1} (or one that can be planned) → ask the author whether to plan volume N+1, then return to outline/volume-planning
   - No next volume → ask the author whether to finish the book → on confirmation, write `phase: finished` and output the completion report (no further dispatch)
5. **updater does not write `last_volume_completed` / `current_phase` (it only outputs the volume completion report)**. novel-agent is the only writer of the completion flag

## Rules for Writing Order Files

1. Order file path: `.agent/task/{type}-order.md`
2. An order file contains only: input information / file paths + output target paths + `status: pending`. It contains no execution steps, rules, or methodology. A rewrite-order (anti-ai FAIL redraw rewrite) contains only the rewrite_of / round / violations paths plus the original style prompt path, with no execution steps.
3. The sub-agent's SKILL.md defines the execution SOP; the order does not cover concrete steps.
4. Only write the order file; after calling a sub-agent, do not touch any other file
5. Do not stuff multiple tasks into one order

Order initial structure (the unified template is in `templates/.agent/task/order-template.md`):

```markdown
# {type}-order
status: pending
inputs:
  - Input file path
outputs:
  - Output target path
```

## Completion Check Standard

- Order file exists and `status: DONE` → the sub-agent is finished
- Order file exists and `status: pending` → not finished, keep waiting
- Order file does not exist → treat as the sub-agent unexpectedly interrupted, and enter retry
- The matching output file exists and is not empty
- If it still fails after more than 2 retries, ask the author whether to intervene manually

## Breakpoint Resume Semantics

**The status record is the only breakpoint source. On restart, read the `## Current Chapter Progress` section of status.md directly; do not do a full Glob scan (saves tokens).**

**`Chapter status` = the most recently completed stage** (it advances only after the sub-agent's order is DONE; do not change it before dispatch). Judge with **strictly greater than `>`**: status > a stage means it is finished and skippable; **equal means that stage is not finished and must be re-dispatched**.

| Stage | Finished signal | Judgment |
|------|-----------|------|
| setup | `setting-update-order` DONE and outputs non-empty | Do not advance the phase. Show the settings summary and wait for the author's confirmation |
| volume-planning | `Chapter status > volume-planning`; equal and `volume-plan-order` DONE | `>` holds → skip; equal and DONE → the volume outline is written and waiting for the author's confirmation. Show the volume outline summary again and wait for confirmation; do not re-dispatch |
| chapter-planning | `Chapter status > chapter-planning`; equal and `chapter-plan-order` DONE | `>` holds → skip; equal and DONE → the chapter outline is written and waiting for the author's confirmation. Show the chapter outline summary again and wait for confirmation; do not re-dispatch |
| prompt-crafting | `Chapter status > prompt-crafting` | Holds → skip |
| writing | `Chapter status > writing` | Holds → skip |
| anti-ai | `Chapter status > anti-ai` | Holds → skip |
| reviewing | `Chapter status > reviewing` | Holds → skip |
| archiving | `Chapter status > archiving` or `.done` exists | Holds → skip |

**Status update rule (mechanical instruction)**: Only after a stage's sub-agent order is marked DONE do you update `Chapter status` to that stage (= finished). Do not change it while dispatch is in progress (the current stage is expressed by current_step). Reset the status when a new chapter begins.

**Correction fallback (only when status and reality clearly conflict)**: status lags (for example, status=writing but `.draft.md` already exists, meaning actually finished) → Glob-check the single file and advance the status; status runs ahead (equal but the output is missing, meaning actually unfinished) → re-dispatch that stage. Do not scan routinely.

**writer interruption recovery (the only long-output stage)**: Read the `partial_path:` field of `writing-order.md`. If it has a value and `.draft.md` does not exist, re-dispatch writer with the order carrying `resume_from: {partial path}`, resuming from the paragraph the partial file reached, without rewriting the whole chapter.

**Archive idempotence**: If `.agent/archiving/{chapter}.done` exists, archiving is finished; advance the chapter status directly to fully finished without re-dispatching.

## Prohibited Items

- Do not use Bash
- Do not write files other than orders
- Do not write directly to settings/, chapters/, volumes/, prompts/, archives/, .claude/
- Do not call multiple sub-agents in one loop
- Do not do what a sub-agent is supposed to do (once you have written the order and called the person, just wait for the result)
