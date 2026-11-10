# Chapter Outline Acceptance Skill

After a chapter outline is produced, check its quality and completeness item by item. Only when everything passes does it move on to the prompt generation stage. Acceptance criteria follow `.claude/knowledge/chapter-setting-style.md`.

## Process

Structured feedback (for the author) → checklist self-check → quick sniff test → AI flavor self-check

## 1. Structured Feedback for the Author

After finishing the work in `chapter-setting-style.md`, present it to the author in the format of Step 1 of the acceptance process in that file. It only counts as passed when the author explicitly says "yes". "More or less" or "you decide" does not count.

If it fails, go back to STEP 3 and revise.

## 2. Checklist Self-Check

After finishing the work in `chapter-setting-style.md`, verify each item of the 24-item checklist in Step 2 of the acceptance process in that file. Any single failing item sends it back for revision.

## 3. Quick Sniff Test

After finishing the work in `chapter-setting-style.md`, run Step 3 of the acceptance process in that file.

## 4. AI Flavor Self-Check and Removal

Scan the full text against the "6 fatal patterns" and the "hollow adjective quick reference" in the style layer of `chapter-setting-style.md`. If any pattern matches, revise and re-check, and only confirm it as passed once everything is cleared.

## 5. Confirmation

Once all checks pass, write it to `chapters/vol-{N}-ch-{M}.md` with status set to `outline`
