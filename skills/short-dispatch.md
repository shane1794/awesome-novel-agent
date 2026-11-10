# short-agent Dispatch SOP

> **This file is the only authoritative source for the short-story dispatch contract** (the order type list + author confirmation gates + breakpoint resume semantics).
> The flow tree in `agents/short-agent.md` is the execution detail, expanded from this table.

## Responsibility Boundaries

short-agent **only does three things**:
1. Read status to detect the current phase and story state
2. Write order files to dispatch sub-agents
3. Verify sub-agent output (order DONE + output file non-empty)

**Anything else is not your job.** Do not write content files, do not run commands, do not change settings.

## Dispatch Table by Phase

| Phase | Who does it | Order file | Output |
|-------|--------|-----------|------|
| setup | short-planner | `short-setting-order.md` | `stories/{slug}/setting.md` |
| planning | short-planner | `short-outline-order.md` | `stories/{slug}/outline.md` |
| contract | short-planner | `short-contract-order.md` | `stories/{slug}/prompt.md` |
| contract | short-verifier | `short-contract-audit-order.md` | `.agent/task/audit-report-{slug}.md` |
| writing | short-writer | `short-writing-order.md` (one per batch) | `stories/{slug}/manuscript.md` (appended) |
| polishing | short-editor | `short-polish-order.md` | Polished manuscript.md |
| verifying | short-verifier | `short-verify-order.md` | `.agent/task/verify-report-{slug}.md` |
| verifying | reader (experience check) | `short-reader-order.md` | `.agent/review/short-{slug}.md` |
| delivered | short-planner | `short-revision-order.md` (revision: conception level) | Updated setting/outline/prompt |
| delivered | short-writer | `short-revision-order.md` (revision: rewrite a few sections) | Updated manuscript.md |
| delivered | short-editor | `short-revision-order.md` (revision: expression level) | Updated manuscript.md |

## Author Confirmation Gates (two)

The framework and outline are the soul of the story; AI only does the brushwork:

| Output | Confirmation action | After the author confirms |
|------|---------|-----------|
| Framework (setting-order DONE) | Show a summary: what feeling the reader is left with / what happened / where the reversal is / who is who | phase becomes planning |
| Outline (outline-order DONE, both verifications passed) | Show a summary: what each section is about / how the emotion moves / where the breakpoint lands | phase becomes contract |

Confirmation semantics (same structure as long-form):
- Explicit confirmation (okay / no problem) → advance; wants changes → re-dispatch the matching agent (with revision notes embedded in the order) → show it again after the revision
- Vague reply (more or less / you decide) → always treat as unconfirmed, and ask what exactly is uncertain
- "You write it all" fully automatic mode → after showing the summary, treat as confirmed and advance directly, **valid for one time only**
- "Continue / advance" → only advances to the next confirmation gate, then stops

**Do not stop and wait for confirmation after the contract audit passes** (the contract is part of the AI brushwork); after the outline is confirmed, the main text pipeline (contract → audit → writing → polishing → check → acceptance) may run continuously through to delivery.

## Rules for Writing Order Files

1. Path: `.agent/task/{type}-order.md`
2. Contains only: input paths + output paths + `status: pending` (a revision order also contains the scoping conclusion and change range)
3. **A writing-order must contain the re-injection block**: the full content of this batch's contract hard-rules zone (or an equivalent excerpt). At the start of each batch, the coordinator writes the contract hard-rules zone in full into the order; the writer does not trace it back on their own
4. Do not stuff multiple tasks into one order; dispatch only one sub-agent at a time

```markdown
# {type}-order
status: pending
story: {slug}
inputs:
  - Input file path
outputs:
  - Output target path
```

## Completion Check Standard

- Order exists and `status: DONE` → finished
- Order exists and pending → waiting
- Order does not exist → unexpected interruption, enter retry (at most 2 times; beyond that, ask the author)

## Breakpoint Resume Semantics

**The status record is the only breakpoint source. On restart, read the `## Current Story Progress` section of `.agent/status.md` directly; do not do a full scan.**

**Story state = the most recently completed stage** (it advances only after the order is DONE). Judge with **strictly greater than `>`**: state > a stage means it is finished and skippable; **equal means unfinished and must be re-dispatched**.

| Stage | Finished signal |
|------|-----------|
| setting | setting-order DONE and setting.md non-empty → stop, show the framework summary, and wait for confirmation |
| outline | `Story state > outline`; equal and DONE → show the outline summary again and wait for confirmation, do not re-dispatch |
| contract-audit | Audit report exists and its conclusion is a pass |
| batch-writing | Advance by batch: writing_order_id + current_batch record where the batch broke off |
| polishing | polish-order DONE |
| verification | verify report passes and the reader review has been produced → delivery summary |

**Revision rollback**: The revision scoping conclusion decides the rollback target (conception → redo setting, with outline and contract following; outline → redo outline, with contract reassembled and re-audited; writing → rewrite only the specified sections). The state machine rolls back to the matching stage, **keeping the progress of unaffected parts**.

**Revisions do not smuggle in checks**: After a revision order is DONE, the coordinator compares the difference range (which files and sections changed). Going beyond the range the author asked for (changing the direction / deleting conflict / adding characters / changing character design / changing point of view / touching sections not asked for) means this revision fails; roll back and redo it.

## After Delivery: Cross-Story Preference Memory

At each story's delivery (confirmed by the author), short-agent asks one follow-up question: "Is there any preference from this story you want fixed in place (writing style / rhythm / things to avoid)?"
Append the author's explicit feedback as one line in "original text → conclusion" form to `<platform>/memory/author-feedback.md` (deduplicate against existing entries, do not rewrite them). short-planner takes the "author preference memory" field for contract assembly from here, so the author's taste is not lost across stories.
Only append when the author explicitly stated a preference; MUST NOT summarize or invent one yourself.

## Prohibited Items

- Do not write files other than orders and status
- Do not write directly to any content under stories/
- Do not call multiple sub-agents in one loop
- Do not do what a sub-agent is supposed to do
