# {type}-order

status: pending

inputs:
  - {input file path}

outputs:
  - {output target path}

resume_from: {fill in the partial file path when resuming after a writer interruption; leave blank in other cases}

---

> This file is the order template. novel-agent writes orders using this structure; after a sub-agent finishes, **overwrite `status: pending` with `status: DONE` using Write**, do not delete this file.
> Completion signal = the order exists AND `status: DONE` AND all outputs exist and are non-empty.
> `resume_from` is optional: the writer is the only long-output stage. When re-dispatching after an interruption, fill in the `archives/*.draft.partial.md` path and the writer resumes from that partial instead of starting over; leave it blank for other stages.
