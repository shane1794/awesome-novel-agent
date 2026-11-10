# Project Status (Short Stories)

- **skill_version:** 4.24.1
- **length:** short
- **phase:** setup        # setup / planning / contract / writing / polishing / verifying / delivered
# phase values: setup (set emotion and direction) / planning (concept and outline) / contract (contract assembly and audit) / writing (write the main text in batches) / polishing (de-AI pass and polish) / verifying (payoff check and acceptance) / delivered (delivered; may revise or start the next story)
- **current_story:**         # Current story slug (directory name under stories/)
- **story_status:**          # Story status: empty / setting / outlined / contracted / drafted / polished / verified / delivered
- **last_quality_gap:**      # Most recent word-count downgrade record (synced by short-agent from the writing order)
- **next_task:** Set the emotion and direction

## Current Story Progress

# Story status = the most recently completed stage (advance only after the sub-agent order completes).
# After an interruption and restart, short-agent reads this section to find the breakpoint: use strict greater-than `>` for the check. A status greater than a stage means that stage is done and can be skipped;
# equal means that stage is not done and must be re-dispatched. The stage currently in progress is expressed by phase and does not go in this section.
# Story status starts empty (reset to empty when a new story begins).
- **Story status:**                  # setting / outline / contract-audit / batch-writing / polishing / verification / all complete
- **writing_order_id:**         # Unique ID of the order the writer executed, for audit reference
- **current_batch:**            # Current batch (e.g. sections 2-3); the contract hard-rules zone is re-injected between batches
