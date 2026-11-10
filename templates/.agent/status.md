# Project Status

- **skill_version:** 4.28.0
- **phase:** setup
- **current_step:** setting        # volume-planning / chapter-planning / prompt-crafting / writing / anti-ai / reviewing / archiving
# phase values: setup / outline / draft / anti-ai / review / archive / finished
# last_volume_completed and phase: finished are written by novel-agent (volume-completion decision); the updater does not write completion flags
- **current_volume:**
- **current_chapter:**
- **last_archived:**
- **last_quality_gap:**        # Most recent word-count downgrade record (synced by novel-agent from the writing order)
- **next_task:** Fill in the basic settings

## Current Chapter Progress

# Stage-level breakpoint signals for the new-chapter flow. Chapter status = **the most recently completed stage** (advance only after the sub-agent order is DONE).
# After an interruption and restart, novel-agent reads this section to find the breakpoint: use strict greater-than `>` for the check. A status greater than a stage means that stage is done and can be skipped;
# equal means that stage is not done and must be re-dispatched. The stage currently in progress is expressed by current_step and does not go in this section.
# Chapter status starts empty (reset to empty when a new volume or chapter begins, before volume-planning).
- **Chapter status:**                  # volume-planning / chapter-planning / prompt-crafting / writing / anti-ai / reviewing / archiving / all complete
- **writing_order_id:**           # Unique ID of the order the writer executed, for audit reference; the partial location follows the partial_path in writing-order.md
