# Writing memory format specification

> Writing memory system: Dynamic memory under `memory/` (divided into 4 files by
> stage), permanent memory under `knowledge/` (high-frequency entries after
> promotion). Each entry records the positive and negative feedback provided by the
> author during the writing process for reference in subsequent processes.

---

## 1. File structure

```
<Platform Directory>/
├── memory/ # Dynamic memory (real-time recording of each link)
│ ├── volume-memory.md # Volume link memory
│ ├── chapter-memory.md # Chapter link memory
│ ├── prompt-memory.md # Prompt word link memory
│ └── writing-memory.md # Text writing session memory
│
└── knowledge/
    └── permanent-memory.md # Permanent memory (high-frequency entries promoted from memory/)
```

> The platform directory is determined by init.py by `--platform`: Claude Code →
> `.claude/`, OpenCode → `.opencode/`, Reasonix → `.reasonix/`, Codex → `.codex/`,
> ZCode → `.zcode/`, dsh → `.dsh/`, Grok Build → `.grok/`.

## 2. File header

Each file begins with a meta-information header:

```markdown
# {stage}writing Memory

> {Description of use}

**Related Agent:** {agent list}
**Related Skills:** {skill list}

---

## Entry list
```

## 3. Entry format

Each memory contains the following fields:

| Field | Required | Description |
|------|------|------|
| **Stage** | Yes | Source stage: Volume outline/Chapter outline/Prompt words/Text |
| **Type** | Yes | Positive Case / Negative Case / Rule |
| **Field** | Yes | Subdivided areas under this stage (see §4 of each document below) |
| **Original text** | Yes | The author provides feedback on the original summary and retains key sentences |
| **Conclusion** | Yes | Distilled into reusable rules or operational guidelines |
| **Scenario** | Yes | When does this rule apply |
| **Source** | Yes | The Agent that triggered this recording |
| **Date** | Yes | YYYY-MM-DD |

Complete writing:

```markdown
### {Serial number}. {Type}: {One sentence summary}

- **Phase:** {Phase name}
- **Type:** {positive case|negative case|rule}
- **Field:** {Field}
- **Original text:** {Author’s feedback summary}
- **Conclusion:** {refined rules}
- **Scenario:** {Applicable conditions}
- **Source:** {agent name}
- **Date:** {YYYY-MM-DD}
- **use_count:** {number of citations, used for promotion}
- **last_used:** {YYYY-MM-DD, last cited date}
```

> `use_count` and `last_used` are used to track the frequency of entry usage. They are
> incremented by the agent when referencing, and the updater performs
> promotion/demotion based on this when referencing.

## 4. Item life cycle

```
memory/ entry ──use_count >= 4──→.claude/knowledge/permanent-memory.md
permanent-memory.md entry──3 consecutive sweeps Unused──→ Mark for removal → Delete after confirmation by the author
```

### 4.1 Promotion conditions (memory → permanent)

| Conditions | Description |
|------|------|
| use_count >= 4 | This memory has been referenced more than 4 times by different agents/links |
| The conclusion is clear and reusable | Confirming the conclusion before promotion is a general rule rather than a one-time scenario |
| No conflict | No conflict with existing permanent memory |

Promotion operation: Remove the entry from `memory/*.md`, append to
`.claude/knowledge/permanent-memory.md`, retaining all original fields + `[promoted
YYYY-MM-DD]` tags.

### 4.2 Downgrade conditions (permanent → remove)

| Conditions | Description |
|------|------|
| `last_used` has not been updated in 3 consecutive sweeps | No agent has cited this entry within 3 writing cycles |
| Author confirmation | Ask author for confirmation before removal |

Downgrade operation: Show the author for confirmation and then delete the entry.
Resetting `skip_count = 0` is reserved if the author thinks there is still value.

### 4.3 Use tracking rules

- After the agent references a certain memory and applies it to the output, it
  increments the entry's `use_count` and updates `last_used`
- Multiple references to the same item in the same writing session will only be counted
  once (to prevent the count from being reset in the same session)
- Check `last_used` during updater sweep. If cross-link is not updated, `skip_count`
  will be accumulated.
