# updater Rollback Skill: Undo This Chapter's Archive Append

## Responsibilities

**Rolling back a chapter means undoing every append that chapter's archiving made to the settings**, returning to the state before that chapter was written. Only roll back this chapter; do not touch other chapters. This is the preparation step for the #81-4 "rewrite after archiving" scenario: when the author wants to rewrite a chapter, first remove the traces that chapter wrote into the settings, then walk the chapter outline / main text / archive pipeline again.

**Input:** `rollback-order.md` (containing volume N / chapter M)
**Output:** A rollback completion report (how many entries of each settings type were deleted + the list of files involved), with the order marked `status: DONE`

**How it is triggered (#81-7 /undo):** After archiving, the author only needs to say "rewrite chapter X" directly in conversation. novel-agent recognizes it and dispatches this order. No special command is needed; natural language triggers it.

## Core Principles

- **Delete by reverse inference, not by snapshot**: archiving is an "append" (a row added to the timeline, a hook added to foreshadowing, a block added to character state), so rollback is "deleting what was appended". Every target file has a chapter anchor to check against.
- **Only roll back this chapter**: all operations are anchored on `vol-{N}-ch-{M}` or `第 {N} 卷第 {M} 章`; never delete another chapter's settings by mistake.
- **Delete less rather than more**: when an anchor does not match (for example, a memory entry has no chapter field), keep it; do not force the deletion.

---

## Step 1: Read the Order, Confirm the Rollback Target

1. Read `rollback-order.md` and take volume `{N}` and chapter `{M}`
2. Confirm that `chapters/vol-{N}-ch-{M}.md` exists and its `status: archived` (only an archived chapter needs rolling back)

## Step 2: Undo the Timeline Append

**Target:** `settings/timeline.md`
**Anchor:** the table row `| vol-{N}-ch-{M} |`
**Action:** Grep for `vol-{N}-ch-{M}` to find the matching row, then use Edit to delete the whole row.

> Each chapter's archiving adds one row to the timeline; rollback deletes that row. Other chapters' rows stay untouched.

## Step 3: Undo the Foreshadowing Append (both directions)

**Target:** `settings/foreshadowing.md`
**Anchor:** the `埋设位置` (planted at) column / `收束位置` (closed at) column equals `vol-{N}-ch-{M}`

**1. Delete the hooks this chapter planted** (from the "unclosed hooks" table):
- Find every row whose `埋设位置` column contains `vol-{N}-ch-{M}` and delete the whole row
- These hooks are newly planted by this chapter; once the chapter is rewritten they are void

**2. Roll back the hooks this chapter closed** (move them from "closed hooks" back to "unclosed hooks"):
- Find every row whose `收束位置` column contains `vol-{N}-ch-{M}`, delete it from the "closed" table, and move it back to the "unclosed" table (status back to active, planned closure cleared)
- These hooks were planted in earlier chapters and closed by this chapter. After the chapter is rewritten, the closure may no longer hold, so roll them back first

## Step 4: Undo the Character State Append

**Target:** `settings/character-setting/{id}.md` (every appearing character)
**Anchor:** two formats are supported:
- v4.9.0 new format: `## vol-{N}-ch-{M} 状态变更`
- Old format: `#### 第 {N} 卷第 {M} 章`

**Action:** For each character file:
1. Grep for the block heading `## vol-{N}-ch-{M} 状态变更` or `#### 第 {N} 卷第 {M} 章`
2. Delete everything from that block heading up to the next header of the **same or higher level**
   - Both the plot history (the `#### 第 {N} 卷第 {M} 章` under `### 剧情履历`) and the emotional arc (the matching sub-block under `### 情绪弧线`) are deleted
3. If a character file has no block for this chapter (for example, a supporting character whose file was only created on first appearance), skip it and leave it untouched

> Note: a character settings file "appends state blocks"; it does not "overwrite the whole state". After deleting this chapter's block, the character returns to the state at the end of the previous chapter (built by stacking the blocks from ch1 through ch(N-1)).

## Step 5: Change the Chapter Outline Status Back

**Target:** `chapters/vol-{N}-ch-{M}.md`
**Action:** Edit `status: archived` to `status: outline`

> This triggers novel-agent to run this chapter through the chapter outline / prompt / main text / archive pipeline again.

## Step 6: Roll Back This Chapter's Memory (delete less rather than more)

**Target:** `.claude/memory/*.md` (writing-memory / chapter-memory / prompt-memory / volume-memory)
**Limitation:** memory entries have a `日期` (date) field but no `章节` (chapter) field, so they are unreliable.
**Action:** Only roll back an entry when it meets both conditions at once; otherwise keep it:
1. Its `场景` (scenario) field contains `vol-{N}-ch-{M}` or `第 {N} 卷第 {M} 章`
2. Its `日期` (date) field equals this chapter's archive date (read `archived_at` from `.agent/archiving/vol-{N}-ch-{M}.done`)

> Delete less rather than more: memory is the author's banked preferences, and deleting it by mistake costs a lot. When no anchor matches, keep it.

## Step 7: Output the Rollback Report

```
## Rollback Completion Report: vol-{N}-ch-{M}
- timeline: deleted X rows
- foreshadowing: deleted X planted hooks / rolled back X closed hooks
- Character settings: {character name} state block deleted, {character name} skipped
- Chapter outline status: archived → outline
- Memory rollback: X entries (those matching the anchor)
- Files involved: {list}
```

Mark the order `status: DONE` (do not delete it).

## Volume Completion State (left to novel-agent)

After rollback, this chapter is no longer `archived`. novel-agent must recalculate volume completion:
- Archived count < planned count → clear `last_volume_completed` (novel-agent is the only writer; updater does not write it)

## Acceptance Checklist

- [ ] The timeline row for this chapter is deleted; other chapters' rows are complete
- [ ] Foreshadowing: hooks planted by this chapter are deleted, hooks closed by this chapter are rolled back
- [ ] Character settings: this chapter's state block is deleted, restored to the state at the end of the previous chapter
- [ ] Chapter outline status is changed back to outline
- [ ] Memory: only anchor-matching entries were rolled back (delete less rather than more)
- [ ] Other chapters' settings are completely untouched
