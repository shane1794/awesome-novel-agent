# Design: 2026-09-10-add-short-story-pipeline

## Context

Current state (motivation in proposal.md): the repo has only the long-form pipeline, held together by four coupled places: `tools/init.py` (skeleton generation + genre selection + knowledge merging), `tools/platforms.py` (7-platform product conversion), `skills/novel-dispatch.md` (dispatch contract + order protocol + breakpoint semantics), and `agents/*.md` (9 agents). Short stories must plug in without breaking these four.

Key existing constraints (must not be broken during implementation):

- Every `.md` under `agents/` is deployed in full by `deploy_agents`, with **no filtering mechanism**; `platforms.py`'s `SUBAGENT_NAMES` / `EXEC_AGENT_SOPS` are hard-coded single sources, and the inlined skill count is hard-asserted as 11 by `test_platforms.py`.
- `deploy_knowledge` merges the 5 general files under `knowledge/anti-ai/` plus genre files into a **single `anti-ai.md`**; `knowledge/format-specs/*.md` deploy flattened.
- `check-agents.py`'s `DEPLOYED_PATTERNS` is the post-deployment path allowlist; `_deployed_knowledge_files` obtains the product manifest by **actually calling `init.deploy_knowledge`** into a temp directory, then runs orphan detection from it.
- Agent and skill body text references to knowledge always use the `.claude/knowledge/...` base path, rewritten per platform by `rewrite_refs`; writing a repo-relative path makes `check-agents.py` error directly.
- `check-conflicts.py` scans all `.md` under `knowledge/` + `skills/` and judges cross-file threshold conflicts by "same object, different number", with `knowledge/anti-ai/common-rules.md` as the authoritative source.
- Repo tools use only the Python standard library (pyyaml is the exception), and CI runs syntax checks + agent checks + rule-conflict checks + platform tests in `.github/workflows/static.yml`.
- Deployment references and author-facing wording are constrained by `knowledge/format-specs/author-communication.md`.

## Goals / Non-Goals

**Goals:**

- Short stories are **physically isolated** from long-form at four levels (skeleton, genre numbering, agent roster, knowledge products), with long-form project products byte-for-byte unchanged.
- Short-story anti-AI has an independent knowledge source, an independent deployed product, and independent criteria, and does **not reuse** long-form-calibrated check tools.
- Short stories have both a straight-through path for experts and a guided path for newcomers, with both paths producing the same finished structure.
- Short stories keep a checkable writing contract, so "is the main text right" can be judged: the final draft can be checked item by item against the contract instead of relying only on subjective reading feel.
- All three main flows (initialization / writing pipeline / cross-story reuse and extension) land as testable requirements.

**Non-Goals:**

- Do not introduce any Node dependency. The pack's 4 Node check scripts are handled in D8.
- Do not change any existing spec's requirements; short stories and the existing pipeline do not affect each other behaviorally (see the D13 compatibility statement).
- Do not wire short-story style distillation: 8,000 to 20,000 words cannot support three-stage distillation, and it would significantly increase agent count and deployment surface.
- Do not do list scanning or text teardown: both are optional front-ends for writing, do not serve "write the finished draft first", and get separate proposals (see D13 and the proposal's "Later Changes").

## Decisions

### D1: Use `--length` as the project-type switch, not a "length mode"

The short-story skeleton (`stories/` vs `volumes/`+`chapters/`+`prompts/`) and agent roster (4+1 vs 9) are **mutually exclusive sets**, not parameterizations of the same set. As a switch, `init.py` only needs branches in four places (`create_skeleton` / `deploy_agents` / `deploy_knowledge` / `write_status`), with the long-form branches kept as-is.

- Alternative A (write both in one project, switching agent behavior by length mode) was rejected: the `anti-ai` agent would have to carry two **opposite** criteria at once (long-form bans emotion words, short-form keeps them), and `chapter-planner` would have to double as an outline for short stories that have no "chapters", so stretched semantics would inevitably leak across.
- Alternative B (no project type, just a skill group) was rejected: without a commander there are no author confirmation gates or breakpoint resume, which contradicts the repo's experience narrative of "9 collaborating agents, humans forge the soul, AI does the brushwork", and authors would have to know which skill to call themselves.
- The default `long` guarantees backward compatibility: without `--length`, products match the pre-change state.

### D2: Grade anti-AI per check item: separate knowledge criteria tracks, reuse tools item by item

The first draft handled this as whole-track separation ("short stories do not reuse `check-prose.py`"); review corrected it: that was a **per-tool blanket cut** that threw away many genre-independent check items along with it. The correct approach is to **decide reuse or independence per check item**.

**Parts that must be independent (knowledge criteria)**: the short story's de-AI criteria, banned words, and keep-or-cut criteria go in a short-story-specific directory and deploy as a standalone product file. The reason is that the keep-or-cut criteria are **directly opposite** to long-form's, so sharing them would make `check-conflicts.py`'s "same object, different number" judgment produce an unresolvable conflict (`common-rules.md` describes itself as the single authoritative source for existing rules).

**Parts that must be reused (genre-independent check items)**:

| Source | Check items | Verdict | Reason |
|---|---|---|---|
| `check-chapter.py` | Label-style sandwiches / nested double quotes / half- vs full-width quotes / word-count expression reconciliation / dash and ellipsis density / weak-adverb per-thousand-word cap / multi-round question-answer in one paragraph / trailing labels | **Reuse** | Format and layout constraints, which short stories share; the project-level asset mechanisms (regression pattern library / locked-lines whitelist) are also general |
| `check-prose.py` | Cliché stop words (说白了 / 说穿了 / 先说结论, "to put it bluntly / to put it plainly / first, the conclusion") | **Reuse** | General AI tone |
| `check-prose.py` | Business jargon (赋能 / 抓手 / 闭环…, "empower / lever / closed loop" and similar) | **Reuse** | General AI tone |
| `check-prose.py` | Signpost language (更微妙的是 / 还有一层…, "more subtly / there is another layer" and similar) | **Reuse** | General AI tone |
| `check-prose.py` | Repeated paragraph openings / sentence-length coefficient of variation | **Reuse** | Guards against monotony, independent of genre |

> Model-degradation items (repetition / truncation / engineering-word leaks) are also genre-independent and should have a machine backstop, but this repo currently **has no** such capability. It is a cross-genre gap, not a short-story-specific need, so it is moved out of this change's scope; see D8 and the proposal's "Later Changes".

**Parts that must be independent (check items bound to genre wording)**:

| Check item | Short-story criteria |
|---|---|
| Lyrical words (`LYRIC_WORDS`: 安放 / 抵达 / 微光 / 褶皱 / 丰盈 / 滚烫…, "settle / arrive / faint light / folds / fullness / scorching" and similar) | Short stories keep them; judging them a violation is a false positive |
| Reversal sentence patterns (`PIVOT_PATTERNS` including 以为…才发现 / 才明白 / 后来才, "thought... only to discover / only then understood / only later") | A core short-story sentence pattern |
| Paragraph shape and single-sentence paragraph share | Short stories require it as a platform shape (see D12) |
| Universal-metaphor threshold | The numeric wording differs |

- Alternative A (drop `check-prose.py` entirely) was rejected: it would also drop the business-jargon, signpost, repeated-paragraph-opening, and sentence-length-variation items that short stories should also check, equal to building a duplicate implementation. That was the first draft's approach.
- Alternative B (apply it wholesale, adding a `--mode short` switch to `check-prose.py`) was rejected: stuffing two opposite word lists into one tool means any word-list adjustment affects both products at once, and the switch turns "which calibration is current" into implicit state.
- Adopted approach: **itemize the check list**. Short-story projects execute against an explicit check-item list, with each item marked as handled by a tool or by the short story's own calibration (see spec `AR1`). The list is the single grading basis and can be checked by tests.

### D3: Split the agent group into 5 new + 1 reused, with acceptance as an independent post

| Short-story agent | Duty | Why not reuse the long-form one |
|---|---|---|
| `short-agent` commander | phase routing, orders, confirmation gates | `novel-agent`'s dispatch table is bound to volumes and chapters |
| `short-planner` concept | Framework + six design items + outline + two validations **+ assembling the writing contract** | `chapter-planner` depends on volume outlines and reference material |
| `short-writer` writer | Batched main-text writing + word-count hard validation | `writer` depends on the 6-element structure of `prompts/*.md` (the short-story contract structure differs) |
| `short-editor` editor | Short-story de-AI pass + polish | `anti-ai`'s criteria are opposite to the short story's |
| `short-verifier` verifier | **Contract audit** + **final-draft payoff check** | Long-form has no matching post; `reader` is an experience post, not a structure post |
| `reader` experience acceptance | Harsh reader experience acceptance | **Reuse**: the experience perspective is independent of length |

Not created, with reasons: **no `updater`**, since short stories have no cross-chapter lore-keeping and the concept agent writes the setting files directly; **no `style-distiller`**, since 8,000 to 20,000 words cannot support three-stage distillation and it would significantly increase agent count and deployment surface.

**Why acceptance must be an independent post** (the alternative analysis for this item): the contract needs two gates, "audit" and "check", and neither gate may be executed by the object being checked. That is the repo's existing doctrine; `skills/prompt-audit.md` states at its start, "you are not prompt-crafter, you carry no baggage for maintaining your own work; your only duty is to find problems". Three alternatives were rejected one by one:

- Alternative A (the concept agent audits its own contract) was rejected: exactly the self-audit that prompt-audit explicitly excludes.
- Alternative B (the editor agent doubles as the payoff checker) was rejected: the editor just finished cleanup, so checking "did cleanup break the original" is self-certification; and cleanup and checking in the same context accommodate each other.
- Alternative C (`reader` doubles as the payoff checker) was rejected: `reader`'s whole value is immersive reading feel with "real reading experience as the only standard"; stuffing a structure checklist into it pollutes its first immersive read, and polluted immersion cannot be repaired (once you read the list first and the text second, the reading feel never comes back).
- Alternative D (the commander writes the whole thing itself) was rejected: long output and piled-up rules pollute the commander's context, and a dispatcher who is also a producer loops on itself at breakpoint resume.

The cost is a short-story agent count rising from 4 to 5. The judgment basis: the short story's finished draft is **one-shot** (unlike long-form, where later chapters can correct course), so one delivery decides everything, and the independence of structure checking outranks saving one agent.

### D4: Directory and file naming follow the repo's English convention; do not carry over the pack's Chinese paths

The pack uses `拆文库/` ("teardown library") and `{title}/正文.md` ("main text"). This repo's existing convention is English directories + English file names (`volumes/`, `chapters/`, `archives/`, `settings/world-setting.md`). Short stories use `stories/{slug}/{setting.md, outline.md, manuscript.md}`, `analysis/`, `market/`.

- Reason one: the toolchain is already built on this assumption. `check-agents.py`'s reference regex is `.claude/knowledge/([A-Za-z0-9_./{}-]+)`, which contains no Chinese; `DEPLOYED_PATTERNS`'s frontmatter allowlist is `[a-z-]+\.md`.
- Reason two: authors face AI conversation, not the file tree, so Chinese paths' readability benefit does not outweigh the toolchain cost.
- Alternative (keep Chinese paths) was rejected: it would require loosening several regexes and verifying cross-platform path behavior one place at a time, with benefits that do not match the cost.

### D5: Genre style packs use pinyin slugs

The 10 short-story genre slugs: `zhuiqi` (wife-chasing crematorium), `shiqing` (worldly face-slapping), `fuchou` (revenge face-slapping), `zongcai` (CEO and wealthy families), `zhaidou` (household and palace intrigue), `minsu` (folk horror), `xuanyi` (suspense), `tianchong` (sweet pampering), `shuangnan` (dual male leads), `shadiao` (absurdist comedy).

- Reason: same style as the existing `xianxia` / `xuanhuan` / `guba` (the existing 24 genres also heavily use pinyin ids), and it satisfies the `[a-z-]+` file-name constraint.
- Alternative A (English translations such as `chase-wife-crematorium`) was rejected: the translated names are long, ambiguous, and hard for authors and agents to match.
- Alternative B (keep Chinese file names) was rejected: same as D4.

### D6: The `length` marker lands in `story.md` as the single basis for sync and routing

`init.py` writes the length marker when writing `story.md`; `sync-project.py` and the entry-point skill both read it to decide sync targets and which commander to load. No standalone config file is added (to avoid duplicating the `story.md` metadata section).

- Alternative (carry it in `.agent/status.md`) was rejected: the status file is a runtime breakpoint carrier that is rewritten repeatedly, while the project type is static metadata that belongs with `story.md`.

### D7: `check-agents.py`'s deployed-product simulation must cover both lengths

`_deployed_knowledge_files` obtains the product manifest by actually calling `deploy_knowledge`, then judges orphans from it. If it only simulated long-form, short-story knowledge files would all be misjudged as orphaned (and CI would go red). So the simulation MUST run both long and short lengths and take the union.

- Alternative (add short-story knowledge to the `_KNOWLEDGE_AUTHOR_REFS` exemption) was rejected: that exemption means "for the author, not consumed by any agent", while short-story knowledge is consumed by agents, so the semantics do not fit.

### D8: None of the pack's 4 Node scripts are wired in this change

Following D2's criterion, decide by **each check item's value and genre relevance**, not by "which pack it came from" as a whole:

| Script | Disposition | Reason |
|---|---|---|
| `check-ai-patterns.js` | Do not port | Its capability surface heavily overlaps `check-prose.py`; what short stories really need differently is in the **word lists** (lyrical words, reversal sentence patterns, paragraph shape), which belong to the short story's own calibration (D2); porting the tool does not solve that |
| `normalize-punctuation.js` | Do not port | It is **mechanical replacement** of punctuation, which hides semantic problems; short stories require semantic-level rewrites at pauses (change to short sentences / action beats / line breaks, see spec `AR6.2`), and mechanical normalization would paper over places that should be changed |
| `check-degeneration.js` | Not wired in this change; separate proposal | Repetition / truncation / engineering-word leaks are **genre-independent**, a real gap in this repo, and degeneration is a failure mode the model cannot report on itself. But it is a **cross-genre capability addition**, not a precondition for "let the author write a novel first", and tying it to short stories would only slow the main chain |
| `check-outline-copy.js` | Not wired in this change; separate proposal | Same as above; short-story outlines give one line per section with very detailed sub-events, so copy risk is indeed higher, but the check is equally genre-independent and fits an independent change landing first |

- Alternative (keep Node and wire it into deployment) was rejected: it breaks the repo's "tools use only the Python standard library" convention and would require changing CI and install scripts.
- Alternative (port both in this change) was rejected: they are cross-genre capabilities with no dependency on the short-story main chain; putting them in this change lengthens the delivery path, while this change's goal is to let the author write a finished draft as soon as possible (D13).

This change's machine-side guarantees for short stories are: word counts measured in Python (spec `D5.3`/`D5.4` hard-require it) + reusing existing tools for genre-independent format and general AI-tone checks + the short story's own calibration for genre-bound items + manual items on the self-check list.

### D9: Move the pack's content with "three rewrites", without rewriting the methodology

When moving the roughly 26 files under `knowledge/short/`, make only three rewrites: (1) change reference paths to post-deployment base paths (`.claude/knowledge/short-*`); (2) delete oh-story external-system references (`story-architect`, `narrative-writer`, `character-designer`, `consistency-checker`, `/story-setup`, `.story-deployed`, `/story-long-*`); (3) pass the wording through `author-communication.md` (remove internal field names and workflow words). The methodology itself does not change.

- Reason: the content is a gifted asset that the other side has field-tested; rewriting it would introduce unverified changes, while mechanical rewrites can be re-checked and done in batches.
- Copyright: file headers MUST mark the source, and the original author must confirm before public or commercial use (aligned with how existing changes handled similar assets).

### D10: `templates/short/` stands alone as a set, rather than adding condition branches to `templates/`

The existing `create_skeleton` copies everything from `templates/` with a full `rglob` and applies codex special-casing and path rewriting to `CLAUDE.md` / `AGENTS.md` / `AGENTS.codex.md`. If short stories were stuffed into the same directory tree, every file would need a length condition and the logic would spread out. Instead, the whole `templates/short/` tree stands alone, `create_skeleton` picks the **tree root** by length, and `_GENERATED_SCAFFOLD` and the codex special-case logic reuse the same code path for both trees.

- Alternative (one tree + file-name suffix convention) was rejected: condition branches would seep into the copy loop, path rewriting, and the scaffold allowlist in three places.

### D11: Keep the writing-contract layer in short stories, and promote the contract to the acceptance baseline

The first draft cut the contract layer (reason: a short story's "prompt" is just settings + outline + genre pack). Prompt-engineering review overturned that. The review conclusion: cutting the contract does not just remove one file; it **simultaneously drops four verified quality mechanisms**:

| Mechanism | Existing carrier | Consequence of cutting it |
|---|---|---|
| Rule deduplication (the same meaning appears only once) | Post-assembly deduplication check + the audit's deduplication dimension (hard gate) | With 20+ short-story reference files and about 40 hard rules handed straight to the writer, duplicate rules fight each other |
| Rule reordering (descending priority + position effects) | The audit's reordering dimension (hard gate) | Hard rules and suggestive techniques are mixed together, and the writer judges priorities itself |
| Four-step transformation of general techniques | The audit's transformation-completeness dimension (hard gate) | The writer gets the genre pack's general techniques instead of this story's writing |
| Inlined conflict adjudication | The pre-assembly priority hierarchy | The writer concedes on its own between five mutually conflicting hard numbers |

So short stories MUST keep the per-story contract `stories/{slug}/prompt.md`, following the six-element structure and flat output, but with two contractions for short-story size: **one per story** (because the emotion goal, core reversal, and throughline prop are story-level attributes, not one per section), and **audit dimensions redefined for short stories** (keeping the five items: transformation quality, priority order, rule deduplication, consistency between constraints, entry checkability).

**The contract's second identity is the acceptance baseline.** This is the review's most valuable conclusion: once the contract is set, "is the main text right" changes from subjective reading feel to item-by-item checking: whether hard rules were followed, whether outline sub-events landed, whether the emotion goal was met, whether the reversal position matches, whether the throughline prop's three appearances are complete, whether word and section counts meet the standard, whether the punctuation ban is at zero. Without a contract, these can only be felt as "something is off" by a reader; with a contract, undelivered items can roll back directly with quoted source evidence.

- Alternative (contract only, no payoff check) was rejected: using the contract only for generation leaves the "was it written well enough" judgment to subjective reading feel, wasting the contract's checkability.
- Alternative (merge the payoff check and experience acceptance into one) was rejected: reading the checklist first destroys immersive reading; the two must be separate, with experience second.

### D12: Short-story paragraph shape must set both a floor and a ceiling

The short-story pack's hard constraint is "each section at least 800 words / 50-65 lines", which converts at 12-16 words per line to effectively one sentence per line; the pack's Heiyan template examples are also one sentence per paragraph. But this repo's existing "warmth balance" judgment treats "requiring single-sentence paragraphs at a hard share" as high AI suspicion, and the `2026-09-04-enhance-generation-prompt-antiai` design D2 even lists "telegram-style risk" as a reason for rejection.

The two wordings directly conflict, so an adjudication was needed. The adjudication: **the platform shape takes priority, but a ceiling must be added**.

- Why the floor stands: Heiyan / Yanxuan are phone streaming reads; one sentence per paragraph is a platform shape, not a style choice, and changing it makes short stories untenable.
- Why the ceiling must be added: the pack itself writes "do not hard-split speech into three-word fragments arranged in sheets" (`submission-craft.md`, "adjust the tone without loosening the de-AI floor"), showing the other side also knows over-deletion is a risk; copying only the floor copies only half of it.
- Wording ownership: this conflict is **design-layer reasoning**; per the D13 wording decision, the spec does not write "different from another genre" and only positively states the short story's own floor, ceiling, and short-sentence positioning (see spec `AR7`).

- Alternative (follow the existing warmth-balance criterion) was rejected: it would put the short-story format spec in direct contradiction with the platform shape, leaving the writer with nowhere to stand.
- Alternative (write only the floor, no ceiling) was rejected: that was the first draft spec's state, and it is self-contradictory, requiring near-total single-sentence paragraphs on one side while inheriting an anti-fragment audit system on the other.

### D13: Scope is bounded by "the author can write a novel first"

**Scope decision**: this change has only one scope criterion: **when the author says "write a short story", can they get a finished draft**. Three blocks are sorted by it:

| Main flow | Positioning | In this change's scope |
|---|---|---|
| A Initialization and deployment | Build the short story's own runtime environment | **In** (a precondition for the finished draft) |
| B Writing pipeline | Emotion to finished draft | **In** (the main body of this change) |
| C Anti-AI track | The judgment criteria running through B | **In** (part of finished-draft quality) |

The three out-of-scope items each get separate proposals: **list scanning** (topic assistance), **text teardown** (benchmarking assistance), **cross-genre check-tool porting** (model-degradation detection, fine-outline copy detection). Reasons are in the proposal's "Later Changes": the first two are optional entry points (authors with an idea can write directly), and the third has no dependency on the short-story main chain.

This criterion also corrects D8 in hindsight: even if those two tools "should be done", they are not preconditions for "let the author write a novel first", and tying them to short stories only lengthens the delivery path.

**Wording decision**: the spec MUST state requirements in the short story's own language and must not use "different from another genre" as a requirement's skeleton. Differences and comparisons are **design-layer reasoning material** (D2, D11, D12 use them to argue why the cut is made this way), not spec body text. The spec only describes what short stories themselves should do, so any single requirement stands and can be tested on its own.

**Compatibility statement**: short stories and the existing pipeline do not affect each other behaviorally. In implementation, only the tool layer is shared (initialization scripts, platform conversion, check scripts), and those tools route by length; branches outside the routing MUST NOT change behavior because of this change.

### D14: The emotion chain is one more structural layer, not one more rule

In the first draft, **the emotion layer was broken**:

- The five-part structure (opening / setup / escalation / reversal / ending) is a **container**: it only gives share numbers, and is generic and hollow
- The genre pack's technique library is **points**: conflict-level and discrete

In between, a **named emotional arc that strings the whole story together** was missing. The fix is to pick one emotion chain at the outline stage as the whole story's skeleton: 4-6 stages, each with a name, for example "Prey Enters the Cage, Lured Into the Trap, Logic Closes In, Public Execution, Treated as Nothing". Once picked, its stages MUST cover every section of the whole story.

Three benefits, the first of which is a **direct improvement**:

1. **Section counts are derived from the chain, not padded out**. D2.7 originally solved "techniques cannot fill the section count" with "five function types as filler", which was a patch. With the chain, section counts are the natural unfolding of each stage of the chain. Both are kept and complement each other: the chain gives the skeleton, and the five function types guarantee no section is empty.
2. "How does this story's emotion move" changes from a set of share numbers into an object that is **nameable, reusable, and checkable**. Shares can only check totals; a chain can check the order of progression.
3. Genre packs upgrade from "technique collections" to "techniques + skeleton", and the author's choice changes from "which technique to use" to "which emotional line to take". The latter is the short story's real decision.

**The chain's stages and the five parts MUST NOT be forced into a one-to-one match**, following the paragraph/section orthogonality already set in D5: the chain is the emotional skeleton (4-6 parts), the five parts are functional segments (a fixed 5 parts), and the two are described independently. A four-stage chain may have two stages landing in the same one of the five parts.

- Alternative A (just add more techniques to the technique library) was rejected: techniques are points, and no quantity of them answers "how does the whole story's emotion move".
- Alternative B (write the emotion chain as a new share allocation) was rejected: that repeats the five parts at the same layer and adds no information.
- Alternative C (require the chain to match the five parts one-to-one) was rejected: a four-stage chain would fight the fixed five parts, equal to manufacturing a new set of contradictions to adjudicate at runtime, exactly the kind of problem D5.8/D5.9 just removed.

### D15: Principles and list for adopting or rejecting external prompts

Two external short-story prompts were reviewed (a standalone hit-story prompt V3.1 and a narrative-engineering meta-system), and several rules were absorbed from them. To avoid "copy it because it looks authoritative" and "reject it because it came from elsewhere", adoption follows four principles:

1. **Decidable beats attitude**: entries that give hard numbers, lists, or positive/negative comparisons are absorbed first; entries that only say "write it well" are not absorbed (they cannot be checked).
2. **Mechanism beats intent**: when the intent is right but the mechanism is wrong, fix the mechanism first and then take it. The classic case is naming: "generate randomly to avoid hackneyed names" has the right intent, but randomness is not reproducible in a language model and would break D8's minimal-revision rollback, so it becomes a decidable banned list + naming saved to disk (AR8).
3. **Short-story criteria take priority**: the two prompts' theoretical bases are long-form novels and film/TV narrative craft (the iceberg principle, zero-degree writing, beat sheets). When they conflict with short-story criteria, short stories win: short stories keep direct emotion words (AR3) and do not take the "delete all emotion words" route.
4. **No quotas**: using quotas such as "at least N kinds of senses per paragraph" or "at least N close-ups per chapter" to pad word counts pushes short stories into a single mold, contrary to AR7's anti-telegram-style goal and D12's paragraph-shape ceiling. Give methods, not quotas (following the existing D5.3 wording).

**Adopted list:**

| Source entry | Landing point | Reason for adopting |
|---|---|---|
| Revision fatal red lines (do not change the direction / delete conflicts / add characters / change characterization / change point of view) | `D8.6` | Decidable; fills the missing smuggling guardrail on the revision path |
| First-person possessive deletion (my heart becomes heart) | `AR3.4` | Checkable by regex; this repo had zero coverage before |
| Reasoning-layer modern concepts must not bare into ancient settings | `AR9` | Decidable; long-form has only a qualitative rule covering only the spoken layer, while short-story historical romance needs it |
| Throughline prop's three semantic progressions (harmless, draws attention, reveals the truth) | `D2.12` | Decidable; the original rule only defined positions, with no semantic definition |
| Catalytic breakdown (place an unexplainable contradiction at 60-75%) | `D2.13` | Decidable; adds the reversal's booster device |
| Instant gestalt reconstruction (reconnect all foreshadowing at the reveal) | `D5.13` | Decidable; before, there was only the "strongest impact" goal, with no means to achieve it |
| Scenes enter late and leave early | `D5.12` | Decidable; the original rule only reached paragraph level and lacked a scene-level entry point |
| Dialogue four-function navigation | `D7.7` | Decidable; the original function check only reached section level |
| Emotion manipulation chain (named emotional arcs) | `D2.9` / `D14` | See D14; adds a structural layer |
| Degree-adverb strong-and-weak word lists | `AR4.5` | Decidable; fills the gaps in the existing word list (seemingly / very / increasingly / indeed) |
| Banned-name list | `AR8` | Decidable; changed the mechanism (see principle 2) |

**Not adopted list:**

| Entry | Reason for not adopting |
|---|---|
| Generate the whole text in one pass (15 chapters, 25,000 words in one go) | An extreme form of context decay; this change's `D5.10` exists precisely to guard against it |
| Role-play stacking (editor-in-chief / outline writer / writer / editor in one) | Titles do not change output quality; and self-review cancels the independence that `D4` and `D7.1` require |
| At least 2 kinds of senses per paragraph, at least 3 close-ups per chapter | Quotas (principle 4) |
| A hard cap of at most 1 metaphor per thousand words | Creates wrongful deletions: functional metaphors (such as a throughline prop's imagery) may be selling points; the existing wording is "handle it only when they appear in sheets", and a hard cap conflicts with it |
| Copying the physiological-reaction word list verbatim (heart skipping a beat / eyes reddening / legs going weak) | The word list is usable, but copying it verbatim moves AI tone from the abstract layer to the word-list layer; it can only be used with a "do not reuse the same batch across stories" constraint, which this change does not introduce |
| Single sentences of at most 15 words / paragraphs of at most 3 lines | Conflicts with the short-story paragraph-shape wording: historical romance and worldly-life genres allow multi-sentence retrospective passages (see the short-story format spec) |
| Colloquializing chapter titles | Short-story sections carry no titles (pure numbers), so it does not apply; story titles are already covered by the existing title methodology |
| Numerology frameworks (wuji, taiji, liangyi, sanqing, sixiang, wuxing, liuren...) | Decorative packaging, with no generative relationship between levels and no information carried |
| "Closing remarks" and "creation info: total words / creation time" in delivery templates | Process products pollute the main-text file, conflicting with `D6.5` clean delivery |
| Censorship-avoiding wording in tension writing | Replacing direct description with metaphor is itself a legitimate romance technique, but that wording's framework is about evading platform review, which is a self-buried risk for platforms with explicit content rules such as Yanxuan |

**What this list is for**: not a review record, but a maintenance constraint. When introducing external material later, apply the same four principles; if someone wants to add back an item from the right column above, they must first overturn the matching principle or give it a decidable form.

## Risks / Trade-offs

- [Short-story thresholds are judged as conflicting with the long-form authoritative source, turning CI red] → `check-conflicts.py` judges by "same object, different number"; run it once during implementation, and add a real conflict to an explicit exemption with its reason recorded (spec `A7.3` already requires no silent passing). Most short-story objects are qualitative criteria, and the quantitative items are mainly the weak-adverb cap, so the expected conflict surface is small.
- [Large content-moving volume (about 26 files), easy to miss a path or leave an external reference] → After the move, run `check-agents.py` (reference validity + orphan detection); sweep external references once with keyword `grep` (`story-architect` / `narrative-writer` / `.story-deployed` / `/story-`).
- [Inlined skill-count assertions are hard-coded in tests] → `test_platforms.py` assertions split into two sets by length, with the long-form set unchanged (spec `A7.4`).
- [Long- and short-story knowledge have same-named entries, confusing authors or agents] → All short-story files carry short-story marks (file-name prefix `short-` + a scope statement in the file header); deployed products are separate files, not merged.
- [`templates/short/` codex special-casing and path rewriting follow the same logic, so short-story-specific files may be wrongly rewritten] → `create_skeleton`'s length branch only changes the **tree root**, with the rewriting logic reused; E2E assertions cover codex short-story products (spec `A4.3`).
- [`reader` is reused but its SOP is still long-form wording, so short-story acceptance focuses (completion rate / spread desire) may not be covered] → The structure-side payoff check is already carried by the independent verifier agent (D3/D11); `reader` only handles experience. This round adds a short-story supplement to `reader-review.md` (without changing existing long-form entries).
- [Contract overload: short stories are only 8,000 to 12,000 words, so an overlong contract squeezes the writer's context, and the more rules pile up, the easier they are to ignore] → The contract is one per story (not one per section), the assembly side keeps a sense of total volume (techniques take only 1-2 entries per scene), and the contract audit lists "whether suggestive techniques leaked into the hard-rules zone" as a must-check item.
- [The contract becomes a new template: every story's contract has the same structure, equal to moving the template fingerprint from the main text to the contract, where it still seeps into the main text] → The contract's hard-rules zone only holds this story's specific red lines and numbers, with general writing standards referenced on demand rather than moved over wholesale; the de-AI criteria keep the "this story's techniques, opening, and ending differ from the previous story" self-check item (spec `AR5.4`).
- [The payoff check becomes formalism: checking just to fill the list, finding no real problems] → The judgment wording matches the existing audit: "the standard for passing an audit is having no sufficient evidence of a problem", and undelivered items must carry quoted main-text evidence; reporting a conclusion alone is not allowed.
- [After narrowing scope, authors who "do not know what to write" have no path to a product] → The writing pipeline's first stage (set the emotion and direction) already provides guided topic selection: six emotion goals, each with recommended genres and market heat (spec `D1.1`), enough to support "from zero to one story"; list scanning is only needed when "following the current market trend", which is an optional enhancement.
- [Narrowing is read as "these capabilities will not be done"] → The proposal's "Later Changes" section records each moved-out item with its reason, and tasks keep no leftover entries for them, avoiding forgetfulness.
- **[The contract decays across batches: one per-story contract plus batched writing means the last batch is several times further from the rules than the first, so the second half starts slipping while word counts still pass]** → Before each batch of writing, the contract's hard-rules zone MUST be fully re-injected (spec `D5.10`/`D5.11`), without relying on the writing side to look it up itself. This is the main gap the review added: it is not one requirement being violated, but **no requirement at all covering this**. Residual risk: re-injection adds one extra copy of the rules to each batch's context, a necessary cost.
- **[Paragraph and section word-count wordings fight: the opening part at 300-500 words and the ending part at 400-800 words both fall below the 800-word per-section floor]** → At spec level, paragraphs and sections are fixed as two orthogonal descriptions (`D5.8`/`D5.9`), with one-to-one mapping and per-part exemptions banned. **Do not adjudicate at runtime**: the first draft handed this conflict to the "contract inlined conflict adjudication table", equal to making the concept agent re-adjudicate a numeric contradiction on the spot for every story, when it is not a math checker and its adjudication results have no stability.
- **[No revision path after delivery: no writer is satisfied in one draft]** → Add the `D8` revision requirement: feedback is first located to a stage (concept / outline / specific sections), only the affected parts roll back, affected gates re-run, and the state machine supports partial rollback that keeps the rest of the progress.
- **[2-3 core techniques cannot fill 10 sections, so the middle has nothing to write and gets padded]** → Two layers of response: `outline.md` MUST contain the emotion-chain landing (D14, with section counts unfolding naturally from the chain's stages) and the technique landing table, and every section MUST take on at least one of six function types (`D2.6`/`D2.7`). Sections the techniques do not cover are carried by adding pressure, foreshadowing, relationship change, emotion delivery, and supporting-character subplots.
- **[Character naming lands in the model's highly convergent name pool, becoming a machine trace readers can recognize]** → `AR8`: constrain with a decidable banned list (full names + characters + homophones), and MUST NOT use "random generation" as the mechanism. Randomness is not reproducible in a language model, so revisions would change names, which would directly break `D8`'s minimal rollback (rewriting a few sections while changing a character's name). So naming results MUST be saved as a record, with later stages following the record.
- **[The emotion chain degrades into a new template: every chain fixed to the same section-count allocation, equal to moving the template from the main text to the skeleton]** → The chain only fixes the stage sequence; how many sections each stage covers is derived from this story's genre and target word count and MUST NOT be fixed; the `AR5.4` self-check item ("this story's techniques, opening, and ending differ from the previous story") also covers the chain's selection.
- **[Formulaic techniques degrade into "applying formulas": every technique carrying a formula and an example makes it easier to copy verbatim]** → `D3.2` already requires techniques to be transformed into this story's writing (anchoring the protagonist, information gap, and emotional rhythm); `D2.10` only requires entries to pair "formula + example" so they are usable when picked, and does not replace the transformation step.

## Migration Plan

0. **A minimal runnable slice goes first** (implementation strategy, not a standalone step): after this change is fully laid out, it is 10 genre packs x 7 platforms x 26 knowledge files, and **nothing runs end to end until all of it is done**. That order is itself a risk: whether the chain holds together is only known at the end. So implement in this rhythm:
   - **First wave (run the chain through)**: 1 genre pack (wife-chasing crematorium, the most complete one in the short-story pack), 1 platform (first on Claude or Zcode alone), knowledge files limited to the three essentials (format spec + de-AI criteria + writing base), length pressed to 3-4 sections. The goal is to **produce one `manuscript.md` end to end**, verifying that the chain of contract assembly, audit, batched writing, de-AI pass, and payoff check really runs.
   - **Second wave (fill in)**: add the 10 genres and all writing references, plus 7-platform adaptation and E2E assertions.
   - **Third wave (wrap up)**: docs, compatibility regression, full-flow live tests.
   - Criterion: if the first wave cannot run, the problem is certainly in the chain design rather than the material volume, and rework costs the least at that point.

1. **Skeleton and switch**: `templates/short/` + `init.py --length` + `platforms.py` roster constants. Verify: short-story initialization products have the right directory tree, and existing initialization products are unchanged.
2. **Agent group and SOPs**: 5 short-story agents + 7 short-story SOPs, wiring frontmatter references, and producing the short-story check-item grading list (D2). Verify: `check-agents.py` passes; every list item is marked with its owner.
3. **Knowledge moving**: `knowledge/short/` in three subdirectories, with D9's three rewrites; at the same time, add AR7's paragraph-shape floor and ceiling into the format spec and de-AI criteria (D12). Verify: `check-agents.py` + `check-conflicts.py` pass, and external-reference grep is at zero.
4. **Contract layer**: the contract assembly SOP, contract audit SOP, and payoff-check SOP land, and the short-story dispatch contract wires the seven phases and three gates (contract audit / payoff check / experience acceptance) into the order-type table. Verify: contract products contain six elements with descending priority, the audit's five items are complete, and the payoff checklist can produce conclusions item by item.
5. **Platform adaptation and E2E**: `deploy_inline_skills` length branch, codex/grok short-story products, `sync-project.py` length recognition, `check-agents.py` dual-length simulation. Verify: `test_platforms.py` short-story cases all green.
6. **Entry point and docs**: `SKILL.md` routing and boundary conditions, README / ARCHITECTURE.
7. **Live test**: from "say one sentence, write a short story" to receiving the finished main text on at least one AI terminal, covering both the expert straight-through path and the guided path, with the payoff check really blocking one deliberately constructed undelivered item.

**Rollback**: revert the whole thing. No data migration, no state upgrade. Short-story projects are a newly created independent type; existing projects' indexes carry no length marker and are handled per the established behavior, matching the pre-change state. No short-story projects exist yet (there was no short-story capability before this change).

## Open Questions

(None. The three out-of-scope items are recorded in the proposal's "Later Changes" and get separate proposals; whether short stories need style-distillation wiring is listed in Non-Goals.)
