# Migration Spec: Migrating from 2.x to 4.0

> The agent follows this spec to migrate settings. Each file's field mapping table defines how old-version fields map to new template locations.
> Acceptance criteria: every required field in the new template has a source in the old version, and content is complete after migration.

## Field Status Markers

| Marker | Meaning |
|------|------|
| ✅ Fill directly | The old field value can be filled into the new location as-is |
| 🔄 Summarize | The agent reads the old field content and distills it into the new sub-fields |
| ⚠️ To infer | The old version has no direct matching field; the agent infers from context |
| ❌ New | Does not exist at all in the old version; the author must supply it |

---

## §1 story.yaml → story.md

**Old path:** `story.yaml`
**New path:** `story.md`
**Template:** `templates/migration/story.md.template`

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| `# {title}` | `story.yaml → title` | ✅ Fill directly | Title matches |
| Metadata → skill_version | None | ❌ New | Write `4.13.0` |
| Metadata → Genre | `writing-style.yaml → genre_profile` | ✅ Fill directly | Fill if a value exists, otherwise mark "to confirm" |
| Metadata → Tags | No direct field | ⚠️ Infer from story.yaml content | May be empty |
| Metadata → Status | None | ❌ New | Write "Writing" |
| Reference path table → Worldbuilding summary | `story.yaml → world_setting.summary` | ✅ Fill directly | Non-empty |
| Reference path table → Genre summary | None | ❌ New | Mark "to confirm" |
| Reference path table → Character summary | `story.yaml → characters.summary` | ✅ Fill directly | Non-empty |
| Reference path table → Writing style summary | `story.yaml → writing_style.summary` | ✅ Fill directly | Non-empty |
| Main story arc → Structure type | No direct field | ⚠️ Infer from the number of volumes plus content | Fill at least one |
| Main story arc → Total volumes | Number of `volumes/*.yaml` files | ✅ Fill directly | Number is correct |
| Main story arc → Core conflict of the whole book | Each volume's `core_conflict` | 🔄 Summarize each volume's core conflict into one sentence | Non-empty |
| Volume plan → Volume N title | `volume-{N}.yaml → title` | ✅ Fill directly | Every volume has one |
| Volume plan → Volume N arc position | No direct field | ⚠️ Infer from `volume-{N}.yaml → summary` | Mark "to confirm" |
| Volume plan → Volume N core conflict | `volume-{N}.yaml → core_conflict` | ✅ Fill directly | Every volume has one |
| Volume plan → Volume N estimated chapters | Count of `volume-{N}.yaml → chapters_summary` | ✅ Fill directly | Number is correct |

### Acceptance

- `story.md` title line is correct
- Of the three metadata fields, at least Genre has a value
- All 4 rows of the reference path table are non-empty (the Genre row is marked "to confirm")
- Main story arc section: structure type, total volumes, and core conflict are all present
- Volume plan: volume count is correct, every volume has at least a title and a core conflict
- No old story.yaml remains

---

## §2 world-setting.yaml → settings/world-setting.md

**Old path:** `settings/world-setting.yaml`
**New path:** `settings/world-setting.md`
**Template:** `templates/migration/world-setting.md.template`

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| Geography → Main locations | `world-setting.yaml → details.geography` | 🔄 Extract key place names and locations from the overall description | At least 1 main location |
| Geography → Climate | `world-setting.yaml → details.geography` | 🔄 Extract climate features from the description | Non-empty |
| Geography → Geographic limits | `world-setting.yaml → details.geography` | 🔄 Extract geographic limits from the description (such as transport and terrain) | Non-empty |
| Politics → Form of rule | `world-setting.yaml → details.politics` | 🔄 Extract the ruling structure from the description | Non-empty |
| Politics → Main factions | `world-setting.yaml → details.politics` | 🔄 Extract at least 2 factions from the description | At least 2 |
| Politics → Social stratification | `world-setting.yaml → details.politics` + `sociology` | 🔄 Extract social strata from the description | Non-empty |
| Politics → Cost of disobedience | `world-setting.yaml → details.politics` + `rules` | 🔄 Extract from the description | Non-empty |
| Rules → World level | `world-setting.yaml → details.rules` + `physics` + `biology` | 🔄 Extract from the underlying physics and biology rules | Non-empty |
| Rules → Society level | `world-setting.yaml → details.rules` + `culture` + `sociology` | 🔄 Extract from the society and culture rules | Non-empty |
| Rules → Personal level | No such sub-field in the old version | ⚠️ Infer from other sections or mark "to confirm" | Mark "to add" |

**Note:** The new template is more structured than the old one (it has sub-fields). The agent reads the old version's free-text paragraphs, understands them, and fills them into the new sub-fields by category. Content from old fields such as `culture`, `history`, and `sociology` is spread across the Geography, Politics, and Rules sections.

### Acceptance

- All three Geography sub-fields have substantive content
- All four Politics sub-fields have substantive content
- Rules sub-fields: world level and society level have content; personal level may be empty but must be marked "to add"
- Compare against the old file to confirm no important setting point was lost

---

## §3 writing-style.yaml → settings/writing-style.md

**Old path:** `settings/writing-style.yaml`
**New path:** `settings/writing-style.md`
**Template:** `templates/migration/writing-style.md.template`

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| role (Narrative identity) | `writing-style.yaml → role` | ✅ Fill directly | Non-empty |
| role (Narrative identity) (merge personality) | `writing-style.yaml → personality` | 🔄 Merge into the end of the role section | Non-empty |
| core_principles (Unbreakable writing creed) | `writing-style.yaml → core_principles.*` | 🔄 Merge all sub-fields into one list | Non-empty, no duplicates |
| possible_mistakes (Mistakes AI commonly makes) | `writing-style.yaml → possible_mistakes` | ✅ Fill directly | Non-empty |
| depiction_techniques (Description levels and techniques) | `writing-style.yaml → depiction_techniques` | ✅ Fill directly | Non-empty |

**Note:** The new version uses Markdown format (not YAML). The old version's 5 `core_principles` sub-fields (global_rules / natural_expression / description_vs_depiction / character_building / pov_consistency) are merged into one list under `## Core Principles`. `personality` is merged into the end of the role section. `genre_profile` goes into §8 genre-setting.md. `workflow` / `writing_model` have no matching location in the new version; skip them during migration.

> **Titles actually read during migration** (aligned 2026-08-12 with init.py `migrate_writing_style`): the old .md card's body headings use the Chinese-suffix form, shown here literally because migration matches them exactly: `## role（叙事身份）` / `## core_principles（不可违背的写作信条）` / `## possible_mistakes（AI 易犯错误）` / `## depiction_techniques（描写层次和手法）` (see repo history f4bb229). Migration extracts by full heading; the `role` / `core_principles` names in the table above are YAML field-key shorthand, not literal headings. Bare English headings (`## role`, etc.) do not exist in the actual old cards and need no compatibility handling.

### Acceptance

- role (Narrative identity) section has personality merged in and is non-empty
- core_principles (Unbreakable writing creed) contains the content of all old sub-fields
- possible_mistakes (Mistakes AI commonly makes) fully migrated
- depiction_techniques (Description levels and techniques) fully migrated
- Compare against the old file to confirm nothing was missed

---

## §4 anti-ai.yaml → settings/anti-ai.md

**Old path:** `settings/anti-ai.yaml`
**New path:** `settings/anti-ai.md`
**Template:** `templates/migration/anti-ai.md.template`

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| Fatigue words → Adverb class | Adverb-class words in `anti-ai.yaml → fatigue_words_zh` + `fatigue_words_en` | ✅ Fill directly | At least some entries |
| Fatigue words → Verb class | Verb-class words in `anti-ai.yaml → fatigue_words_zh` | ✅ Fill directly | Non-empty |
| Fatigue words → Adjective class | Adjective-class words in `anti-ai.yaml → fatigue_words_zh` | ✅ Fill directly | Non-empty |
| Fatigue words → Conjunction class | Conjunction-class words in `anti-ai.yaml → fatigue_words_zh` | ✅ Fill directly | Non-empty |
| Fatigue words → Body-reaction templates | `cliche_action` / `cliche_environment` in `anti-ai.yaml → fatigue_words_zh` | ✅ Fill directly | Non-empty |
| Sentence-pattern rules | `anti-ai.yaml` + `tic-patterns.yaml` | ✅ Fill directly | Reference paths are correct |
| Rewrite algorithm → Perception-word removal | Perception-word rules in `anti-ai.yaml` | 🔄 Agent summarizes the old rules | Non-empty |
| Rewrite algorithm → "le" particle cleanup | "le" (了) rules in `anti-ai.yaml` | 🔄 Agent summarizes the old rules | Non-empty |

**Note:** The new version categorizes more clearly; the old version's `fatigue_words_zh` sub-categories are filled into the new categories.

### Acceptance

- Each fatigue-word category has substantive content
- Sentence-pattern rule reference paths are correct
- The rewrite algorithm has a concrete description

---

## §5 hooks.yaml → settings/foreshadowing.md

**Old path:** `settings/hooks.yaml`
**New path:** `settings/foreshadowing.md`
**Template:** `templates/migration/foreshadowing.md.template`

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| Active foreshadowing table | `hooks.yaml → hooks[]` with `status=pending/mentioned` | 🔄 Extract as table rows: description → Hook, introduced_in → Introduced in, payoff_timing → Expected payoff, last_mentioned_chapter → Last mentioned | Every unresolved hook in the old version appears |
| Resolved foreshadowing table | `hooks.yaml → hooks[]` with `status=resolved` | 🔄 Extract as table rows: description → Hook, introduced_in → Introduced in, resolution_chapter → Resolved in | Every resolved hook in the old version appears |
| Abandoned foreshadowing table | `hooks.yaml → hooks[]` with `status=abandoned` | 🔄 Extract as table rows | Every abandoned hook in the old version appears |

**Note:** The old hooks.yaml has dozens of detailed fields (hook_type, priority, hook_strength, etc.); the new version keeps only core summary information. Detailed metadata is not maintained here; it has been spread into each chapter's chapter.md memo.

### Acceptance

- The three tables cover every hook in the old hooks.yaml, with none missing
- Active / resolved / abandoned categories match the old version
- Each entry has at least a description and a chapter

---

## §6 character yaml → settings/character-setting/*.md

**Old path:** `settings/character-setting/{id}.yaml`
**New path:** `settings/character-setting/{id}.md`
**Template:** `templates/migration/character.md.template`

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| Basic info → id | File name (without extension) | ✅ Fill directly | Non-empty |
| Basic info → Name | `{character}.yaml → name` | ✅ Fill directly | Non-empty |
| Basic info → Story role | `{character}.yaml → story_role` | ✅ Fill directly | Non-empty |
| Basic info → Appearance | `{character}.yaml → appearance` | ✅ Fill directly | Non-empty |
| Basic info → Background | `{character}.yaml → background` + `summary` + `age` + `occupation` | 🔄 Merge multiple fields | Non-empty |
| Basic info → Language traits | No such field in the old version | ❌ New | Mark "to add" |
| Abstract layer → Worldview | `{character}.yaml → cognition.l1_worldview` | ✅ Fill directly | Non-empty |
| Abstract layer → Self-positioning | `{character}.yaml → cognition.l2_self_identity` | ✅ Fill directly | Non-empty |
| Abstract layer → Values | `{character}.yaml → cognition.l3_values` | ✅ Fill directly | Non-empty |
| Practical layer → Abilities | `{character}.yaml → cognition.l4_core_abilities` | ✅ Fill directly | Non-empty |
| Practical layer → Skills | `{character}.yaml → cognition.l5_skills` | ✅ Fill directly | Non-empty |
| Practical layer → Environment | `{character}.yaml → cognition.l6_environment` | ✅ Fill directly | Non-empty |
| Relationships | `{character}.yaml → relationships` | 🔄 Convert entry by entry | Original relationship count is correct |
| Status history | `{character}.yaml → state_history` | ✅ Fill directly | Non-empty (if history exists) |
| Emotional arc | No such field in the old version | ❌ New | Mark "to add" |

### Acceptance

- Every old character yaml maps to one new character md, with matching counts and none missing
- The 6-layer cognition model is fully migrated (the old version has 6 fields, the new version has 6 locations)
- Relationships are converted entry by entry
- Background has merged the old version's multiple fields
- Language traits and emotional arc are marked "to add"

---

## §7 volume yaml → volumes/volume-{N}.md

**Old path:** `volumes/volume-{N}.yaml`
**New path:** `volumes/volume-{N}.md`
**Template:** `templates/migration/volume.md.template`

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| `# Volume {N}: {Title}` | `volume-{N}.yaml → title` | ✅ Fill directly | Non-empty |
| Core conflict | `volume-{N}.yaml → core_conflict` | ✅ Fill directly | Non-empty |
| Estimated chapters | Count of `volume-{N}.yaml → chapters_summary` | ✅ Fill directly | Number is correct |
| Chapter list → Chapter titles | `volume-{N}.yaml → chapters_summary[].title` | ✅ Fill directly | Every chapter has one |
| Chapter list → Conflict events | `volume-{N}.yaml → chapters_summary[].summary` | ✅ Fill directly | Every chapter has one |

**Note:** The old version's `summary` and `main_events` fields have no direct location in the new template; the agent may fold their core content into the volume's introductory paragraph.

### Acceptance

- Volume count matches the old version
- Every volume's core conflict is fully migrated
- Chapter list length matches the old chapters_summary
- Nothing is marked "to add"

---

## §8 genre-setting.md (new)

**No such file in the old version.** The old `writing-style.yaml` field `genre_profile` records the genre ID.

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| Selected type | `writing-style.yaml → genre_profile` | ✅ Fill directly | Fill if a value exists, otherwise mark "to confirm" |
| Payoffs to deliver | No such field in the old version | ⚠️ Extract from the genre-example library | Mark "to confirm" |
| Pacing rules | No such field in the old version | ⚠️ Extract from the genre-example library | Mark "to confirm" |
| Cliches to avoid | No such field in the old version | ⚠️ Extract from the genre-example library | Mark "to confirm" |
| Genre taboos | No such field in the old version | ⚠️ Extract from the genre-example library | Mark "to confirm" |

**Note:** This file is new in 3.0. If the old version has a `genre_profile`, the agent pre-fills from the matching genre config under `knowledge/genre-example/`; if not, mark everything "to discuss".

---

## §9 chapter yaml → chapters/vol-{N}-ch-{M}.md (archived only)

**Old path:** `chapters/vol-{N}-ch-{M}.yaml` (only `status: archived`)
**New path:** `chapters/vol-{N}-ch-{M}.md`
**Template:** `templates/migration/chapter.md.template`

### Field Mapping

| New Template Location | Old Version Source | Migration Method | Acceptance |
|-----------|---------|---------|------|
| `# Volume {N} Chapter {M}: {Title}` | `volume` + `chapter` + `title` | ✅ Fill directly | Non-empty |
| Status | `status` | ✅ Fill directly | `archived` |
| Outline → Summary | `outline.summary` | ✅ Fill directly | Non-empty |
| Outline → Key points | `outline.key_points` | ✅ Fill directly | Non-empty |
| Outline → Characters appearing | `outline.characters` | ✅ Fill directly | Non-empty |
| Outline → Scene location | `outline.location` | ✅ Fill directly | Non-empty |
| Outline → Time | `outline.time` | ✅ Fill directly | Non-empty |
| Memo → Current task | `memo.current_task` | ✅ Fill directly | Non-empty |
| Memo → Reader expectation → Emotional state | `memo.reader_expectation.state` | ✅ Fill directly | Non-empty |
| Memo → Reader expectation → Strategy | `memo.reader_expectation.strategy` | ✅ Fill directly | Non-empty |
| Memo → Reader expectation → Details | `memo.reader_expectation.detail` | ✅ Fill directly | Non-empty |
| Memo → Payoff plan → Must resolve | `memo.payoff_plan.must_resolve` | ✅ Fill directly | Non-empty |
| Memo → Payoff plan → Must hold back | `memo.payoff_plan.must_hold` | ✅ Fill directly | Non-empty |
| Memo → Payoff plan → Advance without resolving | `memo.payoff_plan.partial_advance` | ✅ Fill directly | Non-empty |
| Memo → Downtime functions | `memo.downtime_functions` | ✅ Fill directly | Non-empty |
| Memo → Key choices | `memo.key_choices` | ✅ Fill directly | Non-empty |
| Memo → Character info status | No such sub-section in the old version | ❌ New | Mark "to add" |
| Memo → Changes by chapter end | `memo.required_changes` | ✅ Fill directly | Non-empty |
| Memo → Hard constraints | `memo.prohibitions` | ✅ Fill directly | Non-empty |
| Emotional design → Primary mood | `emotional_design.primary_mood` | ✅ Fill directly | Non-empty |
| Emotional design → Mood progression | `emotional_design.mood_progression` | ✅ Fill directly | Non-empty |
| Emotional design → Intensity peak | `emotional_design.intensity_peak` | ✅ Fill directly | Non-empty |
| Emotional design → Intensity level | `emotional_design.intensity_level` | ✅ Fill directly | Non-empty |
| Emotional design → Emotional hook | `emotional_design.emotional_hook` | ✅ Fill directly | Non-empty |
| Emotional design → What the reader gains | `emotional_design.satisfaction_beat` + `micro_payoffs` | 🔄 Summarize from both sources | Non-empty |

### Migration Notes

**narrative_pov / narrative_style:** The old chapter YAML root level may have these fields (for example `narrative_pov: "林默第三人称有限视角"`, literally "Lin Mo, third-person limited POV"). The new chapter.md template has no standalone location for them. The agent writes their content at the end of Memo → Current task, tagged `[POV]`.

**segments section:** Some old chapters have a `segments:` section-level split. The new version has dropped it; section-level splitting moved to the prompt layer. Skip it during migration.

**cycle_position / suppression_stack:** InkOS-specific emotional-cycle fields that do not exist in the new version. Skip them during migration.

**prompt_path / prompt_variant / archive_path:** Metadata fields of old chapter files; the new version manages file relationships through naming conventions. Skip them during migration.

### Acceptance

- All archived chapters are migrated, with none missing
- Fields marked ✅ all have content
- Fields marked ❌ are marked "to add"
- Total chapter count matches the old version
- Skipped non-archived chapters are listed in the report

---

## §10 timeline file (new)

**No such file in the old version.** The timeline is auto-appended by the updater when archiving; during migration, just create the empty file.

**Template:** `templates/migration/timeline.md.template`

### Acceptance

- `settings/timeline.md` exists and its table header is correct

---

## Overall Acceptance Checklist

After all migration steps, the agent checks each item:

### Structure Acceptance

- [ ] `story.md` exists and its metadata is filled in
- [ ] `settings/world-setting.md` exists
- [ ] `settings/writing-style.md` exists
- [ ] `settings/genre-setting.md` exists
- [ ] `settings/anti-ai.md` exists
- [ ] `settings/foreshadowing.md` exists
- [ ] `settings/timeline.md` exists
- [ ] Character files under `settings/character-setting/` match the old version
- [ ] `volumes/volume-{N}.md` volume count matches the old version
- [ ] All archived chapters under `chapters/` are migrated
- [ ] `archives/` main text fully copied
- [ ] `prompts/` prompts fully copied
- [ ] Old `.yaml` files moved into `old/`, with none left behind
- [ ] Deprecated files (author-intent.md, current-focus.md, drafts/, etc.) cleaned up

### Field Completeness Acceptance

For each migrated file, check against its section's acceptance conditions:

- [ ] Fields marked ✅: all have content
- [ ] Fields marked 🔄: the agent's summarized content is reasonable and loses no information
- [ ] Fields marked ⚠️: marked "to confirm" or "to infer"
- [ ] Fields marked ❌: marked "to add"

### Post-Upgrade Note

> After migration, the `old/` directory keeps the old files. Once confirmed correct, delete it manually with `rm -rf old/`.
> Fields marked "to discuss", "to confirm", or "to add" are refined gradually during later writing.
