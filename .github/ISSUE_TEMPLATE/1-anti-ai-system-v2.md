---
name: Anti-AI System Upgrade v2 - From Rule List to Root Causes
about: Based on deep research into the salt-story project, systematically upgrade awesome-novel's anti-AI writing system
title: "[RFC] Anti-AI System Upgrade v2: From Checklist to Root Causes"
labels: enhancement, anti-ai, rfc
assignees: ""
---

## Background

awesome-novel's current anti-AI system (`memory/anti-ai/`) already has a rule system: fatigue-word thresholds, banned sentence patterns, meta-narrative filtering, externalized-emotion rules, and more. The system works, but it has a fundamental problem:

**It is a "symptom checklist": it tells the AI what not to do, but never tells the AI why not.**

Through deep research into the [salt-story](https://github.com/your/salt-story) project's anti-AI methodology, we found it builds a complete cognitive system from `Layer 0: root causes → Layer 1: sentence level → Layer 2: paragraph level → Layer 3: full-text level → Layer 4: temperament level`. It not only wrote 20+ stories that passed Yanxuan editorial review, its output is also nearly unrecognizable as AI in Tieba/Douban tests.

This RFC proposes integrating salt-story's anti-AI cognitive framework into awesome-novel systematically.

---

## 1. The Five Root Causes of AI Flavor (salt-story's Core Theory)

> **The essence of AI flavor is not a few words or patterns. It is an excess of order: AI prose reads like a person dressed perfectly but with hollow eyes.**

### Root Cause 1: Regression to the Mean
AI tends to generate "the most likely next word", so all output converges toward the average. Human writing has extreme values: especially good and especially bad sentences coexist.

**Effect on generation**: AI writes neither "killer lines" nor "bad lines". Removing the low-scoring region also removes the high-scoring region.

### Root Cause 2: Symmetry
AI loves symmetric structures ("not A but B", "both A and B"). Human writing is asymmetric: it leans to one side and ignores the other.

**Effect on generation**: Symmetric structures are not wrong by themselves, but when they repeat throughout a text they expose it as "the most probable sequence AI would generate".

### Root Cause 3: Emotional Correctness
AI's emotional reactions are always "reasonable". Human emotional reactions are often misplaced, contradictory, and out of proportion.

**Effect on generation**: Reasonable emotions are never wrong, but they never make the reader feel "a real person is talking". Misplaced emotions are what feel human.

### Root Cause 4: Lossless Information Transfer
Every AI sentence carries information; there is no genuine "filler". Human writing is full of genuine filler, and that filler is the core of what feels human.

**Effect on generation**: AI text has "uniform information density": every paragraph advances the plot. Human writing pauses, drifts off, and writes things that seem irrelevant.

### Root Cause 5: Perspective Stability
AI first-person narration reads like an omniscient view: perfect observation, precise description. Human first-person narration has blind spots, biases, and self-deception.

**Effect on generation**: AI first-person narration is always reliable; unreliable human first-person narration is the norm.

**Once you understand these five root causes, you can invent countless de-AI-flavor techniques yourself instead of relying on a static ban list.**

---

## 2. Gap Analysis of the Current System

### ❌ Missing Layers

| Layer | Current State | salt-story's Approach |
|------|---------|-----------------|
| **Layer 0: Root-Cause Theory** | None | 5 root-cause explanations (regression to the mean, symmetry, emotional correctness, etc.) |
| **Layer 1: Sentence Level** | ✅ Fatigue-word thresholds + banned sentence patterns | Same level, plus an explanation of "why this has AI flavor" |
| **Layer 2: Paragraph Level** | ⚠️ Paragraph-length rules (25%-45% single-sentence paragraphs) | More granular: paragraph rhythm distribution (uneven is human), emotional arc (ECG shape), broken causal chains |
| **Layer 3: Full-Text Level** | ❌ Partially present | Information-density distribution (a drumbeat, not white noise), character language DNA tables, limited narrator perspective |
| **Layer 4: Temperament Level** | ❌ Completely missing | Imperfect beauty, obsession/fixation, humor/self-mockery, silence/negative space |

### ❌ Missing Processes

| Process | Current | salt-story |
|------|------|-----------|
| **Character Language DNA Table** | Character settings exist, but no language-feature dimensions | Required before writing: average sentence length, word register, catchphrases, speech habits, and 6 other dimensions |
| **Paragraph Rhythm Distribution Check** | None | Uneven distribution: 20-30% single-sentence paragraphs, 15-20% two-sentence, 20-25% three-sentence |
| **Uneven Information Density** | None | Deliberately vary information density: some paragraphs extremely dense, others with almost no new information |
| **Limited Narrator Perspective** | Perspective rules ask to "focus on the protagonist" but do not require "limitedness" | The narrator misses obvious things, misunderstands others, over-focuses on irrelevancies, and reconstructs memories after the fact |
| **Multi-Model Cross-Review** | None | 3 rounds: Opus (timeline + twists) → GPT (logic + AI flavor) → Opus (speed-up) |
| **Tieba Test** | None | Final check: post anonymously to Tieba, 3 randomly drawn passages; would anyone say AI wrote this? |

### ✅ Present but Needs Strengthening

| Present | Strengthening Direction |
|------|---------|
| `memory/anti-ai/common-rules.md` | Add root-cause explanations + paragraph-rhythm distribution requirements + uneven information-density requirements |
| Genre anti-AI files (❌/✅ mode) | Add more explanations of "why this pattern has AI flavor" |
| `chapter-quality-checklist.md` | Add Layer 0 + Layer 4 check items |
| `writing-execution.md` | Add "anti-AI-flavor" rules to the sub-agent execution instructions |
| `writing-style.md` four fields | Add an explicit "limited perspective" requirement to the narrative identity |

---

## 3. Implementation Plan

### Phase 1: Knowledge Base Upgrade (`memory/anti-ai/`)

#### 1.1 Upgrade `common-rules.md`: Add Root-Cause Theory + Paragraph Rhythm + Information Density

Add a **"Five Root Causes of AI Flavor"** section at the top of `common-rules.md`. Add chapters:

- **Paragraph rhythm distribution rules**: 20-30% single-sentence paragraphs, 15-20% two-sentence, 20-25% three-sentence, ~10% four-sentence, 5-8% five-sentence
- **Uneven information-density rules**: create sparse/dense rhythm instead of distributing information evenly
- **Emotional arc rules**: a jagged ECG-style rise and fall, not smooth
- **Broken causal-chain rules**: going off-topic allowed, unrelated details placed side by side allowed, "dead threads" allowed

#### 1.2 Upgrade Each Genre's Anti-AI File

Add to every `memory/anti-ai/{genre}.md`:

- One root-cause explanation per ❌ pattern ("why this is AI flavor")
- **Limited narrator perspective** positive/negative examples (for that genre)
- **Temperament-level** positive/negative examples: imperfect expression, obsession/fixation, humor/self-mockery, silence/negative space

#### 1.3 New Knowledge Files

| File | Content | Priority |
|------|------|--------|
| `memory/anti-ai/root-causes.md` | Full five-root-cause theory + hands-on comparison table (AI version / improved version / viral-hit version of the same passage) | P0 |
| `knowledge/character-craft/character-dna-table.md` | Character language DNA table template (6 dimensions: sentence length, word choice, catchphrases, speech habits, information-leak style, emotional expression) | P0 |
| `knowledge/plot-craft/information-density.md` | Information-density control methodology (drumbeat model, sparse/dense rhythm, buildup and release) | P1 |
| `knowledge/narrative/flawed-narrator.md` | Limited-narrator techniques (blind spots, bias, self-deception, retrospective reconstruction) | P1 |

### Phase 2: Process Upgrade (Writing Workflow)

#### 2.1 writer agent Upgrade

Add to `writing-execution.md`:

```
## Anti-AI-Flavor Rules (Enhanced)

### Paragraph Rhythm: Check Sentence Counts Paragraph by Paragraph After Writing
- 1-3 sentences per paragraph; anything over 3 sentences must be broken up
- Single-sentence paragraphs at least 25%
- 3 consecutive paragraphs of similar length must be broken up

### Emotional Arc: Not Smooth
- At least 1 "misplaced emotion" per chapter (laughing when one should cry, spacing out when one should be furious)
- Emotional outbursts must be sudden, not "slowly building until finally unable to hold back"

### Information Density: Uneven
- At least 1 "sparse" paragraph with almost no new information: pure state description or idle brushstrokes
- Plot-advancing and non-advancing paragraphs alternate
- At least 1 "filler" passage in the whole text (everyday idle brushstrokes, unrelated to the main line)

### Imperfect Narrator
- The narrator may miss obvious things ("What exactly was I wearing that day? I don't remember.")
- The narrator may judge wrong ("I thought he was helping me at the time. Only later did I learn he wasn't.")
- The narrator may over-focus on irrelevant details (out of anxiety/bias)

### Temperament Requirements
- At least 1 "rough-edged expression" (non-standard word order, imprecise wording that still lands)
- At least 1 self-mockery or dark humor moment
- The same key detail appears at least 2 times (a sense of obsession/fixation)
- At least 1 "negative space": action/silence instead of an emotional explanation
```

#### 2.2 reader agent Upgrade

Add a **"Human-Feel Index"** review dimension to the reader's review dimensions:

7. **Human-Feel Index (new)**
   - Is the paragraph rhythm uniform (uniform = AI trait)?
   - Are emotional changes smooth (smooth = AI trait)?
   - Is information density too uniform (too uniform = AI trait)?
   - Does the narrator have blind spots (omniscient = AI trait)?
   - Is there any roughness (too polished = AI trait)?

#### 2.3 prompt-crafter Upgrade

Add to the `Output · Writing Standards` section of `prompt-setting-style.md`:

- Add **paragraph rhythm requirements** (uneven distribution)
- Add **emotional arc requirements** (ECG-style, not a sine wave)
- Add **information-density control** (sparse/dense alternation)
- Add a hard constraint for the **limited narrator perspective**
- Add a **roughness** requirement (imperfect expression)

### Phase 3: Quality Management Upgrade

#### 3.1 Body-Text Acceptance Checklist Upgrade

Add new check dimensions to `chapter-quality-checklist.md`:

```markdown
## AI-Flavor Deep Check (6 New Dimensions)

### 1. Paragraph Rhythm Distribution (the Most Important AI Fingerprint)
- [ ] Single-sentence paragraphs ≥ 25%? (Below 25% is probably AI)
- [ ] No 3 consecutive paragraphs of similar length?
- [ ] Longest paragraph ≤ 5 sentences? (Break up anything over 5 sentences)

### 2. Emotional Arc
- [ ] At least 1 misplaced emotion? (Not reasonable emotional reactions throughout)
- [ ] Is the outburst abrupt? (Not the "slowly building until it can't be held back" pattern)

### 3. Information Density
- [ ] At least 1 paragraph with extremely low information density (pure state/idle brushstrokes)?
- [ ] No obvious "every paragraph advances the plot" uniformity?

### 4. Character Language Differentiation
- [ ] With character names covered, can you tell who is speaking? (Randomly draw 3 dialogue passages)
- [ ] Do characters differ clearly in speech length / vocabulary / habits?

### 5. Narrator Limitations
- [ ] Does the narrator observe every detail? (Too perfect = AI)
- [ ] Does the narrator have clear subjective biases?

### 6. Human-Feel Overall Score
- [ ] Tieba test: post 3 passages anonymously; would they be recognized as AI?
- [ ] Roughness: at least 1 "not quite perfect" expression?
- [ ] Negative space: any place where action/silence replaces an emotional explanation?
```

#### 3.2 Multi-Model Cross-Review (New Step)

Add an optional **cross-review phase** to the writing flow:

```markdown
## Cross-Review Process (Optional, Before reader review)

### When to Use
- Enable when the closest-to-human-written effect is needed
- Controlled by the author through status.md's cross_review: true/false

### Process
1. **Round 1: Anti-AI Check** (current model or a fast model)
   - Check fatigue-word overruns, pattern violations, paragraph rhythm distribution
   - Save as {chapter}.draft.ai-checked.md

2. **Round 2: Human-Feel Enhancement** (full model)
   - Add roughness, misplaced emotions, limited perspective, negative space
   - Save as {chapter}.draft.humanized.md

3. **Round 3: Full Read-Through** (author or their designated model)
   - Confirm the human-feel enhancement did not break the narrative, without losing plot integrity
```

### Phase 4: Config and Template Upgrades

#### 4.1 `writing-style.md` Upgrade

Add to the four fields:

**Narrative identity** gains a limited-perspective constraint:
```yaml
narrative_identity:
  # existing content + new:
  imperfection_limits: the narrator has blind spots, biases, fuzzy memory
  human_feel_constraints: filler allowed, zoning out allowed, misplaced emotions allowed
```

**Common mistakes** gains:
```yaml
common_mistakes:
  # existing entries +
  - uniform paragraph lengths (3+ consecutive paragraphs with the same or similar sentence counts)
  - smooth emotional change (no abrupt emotional turns)
  - uniform information density (every paragraph advances the plot)
  - an "omniscient" narrator (noticing every detail)
  - no rough edges (prose too smooth, too perfect)
```

#### 4.2 New Files Deployed at Project Init

`init.py` needs to deploy these for every new project:
- `.claude/knowledge/anti-ai/root-causes.md` (root-cause theory)
- `.claude/knowledge/character-craft/character-dna-table.md` (character DNA table template)
- `.claude/knowledge/plot-craft/information-density.md` (information-density control)

---

## 4. Relationship to the Existing System

This upgrade is an **enhancement, not a replacement**:

| Existing System | Relationship |
|---------|------|
| `memory/anti-ai/common-rules.md` | Keep; add root-cause theory at the front |
| `memory/anti-ai/{genre}.md` | Keep; add a "why this has AI flavor" explanation to every rule |
| `chapter-quality-checklist.md` | Keep; add 6 new deep-check dimensions |
| `writing-execution.md` | Keep; strengthen the anti-AI-flavor rules |
| `writing-style.md` four fields | Keep; add limited-perspective and roughness constraints |

---

## 5. Implementation Priority

| Priority | Content | Effort | Depends On |
|--------|------|--------|------|
| **P0** | Root-cause theory into `common-rules.md` | Low | None |
| **P0** | Paragraph rhythm distribution rules | Low | None |
| **P0** | writer execution instruction enhancement (paragraph rhythm + misplaced emotion + limited perspective + roughness) | Medium | None |
| **P0** | `chapter-quality-checklist.md` adds 6 new dimensions | Medium | None |
| **P1** | Character language DNA table (`knowledge/character-craft/`) | Medium | None |
| **P1** | Root-cause explanations in each genre's anti-AI file | High | P0 |
| **P1** | prompt-crafter injection upgrade | Medium | P0 writer upgrade |
| **P2** | Information-density control methodology | Medium | P0 |
| **P2** | Limited-narrator technique document | Medium | P0 |
| **P2** | Cross-review process | High | P0 |
| **P3** | `writing-style.md` four-field enhancement | Low | P0 |

---

## 6. Acceptance Criteria

- [ ] Every writer sub-agent runs the enhanced anti-AI-flavor rules
- [ ] `common-rules.md` contains the five-root-cause theory
- [ ] Every rule in each genre's anti-AI file is labeled with its root cause
- [ ] The body-text acceptance checklist includes paragraph rhythm distribution checks
- [ ] The prompt output module includes limited-perspective constraints
- [ ] At least 1 real project runs the full flow and produces body text with under 10% AI detection rate
- [ ] The character DNA table works in new projects

---

## 7. References

This upgrade is based on deep research into the [salt-story](https://github.com/your/salt-story) project's anti-AI methodology. Key reference files:

- `references/anti-ai.md`: complete check system from sentence level to temperament level + hands-on comparison tables
- `references/principles.md`: root principles (information-asymmetry economics, reader psychology, platform algorithms)
- `references/case-studies.md`: viral-hit teardowns (Ye Xiaobai's 35,000 likes and more)
- `SKILL.md`: complete Yanxuan story writing flow (de-AI flavor, multi-model cross-review)

---

Please discuss this proposal in the community before implementing. Supplements and improvements are welcome in the comments.
