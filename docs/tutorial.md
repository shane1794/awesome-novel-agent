# awesome-novel-agent User Manual

Using the xianxia (immortal cultivation) novel *Qingyun Chronicles* as the worked example, this manual walks through the full process of writing a novel from scratch.

---

## Table of Contents

1. [Installation and Setup](#1-installation-and-setup)
2. [Start Writing](#2-start-writing)
3. [Phase 1: Setup](#3-phase-1-setup)
4. [Phase 2: Main Arc Breakdown and Volume Outlines](#4-phase-2-main-arc-breakdown-and-volume-outlines)
5. [Phase 3: Chapter-by-Chapter Writing](#5-phase-3-chapter-by-chapter-writing)
6. [Continuing with Chapter 2](#6-continuing-with-chapter-2)
7. [Frequently Asked Questions](#7-frequently-asked-questions)

---

## 1. Installation and Setup

### 1.1 Prerequisites

- You can open a command-line terminal (Windows: PowerShell or CMD; Mac/Linux: Terminal)
- You have a network connection (to download the installer)

### 1.2 Installation Steps

Copy the following message to your AI:

> "Help me install awesome-novel-agent. The repository is at https://github.com/modoojunko/awesome-novel-agent"

---

> **About the multi-agent collaboration architecture:** This system is driven by 8 collaborating agents. `@novel-agent` is the top-level entry point, loaded by the main AI to play the commander role. It does not write content directly; instead, it dispatches sub-agents through the Agent tool (volume-planner / chapter-planner / prompt-crafter / writer / reader / anti-ai / updater), each doing its own job. When a sub-agent finishes, it clears its task marker, and novel-agent detects this and automatically advances to the next phase.

---

**The AI will help you:**

1. Download the latest version
2. Run the install script for your platform (`./install.sh <platform>`) to install the skill itself
3. Configure it into your AI tool

---

**Platforms supported by the install script:**

| Platform | Command |
|------|------|
| Claude Code | `./install.sh claude-code` |
| OpenCode | `./install.sh opencode` |
| Codex | `./install.sh codex` |
| Reasonix | Project-level deployment: `python tools/init.py <project path> --platform reasonix` (does not go through install.sh) |

> `install.sh` is also compatible with deepseek-tui / hermes / openclaw; on Windows PowerShell, run `install.ps1 <platform>`.

---

**If the AI says it does not know this project, try this instead:**

> "Go to https://github.com/modoojunko/awesome-novel-agent/releases, download the latest release, then install it following the README"

(Reasonix does not go through install.sh: after cloning, initialize with `python tools/init.py <project path> --platform reasonix`.)

---

### 1.3 Verify the Installation

After installation, open your AI tool in the directory where you want to put your novel project and type:

```
/awesome-novel
```

The skill will first confirm and initialize the novel workspace; if novel-writing guidance appears, the installation succeeded.

---

## 2. Start Writing

### 2.1 Trigger

Type in your AI tool:

```
/awesome-novel
```

Or just say:

> Help me write a novel

In Codex, type `/use awesome-novel`.

### 2.2 Automatic System Detection

The AI detects a new project and starts initialization:

```
Detected: no story.md → new project
Running init.py to initialize the skeleton...
```

---

## 3. Phase 1: Setup

The setup phase is completed in one go, covering: genre selection, writing style, worldview, and character setup.

---

### 3.1 Create the Project

**[AI]** announces:

> "I will guide you through the novel setup. First, let us confirm the project's basic information."

**[AI]** runs init.py (the `tools/init.py` under this skill's install directory; the AI locates it automatically):

```bash
python <this skill's install directory>/tools/init.py
```

`init.py` automatically creates the project skeleton; no extra parameters are needed.

---

**[Author]** answers:

> The book is called *Qingyun Chronicles*, and the author's name is Zhang San.

---

### 3.2 Genre Selection

**[AI]** uses the conversation-guided method:

> "What kind of story do you have in mind? Do not worry about genre labels; just tell me who the protagonist is, what world they are in, and what they do."

---

**[Author]** answers:

> "I want to write a xianxia (immortal cultivation) story, where the protagonist starts as a mortal, cultivates step by step, and finally ascends to become an immortal."

---

**[AI]** extracts the key signals from the description:

| Key Signal | Matching Type |
|---------|---------|
| Eastern world + immortal cultivation / Dao cultivation / true cultivation | Eastern xianxia |

> "It sounds like you are writing **Eastern xianxia (immortal cultivation)**: the protagonist cultivates in an immortal cultivation world and ascends. Is that right?"

---

**[Author]** confirms:

> "Yes, exactly xianxia."

---

### 3.3 Writing Style Confirmation

**[AI]** states the default setting:

> "writing-style.md is pre-filled with the 'low-AI-flavor optimized edition': natural and relaxed, enforced sentence patterns, no technique stacking, no poetic register."

**[AI]** AskUserQuestion:

> A. Use the default
> B. Adjust it
> C. Use my own style

---

**[Author]** answers:

> "A. Use the default"

---

**[AI]** diagnoses:

> "What are your three favorite novels or films? What draws you to them most?"

---

**[Author]** answers:

> "*Battle Through the Heavens*, *A Record of a Mortal's Journey to Immortality*, *Renegade Immortal*. I like the feeling of the protagonist growing from weak to strong, step by step."

---

### 3.4 Genre Profile Selection (Optional)

**[AI]** shows the 24 genre profiles:

```
1. Eastern xianxia - immortal cultivation / Dao cultivation / true cultivation
2. Traditional xuanhuan - otherworld continent + high martial arts + trash-to-power comeback
3. Urban (major category) - modern urban base category (sub-category variants cover the differentiating fields)
4. Urban romance - modern urban + romance / love
5. Urban slice-of-life - modern urban + everyday emotion + real life
6. Urban farming - modern urban + farming and construction + business-war workplace
7. Urban brainstorm - modern urban + cheat power + wild ideas
8. Urban cultivation - modern urban + immortal cultivation / true cultivation system
9. Urban high-martial - modern urban + universal cultivation + spiritual energy revival
10. God-of-war son-in-law - modern urban + war god returns + son-in-law comeback
11. Western fantasy - Western world + magic / battle aura / fantasy
12. Ancient court intrigue - ancient court + power schemes / vying for supremacy
13. Historical (major category) - ancient background base category (sub-category variants cover the differentiating fields)
14. Historical ancient - ancient background + farming / court / vying for supremacy
15. Historical brainstorm - ancient background + cheat power + wild ideas
16. War of Resistance espionage - War of Resistance era + military / espionage
17. Sci-fi apocalypse - apocalypse / zombies / interstellar / mecha / future tech
18. Suspense crime - modern + case-solving / deduction / criminal investigation
19. Suspense supernatural - modern + supernatural / feng shui / horror
20. Suspense brainstorm - eerie revival + rules-based horror tales + horror games
21. Gaming and sports - online games / competitive / sports / gamified world
22. Anime derivative - games / anime / 2D fan fiction
23. Derivative (category) - derivative base category (shared corpus)
24. Male-oriented derivative - film and TV fan-fiction adaptations
```

> The number maps one-to-one to `init.py --genre <number>`; you can also skip the number, just describe the story you want to write, and let the AI match the genre.

---

**[Author]** answers:

> "1. Eastern xianxia"

---

**[AI]** shows the profile summary:

> **Genre profile: Eastern xianxia**
> - Style and prose: half-classical, half-vernacular, poetic yet grounded in real life
> - Core atmosphere: airy and otherworldly, without losing the smoke of everyday life
> - Exclusive elements: spirit-root system, elixirs and cultivation techniques, sects and schools
> - Narrative point of view: third-person limited
> - Genre taboos: jumping off a cliff always yields a lucky encounter, system-driven stories

---

**[Author]** confirms

---

### 3.5 Genre Configuration (5 Fields)

**[AI]** has a genre profile selected, so it shows the merged configuration and asks "Anything to adjust?"

> If the author picks "Not choosing for now", discuss each of the 5 fields one by one:
> - Payoff type (oppression → gain → release → oppression again)
> - Pacing rules (more action / more setup / alternating tension and release / tense throughout)
> - Clichés to avoid (jumping off a cliff always yields a lucky encounter / the heroine throwing herself at the hero, and so on)
> - Genre taboos (gore / killing without cause, and so on)

---

**[Author]** answers:

> "Fine, no adjustments needed."

---

### 3.6 Worldview (3 Items)

**[AI]** discusses geography item by item:

> **[Geography]**
>
> Where does your protagonist act? From where to where?
>
> - Starting point: a small sect in the mortal world (the protagonist's family)
> - Middle: a great immortal cultivation sect (Qingyun Sect)
> - End point: the immortal realm (optional after ascension)

---

**[Author]** answers:

> "The starting point is a small sect in the mortal world, then he goes to Qingyun Sect to cultivate. The immortal realm can be added, but I will add one setting: the immortal realm is actually a puppet cage."

---

**[AI]** continues with politics:

> **[Politics]**
>
> Who calls the shots? Who holds him back? What happens if he refuses? (At least 2 factions)

---

**[Author]** answers:

> "Qingyun Sect is the leader of the righteous path, but inside it there is a traitor, Chen Feng, who is secretly colluding with the Heavenly Demon Sect."

---

**[AI]** continues with the rules:

> **[Rules]**
>
> What are this world's cultivation rules? What are the spirit-root system, the cultivation levels, and the core rules?

---

**[Author]** answers:

> "Qi Refining → Foundation Establishment → Golden Core → Nascent Soul → Soul Transformation → Tribulation Transcendence → Immortal. The protagonist has a heavenly spirit root, but Chen Feng sealed it, so on the surface it looks like a trash spirit root."

---

**[AI]** confirms the geography / politics / rules and writes them into `settings/world-setting.md`

---

#### 3.6.1 Self-Check (Worldview)

**[AI]** checks the written settings:

1. **Geography completeness check**: Are there three levels, starting point / middle / end point?
2. **Politics plausibility check**: Are the faction relationships clear, with no logical holes?
3. **Rules executability check**: Can readers understand them, and can they be applied while writing?
4. **Conflict space check**: Is there righteous-versus-evil opposition and internal contradiction?

---

### 3.7 Character Setup

**[AI]** collects the characters:

> "Which characters does your story have? Protagonist, villain, heroine / close friend, mentor?"

---

**[Author]** answers:

> "The protagonist is Lin Yi, the villain is Chen Feng, the heroine is Su Qing, and the mentor is Yunxiaozi."

---

#### 3.7.1 Protagonist Setup

**[AI]** discusses Lin Yi's basic information:

> **[Lin Yi: Basic Information]**
>
> - Name: Lin Yi
> - Background: outer disciple of Qingyun Sect; his father was once an inner elder
> - Appearance: a handsome youth, with a knot of gloom between his brows

---

**[AI]** expands it with the six-layer cognition model:

| Layer | Content |
|------|------|
| Worldview | "This world is unfair, but I will find the truth" |
| My position | Outer disciple of Qingyun Sect, the unrecognized eldest son of the Lin family |
| Values | A debt must be repaid, but revenge needs a just cause |
| Abilities | A sealed heavenly spirit root, the cultivation technique his father left behind |
| Skills | Basic swordsmanship, a resilient mind |
| Environment | The outer sect of Qingyun Sect, a pressured situation |

---

**[AI]** writes it into `settings/character-setting/林逸.md`

---

#### 3.7.2 Villain Setup

**[AI]** discusses Chen Feng:

> **[Chen Feng]**
>
> - Name: Chen Feng
> - Identity: inner elder of Qingyun Sect
> - Appearance: a middle-aged man with a refined, scholarly look
>
> | Layer | Content |
> |------|------|
> | Worldview | "Might is right; the weak deserve to be trampled" |
> | My position | Inner elder of Qingyun Sect, a respected senior |
> | Values | "Success is justice; the means do not matter" |
> | Abilities | Nascent Soul stage cultivation, superb scheming |
> | Skills | Qingyun swordsmanship, secretly colluding with the Heavenly Demon Sect |
> | Environment | The upper levels of Qingyun Sect, with power and resources |

---

**[AI]** writes it into `settings/character-setting/陈风.md`

---

#### 3.7.3 Heroine Setup

**[AI]** discusses Su Qing:

> **[Su Qing]**
>
> - Name: Su Qing
> - Identity: outer disciple of Qingyun Sect, junior sister
> - Appearance: a young girl with bright eyes and white teeth, with two dimples when she smiles
>
> | Layer | Content |
> |------|------|
> | Worldview | "The world is beautiful, but it has a dark side too" |
> | My position | Outer disciple of Qingyun Sect, an innocent and cute junior sister |
> | Values | "Protect the people who matter" |
> | Abilities | A hidden nine-yin constitution (not yet discovered) |
> | Skills | Lively and cheerful, able to sense danger |
> | Environment | The outer sect of Qingyun Sect |

---

**[AI]** writes it into `settings/character-setting/苏晴.md`

---

#### 3.7.4 Mentor Setup

**[AI]** discusses Yunxiaozi:

> **[Yunxiaozi]**
>
> - Name: Yunxiaozi
> - Identity: supreme elder of Qingyun Sect
> - Appearance: a white-haired old man, with the bearing of a Daoist immortal
>
> | Layer | Content |
> |------|------|
> | Worldview | "The great Dao is formless; follow nature" |
> | My position | Guardian of Qingyun Sect, uninvolved in worldly affairs |
> | Values | "Look only at character, not at talent" |
> | Abilities | Peak Soul Transformation stage, unfathomably strong |
> | Skills | Sees into people's hearts, a mysterious inheritance |
> | Environment | The forbidden grounds of Qingyun Sect, appearing only occasionally |

---

**[AI]** writes it into `settings/character-setting/云霄子.md`

---

#### 3.7.5 Possessions and Experiences

Each character can also record items they hold and major experiences; these are updated automatically by updater during archiving.

```markdown
### Possessions
| Name | Type | Source | Status | Notes |
|------|------|------|------|------|

### Experiences
| Event / Location | Type | Outcome | Status |
|-----------|------|------|------|
```

#### 3.7.6 Self-Check (Characters)

**[AI]** checks each character:

1. **Six-layer cognition completeness check**: Are worldview / position / values / abilities / skills / environment all present?
2. **Motivation clarity check**: What is each character's initial motivation? Is it clear?
3. **Weakness presence check**: Does each character have a weakness? (A villain does not necessarily need one)
4. **Ability boundary clarity check**: What can a character do, and what can they not do?

---

### 3.8 Completion Report

**[AI]** shows:

```
Setup complete.
──────────────────────────────
✅ Written:
  - story.md (Qingyun Chronicles / Zhang San / creation time)
  - settings/writing-style.md (low-AI-flavor style)
  - settings/genre-setting.md (Eastern xianxia)
  - settings/world-setting.md (geography / politics / rules)
  - settings/character-setting/ (4 characters)
📌 Fields to fill in later:
  - character-setting/*.md → speech traits (added during writing)
──────────────────────────────
```

---

**[Author]** confirms:

> "Confirmed. Let us start planning the main arc and volume outlines."

---

## 4. Phase 2: Main Arc Breakdown and Volume Outlines

### 4.1 Announce the Start

**[AI]** announces:

> "I will guide you in planning the story's main arc. First we set the whole-book framework, then expand it into each volume."

---

### 4.2 Determine the Author Type

**[AI]** asks:

> "Do you currently have a complete picture of the whole book's story direction, from opening to ending? Or do you only have ideas for the first volume and will figure out the rest as you go?"

---

**[Author]** answers:

> "I have a rough idea: the protagonist succeeds in his revenge, but I do not know how many volumes it will take."

---

**[AI]** judges: Type A (knows the whole-book direction) → follow the complete flow

---

### 4.3 Main Arc Breakdown

#### 4.3.1 Overall Main Arc

**[AI]** extracts the three elements from the author's description:

> "From what you describe, the main arc is: **Lin Yi grows from a youth abandoned by his sect into an immortal who exposes the truth behind his father's death and succeeds in his revenge**"
>
> Is that right?

---

**[Author]** confirms:

> "Yes, that is it."

---

#### 4.3.2 Set the Ending

**[AI]** asks:

> "What is the last scene of the story? Can you describe that picture?"

---

**[Author]** answers:

> "Lin Yi ascends to the immortal realm, discovers the immortal realm is a puppet cage, defeats the mastermind behind it, and ends up together with Su Qing."

---

#### 4.3.3 Find the Natural Breakpoints

**[AI]** reasons:

> "From the starting point to the ending, the most fundamental changes are:
> 1. Lin Yi goes from 'passively enduring' to 'actively striking'
> 2. Lin Yi goes from 'trusting the sect' to 'seeing through the truth'
>
> Is that right?"

---

**[Author]** confirms

---

#### 4.3.4 Set Each Volume's Conflict

**[AI]** confirms volume by volume:

| Volume | Title | Core Conflict | Estimated Chapters |
|----|------|----------|----------|
| 1 | Mortal World | After his family is wiped out, Lin Yi wanders, finally enters Qingyun Sect, and discovers clues | 10 |
| 2 | The Sect | Intrigue inside the sect; he starts to stand out and discovers Chen Feng's plot | 10 |
| 3 | Rising Storm | All-out conflict, a direct confrontation with Chen Feng | 10 |
| 4 | Comeback | The revenge climax: exposing the truth and the decisive battle with Chen Feng | 10 |
| 5 | The Immortal Path | Ascending to the immortal realm, discovering the deception, and the final decisive battle | 10 |

---

**[Author]** confirms or adjusts

---

#### 4.3.5 Write into story.md

**[AI]** writes into `story.md#story_arc`

---

#### 4.3.6 Acceptance: Three-Way Cross-Check

**[AI]** checks three items:

1. **Overall main arc → per-volume check**: Point at the overall main arc and ask for each volume, "Which step of the main arc is this volume?" Can you answer?
2. **Volume sequence check**: Do all the volumes' core conflicts string together into one complete story line? Are there any breaks or jumps?
3. **Reverse inference check**: Looking only at the volume conflicts, can you guess the whole book's core conflict? Or do they each point in different directions?

---

### 4.4 Volume Direction

#### 4.4.1 Use a Story Structure Template for the First Volume

**[AI]** judges: this is the first volume, so use a structure template.

**[AI]** proposes directly (without asking):

> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
>   Volume 1 structure suggestion: three-act structure
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
>
> Suggested chapter count: 10 chapters
>
> Overview of each stage:
> 1. setup (chapters 1-3) → establish the protagonist's situation and the core suspense
> 2. confrontation (chapters 4-8) → conflicts escalate, the protagonist starts cultivating
> 3. resolution (chapters 9-10) → a small climax wraps up, planting Chen Feng foreshadowing
>
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

**[Author]** confirms:

> "This structure works."

---

### 4.5 Volume Outline Discussion

#### 4.5.1 Set the Core Conflict

**[AI]** inherits it from story.md:

> "Core conflict: **After his family is wiped out, Lin Yi wanders, finally enters Qingyun Sect, and discovers clues**"
>
> Anything to adjust?

---

**[Author]** confirms

---

#### 4.5.2 Break Down the Chapters


**[AI]** fills in the chapters stage by stage following the template:

| id | title | Conflict event (who does what + conflict + change) |
|----|-------|-----------------------------|
| 1-1 | Night of the Massacre | On Lin Yi's 9th birthday, the family is ambushed, and his father dies protecting him |
| 1-2 | Life Among the Ruins | A year of wandering life; he discovers his father's keepsake and his resolve for revenge ignites |
| 1-3 | Father's Keepsake | The jade pendant hides a cultivation-technique clue; he starts cultivating |
| 1-4 | Qingyun Sect Takes Disciples | He takes part in the sect selection and enters as an outer disciple |
| 1-5 | Outer Disciple | A life of chores; his first cultivation, discovering his spirit root is abnormal |
| 1-6 | Spirit Root Awakening | Yunxiaozi discovers the truth and secretly gives him guidance |
| 1-7 | Death of a Senior Brother | A senior brother is killed, sparking conflict; he discovers he is being watched |
| 1-8 | Clues Surface | He finds evidence linked to Chen Feng and is noticed by Chen Feng |
| 1-9 | Undercurrents Stir | Chen Feng starts suppressing him; he is framed and punished |
| 1-10 | The Truth About Father | He discovers more clues and resolves to take revenge |

---

**[Author]** confirms the chapter list

---

#### 4.5.3 Write into volume-1.md

**[AI]** writes into `volumes/volume-1.md`

---

#### 4.5.4 Acceptance: Volume-Level Checks

**[AI]** runs 4 checks:

1. **Completeness check**: Read all the chapters together; do they form a complete story? Would removing or adding one chapter still work?
2. **Traceability check**: Point at the core conflict and ask for each chapter, "Which step of the conflict does this chapter advance?"
3. **Progress check**: After each chapter ends, has the story moved forward? (Discovering a clue that affects nothing later is the same as not discovering it)
4. **Title check**: Looking only at the titles, can you guess what happens in each chapter?

---

**[AI]** 15-second quick sniff test:

1. Can you state the core conflict in one sentence without naming any file?
2. Point at any chapter: can you say "what changed after this chapter ends"?
3. Point at any two chapters: can you say "why does chapter 1 come before chapter 2, instead of jumping straight to chapter 3"?

---

### 4.6 Status Update

**[AI]** updates `.agent/status.md`:

```
phase: outline
current_volume: 1
current_chapter: 1
```

---

**[AI]** reports:

> ✅ Volume outline complete
>
> → Dispatch to chapter outline setup

---

**[Author]** answers:

> "Start the chapter 1 outline."

---

## 5. Phase 3: Chapter-by-Chapter Writing

### 5.1 Chapter 1: Night of the Massacre

#### 5.1.1 Announce the Start

**[AI]** announces:

> "I will guide you in planning the chapter outline for volume 1, chapter 1."

---

#### 5.1.2 Direction Input

**[AI]** reads the volume outline:

> Read `volumes/volume-1.md`'s chapters_summary:
> → Chapter 1: Night of the Massacre (flashback), father sacrifices himself

**[AI]** generates the character's voice:

> **[Lin Yi's situation]** 9 years old, innocent and lively, on the night of his birthday
>
> **[Lin Yi's unfinished business]** None (chapter 1, initial state)
>
> **[What Lin Yi wants to do now]** Celebrate his 9th birthday (not yet knowing what is about to happen)

---

**[AI]** collects the four input groups:

| Input | Content |
|------|------|
| Reader gap | None (no suspense left over from the previous chapter's ending) |
| Character state | Lin Yi, 9 years old, innocent |
| Hook inventory | None (old hooks) |
| Volume outline position | setup chapter 1, establishing suspense |

---

**[AI]** synthesizes a direction proposal:

> **Direction proposal:** Night of the Massacre: on Lin Yi's 9th birthday, the family is ambushed, and his father dies protecting him.
>
> Does this direction work?

---

**[Author]** confirms:

> "Yes."

---

#### 5.1.3 Expand the Outline Points

**[AI]** expands the key points (each with a 2-3 sentence anchor description + function type):

| # | Key Point | Function |
|---|--------|------|
| 1 | The Lin family hall, a birthday feast at night, the family eating longevity noodles. Father Lin is weighed down by worries | [Advance plot · setting] |
| 2 | Roof tiles shatter; men in black drop from the sky | [Build suspense] |
| 3 | Father Lin stands in front of Lin Yi and orders him to run | [Advance plot · action] |
| 4 | A man in black draws his sword; Father Lin is struck down (using Qingyun swordsmanship) | [Advance plot · climax] |
| 5 | Father presses the jade pendant into Lin Yi's hand and says "Run, do not look back" | [Build suspense · clue] |
| 6 | Lin Yi climbs out the back window, looks back at the burning house, and disappears into the night | [Transition · emotion] |

---

**[AI]** confirms the word-count target:

> Word-count target: 4,000 words

---

#### 5.1.4 Prohibition List

**[AI]** asks:

> "Are there any scenes, elements, or plot points that must definitely not appear in this chapter?"

---

**[Author]** answers:

> "The killer must not show his true face, and there must be no AI-flavored description."

---

#### 5.1.5 Memo (8 Sections)

**[AI]** fills in:

| Field | Content |
|------|------|
| current_task | On the night of Lin Yi's 9th birthday, the family is ambushed, and his father dies protecting him |
| reader_expectation | The brutal massacre scene, the father's sacrifice, the protagonist's traumatic memory |
| payoff_plan | This chapter is a setup; readers will wonder who wiped out the Lin family |
| downtime_functions | A warm scene of the family of three before the massacre |
| key_choices | Lin Yi chooses to run instead of staying |
| knowledge_state | Lin Yi does not know who the killer is; he only remembers Qingyun swordsmanship |
| required_changes | From an innocent youth to a traumatized child |
| prohibitions | The killer must not show his true face |

---

#### 5.1.6 Emotion Design (6 Fields)

| Field | Content |
|------|------|
| primary_mood | Sadness, tension |
| mood_progression | Warmth → tension → fear → sadness |
| intensity_level | High |
| intensity_peak | The moment the father dies |
| emotional_hook | The father's dying instructions |
| micro_payoffs | The warm family scene, the father's sacrifice, little Lin Yi's tears |

---

#### 5.1.7 Hook Operations

| Type | Content | Payoff Timing |
|------|------|----------|
| Foreshadowing | The killer uses Qingyun swordsmanship | When Chen Feng appears in volume 2 |
| Clue | Father presses the jade pendant into Lin Yi's hand | Chapter 2 |
| Foreshadowing | Father calls out "Junior Brother Chen" | When the truth is exposed in volume 4 |

---

#### 5.1.8 Acceptance

**Step 1: Show the structured feedback**

**[AI]** shows:

```
📋 Chapter 1 outline feedback

This chapter's position: prologue, flashback in nature
Main content:
- The night of Lin Yi's 9th birthday
- The family is ambushed
- The father dies protecting him

Key scenes:
- Birthday feast (characters: Lin Yi, Father Lin, Mother Lin)
- The ambush arrives (characters: men in black)
- The father's sacrifice (climax)
- Lin Yi flees

Conflict progress: suspense established (who wiped out the Lin family?)
Word-count target: 4,000 words
```

---

**Step 2: Self-check list**

**[AI]** checks:

- [x] Word-count target confirmed (4,000+)
- [x] Paragraph distribution confirmed (how many paragraphs advance / transition / plant foreshadowing)
- [x] Each key point maps to a writable scene with a conflict event
- [x] New hooks recorded (Qingyun swordsmanship, jade pendant, "Junior Brother Chen")
- [x] Prohibitions listed (killer's true face, AI flavor)
- [x] The emotion line has three nodes (warmth → tension → sadness)

---

**Step 3: Quick sniff test**

**[AI]** self-checks:

- Can you say how many points there are and what scene each one writes? → ✅
- Can you say what each character knows and does not know? → ✅
- Can you say which old hooks were paid off and which new hooks were planted? → ✅

---

**Step 4: AI-flavor self-check**

**[AI]** checks:

- [x] No omniscient overview ("This chapter tells the story of")
- [x] No abstract psychological summaries ("he felt" / "he realized")
- [x] No analytical conclusions ("this shows" / "this means")
- [x] No literary-commentary tone ("through X, Y is shown")
- [x] No "not X but Y" sentence pattern
- [x] No abstract labels ("relationship progression" / "conflict escalation")

---

**[Author]** explicitly says "yes":

> "Yes, I confirm the chapter outline."

---

#### 5.1.9 Write chapter.md

**[AI]** writes `chapters/vol-1-ch-1.md`, status → `outline`

---

#### 5.1.10 Status Report

> ✅ Chapter outline: `chapters/vol-1-ch-1.md` → `status: outline`
>
> → Dispatch to prompt generation

---

### 5.2 Prompt Generation

**[AI]** generates a 6-module prompt and writes it into `prompts/vol-1-ch-1-prompt.md`:

**Module 1: Basic Positioning**
- Genre: xianxia (immortal cultivation)
- Tone: heavy, sad
- This chapter's position: prologue, flashback in nature
- Word-count target: 4,000 words
- Payoff beats / emotion: a trace of hope within the sadness

**Module 2: Prior Context**
- Recap: none (chapter 1)
- Core scene: night of the massacre
- Emotion line: warmth → tension → fear → sadness

**Module 3: Characters' Immediate States**
- Lin Yi (9 years old): innocent and lively, able to sense danger
- Father Lin: protecting his son, giving dying instructions
- Men in black: masked, using Qingyun swordsmanship

**Module 4: This Chapter's Narrative Tasks**
- Scene breakdown:
  1. [Advance plot · setting] The Lin family hall, birthday feast at night
  2. [Build suspense] Roof tiles shatter, men in black arrive
  3. [Advance plot · action] Father Lin stands in front
  4. [Advance plot · climax] A man in black draws his sword; Father Lin is struck
  5. [Build suspense] Father presses the jade pendant into Lin Yi's hand
  6. [Transition] Lin Yi flees

**Module 5: Prose and Detail Requirements**
- Narrative point of view: third-person limited, focused on Lin Yi
- Description requirements: action description first, psychology hinted through expressions
- Prohibitions: AI-flavored description, killer's true face

**Module 6: Human-Touch Supplement**
- Emotions must feel real: Lin Yi's fear is a child's fear
- Half-classical, half-vernacular, xianxia (immortal cultivation) style

---

### 5.3 Prompt Acceptance

**[AI]** checks 6 items:

1. **Module completeness check**: Are all 6 modules present (positioning / context / characters / narrative tasks / prose requirements / human touch)?
2. **Field fill check**: Are every module's fields filled in? Are there any "______" placeholders left?
3. **writing-style injection check**: Are core_principles / possible_mistakes / depiction_techniques all written in?
4. **Word-count target check**: Is the word-count target clear?
5. **Narrative point-of-view check**: Is the narrative point of view locked in? (Third-person limited)
6. **Scene breakdown check**: Is the scene breakdown clear? (Each scene carries boundary signals)

---

**[AI]** shows the acceptance report:

```
## Prompt acceptance report: Chapter 1
✅ Passed

| Check Item | Result |
|--------|------|
| 6 modules complete | ✅ |
| Fields fully filled | ✅ |
| writing-style injected | ✅ |
| Word-count target clear | ✅ |
| Narrative point of view locked | ✅ |
```

---

**[Author]** confirms it passed

---
**[AI]** updates `chapters/vol-1-ch-1.md` status → `draft`

---

### 5.4 Main Text Writing

**[AI]** writes the main text following the prompt, into `archives/vol-1-ch-1-灭门之夜.draft.md`

---

### 5.5 Main Text Acceptance

**[AI]** runs the 10-dimension layered check:

---

**L1 Surface Text Check:**

| Check Item | Details |
|--------|----------|
| Tired words | suddenly, abruptly, unexpectedly, silently, gradually, and 6 other major categories |
| Sentence-pattern violations | 8 structural habits, 6 sentence-pattern rules |
| Dialogue rules | Tags / spacing / intent / exclamation marks |

---

**L2 Content Compliance Check:**

| Check Item | Details |
|--------|----------|
| Setting compliance | Worldview / OOC / taboos / continuity |
| Outline fulfillment | required_changes (from innocent youth to traumatized child) |
| Hook fulfillment | Newly planted Qingyun swordsmanship foreshadowing, jade pendant clue, "Junior Brother Chen" |

---

**L3+ Basic Quality Check:**

| Check Item | Details |
|--------|----------|
| Word count | ≥3,200 words (80% of the 4,000 target) |
| Point of view / tense | Third-person limited, past tense |
| Style | Low AI flavor, no tired words, no stacking |
| End-of-chapter pull | Has a hook, leading the reader to the next chapter |

---

**[AI]** shows the acceptance report:

```
## Main text acceptance report: Chapter 1
✅ Passed

L1 Surface text: ✅✅✅
  - Tired words: none
  - Sentence-pattern violations: none
  - Dialogue rules: passed

L2 Content compliance: ✅✅✅
  - Setting compliance: passed
  - Outline fulfillment: passed (required_changes completed)
  - Hook fulfillment: passed (Qingyun swordsmanship / jade pendant / Junior Brother Chen planted)

L3+ Basic quality: ✅✅✅✅
  - Word count: 4,150 words ✓
  - Point of view / tense: passed ✓
  - Style: passed ✓

Word count: 4,150 words
Acceptance conclusion: 10 items passed / 0 items failed
```

---

**[AI]** asks:

> "The main text passed acceptance. **Archive it now, or do an in-depth review first?**"

---

**[Author]** answers:

> "Archive it."

---

### 5.6 Archiving

novel-agent writes archive-order.md and dispatches updater through the Agent tool to perform the archiving.

**updater performs the archiving operations:**

1. Draft → final: `vol-1-ch-1-灭门之夜.draft.md` → `vol-1-ch-1-灭门之夜.md`
2. Update chapter.md status → `archived`
3. Append character state history (Lin Yi):
   - State change: from "9-year-old innocent youth" to "10-year-old silent orphan"
   - Emotion arc: +sadness (intensity: high)
4. Append **possessions** / **experiences** (if any)
5. Update the hooks record:
   - "Qingyun swordsmanship": pending payoff
   - "Jade pendant": pending payoff
   - "Junior Brother Chen": pending payoff
6. Detect the volume boundary: volume 1 has 10 chapters; chapter 1 archived
7. Clean up the order file

---

**[AI]** reports:

```
Chapter 1: Night of the Massacre: archived

Next step: chapter 2 outline
```

---

**[Author]** answers:

> "Start chapter 2."

---

## 6. Continuing with Chapter 2

**State detection:** `vol-1-ch-1` status = `archived`

---

### 6.1 The AI Helps the Author Plan the Chapter Outline

#### 6.1.1 Read the Context

**[AI]** detects that chapter 1 is archived and starts reading the context:

```
✅ Read vol-1-ch-1.md (archived)
✅ Read settings/character-setting/林逸.md (state history: 1 entry)
✅ Read the hooks record (Qingyun swordsmanship / jade pendant / Junior Brother Chen)
✅ Read volumes/volume-1.md (chapters_summary)
```

---

#### 6.1.2 Generate the Character's Voice (Based on State History)

**[AI]** generates the following after reading Lin Yi's state history:

> **[Lin Yi's situation]** 10 years old, a year of wandering, taken in by villagers, working during the day and practicing the breathing method his father taught him at night
>
> **[Lin Yi's unfinished business]** His father's revenge is unavenged; he still does not know who the killer is
>
> **[What Lin Yi wants to do now]** Find out the cause of his father's death and leave the village to seek the truth

---

#### 6.1.3 Hook Inventory

**[AI]** checks the hooks planted in chapter 1:

| Hook | Source | How This Chapter Should Handle It |
|------|------|-----------|
| Qingyun swordsmanship | Chapter 1 | ❌ Not paid off in this chapter (paid off when Chen Feng appears in volume 2) |
| Jade pendant | Chapter 1 | ✅ Paid off in this chapter: the jade pendant glows, revealing a cultivation technique |
| "Junior Brother Chen" | Chapter 1 | ❌ Not paid off in this chapter (paid off when the truth is exposed in volume 4) |

---

#### 6.1.4 Collect the Four Input Groups

**[AI]** synthesizes the direction inputs:

| Input | Content | Source |
|------|------|------|
| Reader gap | The suspense left by chapter 1: who wiped out the Lin family? What is the jade pendant for? | Auto-generated |
| Character state | Lin Yi changed from innocent to silent, with fire inside but not showing it | State history |
| Hook inventory | Jade pendant clue (planted in chapter 1), Qingyun swordsmanship foreshadowing | Hooks record |
| Volume outline position | setup chapter 2, linking past and future, from oppression to kindled hope | volume-1.md |

---

#### 6.1.5 Expand the Outline Points (AI Smart Expansion)

**[AI]** combines the volume outline position + character state + hook direction to generate 7 key points:

| # | Key Point | Function | Hook Link |
|---|--------|------|----------|
| 1 | At the villagers' home, in the morning, Lin Yi finishes the farm work and sits alone in a daze, thinking of his father | [Advance plot · setting] | None |
| 2 | Today is the first anniversary of the massacre; Lin Yi decides to go back to the ruins to look | [Advance plot · turning point] | None |
| 3 | The scene at the ruins: charred walls; Lin Yi digs out the box his father buried | [Build suspense · discovery] | None |
| 4 | Inside the box is the jade pendant; it glows, revealing the Qingyun Sect entry-level mind technique | [Advance plot · climax] | ✅ Jade pendant paid off |
| 5 | The technique is incomplete, only the basic part | [Build suspense · limitation] | None |
| 6 | The jade pendant also holds a divine-sense message; his father's words "My son..." are cut off | [Build suspense · clue] | None |
| 7 | Lin Yi decides to leave the village and go to Qingyun Sect to seek the truth | [Transition · ending] | None |

---

**[AI]** confirms the word-count target:

> Word-count target: 4,000 words

---

#### 6.1.6 Prohibition List

**[AI]** asks:

> "Are there any scenes, elements, or plot points that must definitely not appear in this chapter?"

---

**[Author]** answers:

> "Lin Yi must not suddenly become strong; the technique is incomplete, and there must be no system or cheat power."

---

#### 6.1.7 Memo + Emotion Design (AI-Generated)

**[AI]** fills in (based on character state and story direction):

| Field | Content |
|------|------|
| current_task | One year after the massacre, Lin Yi returns to the ruins, discovers the technique and his father's message inside the jade pendant, and decides to leave the village |
| reader_expectation | Want to know how Lin Yi spent this year, and what the jade pendant is for |
| payoff_plan | The jade pendant is the inheritance his father left him, with technique clues inside; the "Junior Brother Chen" foreshadowing is still pending |
| downtime_functions | Lin Yi's everyday life at the villagers' home, simple but warm |
| key_choices | Lin Yi chooses to leave the village for Qingyun Sect instead of staying somewhere safe |
| knowledge_state | Lin Yi does not know the jade pendant's secret, or who wiped out his family |
| required_changes | From "passively staying alive" to "actively seeking direction", with his resolve for revenge ignited |
| prohibitions | Lin Yi must not suddenly become strong; no system / cheat power |

---

| Field | Content |
|------|------|
| primary_mood | Oppression, hope |
| mood_progression | Oppression (everyday life) → discovering the jade pendant (turning point) → hope ignited (ending) |
| intensity_level | Low → medium |
| intensity_peak | The moment he discovers the jade pendant's secret |
| emotional_hook | His father's message is cut off, leaving suspense |
| micro_payoffs | The villagers' warm care, the glowing jade pendant, his father's message, the resolve to leave |

---

#### 6.1.8 Acceptance

**Step 1: Show the structured feedback**

**[AI]** shows:

```
📋 Chapter 2 outline feedback

This chapter's position: linking past and future, from oppression to kindled hope
Main content:
- Lin Yi's year of wandering life
- Returning to the ruins and discovering the jade pendant
- The technique and his father's message inside the jade pendant
- Deciding to leave for Qingyun Sect

Key scenes:
- Everyday life at the villagers' home (characters: Lin Yi, the villager couple)
- Returning to the ruins (character: Lin Yi)
- Discovering the jade pendant (character: Lin Yi)
- His father's message (character: Lin Yi)

Conflict progress: the jade pendant's secret is revealed; resolve for revenge ignites
Word-count target: 4,000 words
```

---

**Step 2: Self-check list**

**[AI]** checks:

- [x] Word-count target confirmed (4,000+)
- [x] Paragraph distribution confirmed (how many paragraphs advance / transition / plant foreshadowing)
- [x] Each key point maps to a writable scene with a conflict event
- [x] Old hook payoff recorded (jade pendant)
- [x] New hook recorded (carved words on the wall)
- [x] Prohibitions listed (suddenly becoming strong, system)
- [x] The emotion line has three nodes (oppression → turning point → hope)

---

**Step 3: Quick sniff test**

**[AI]** self-checks:

- Can you say how many points there are and what scene each one writes? → ✅
- Can you say what each character knows and does not know? → ✅
- Can you say which old hooks were paid off and which new hooks were planted? → ✅

---

**Step 4: AI-flavor self-check**

**[AI]** checks:

- [x] No omniscient overview ("This chapter tells the story of")
- [x] No abstract psychological summaries ("he felt" / "he realized")
- [x] No analytical conclusions ("this shows" / "this means")
- [x] No literary-commentary tone ("through X, Y is shown")
- [x] No "not X but Y" sentence pattern
- [x] No abstract labels ("relationship progression" / "conflict escalation")

---

**[Author]** explicitly says "yes":

> "Yes, I confirm the chapter outline."

---

#### 6.1.9 Write chapter.md

**[AI]** writes `chapters/vol-1-ch-2.md`, status → `outline`

---

#### 6.1.10 Status Report

> ✅ Chapter outline: `chapters/vol-1-ch-2.md` → `status: outline`
>
> → Dispatch to prompt generation

---

### 6.2 Prompt Generation

**[AI]** generates a 6-module prompt and writes it into `prompts/vol-1-ch-2-prompt.md`:

**Module 1: Basic Positioning**
- Genre: xianxia (immortal cultivation)
- Tone: oppression → hope
- This chapter's position: linking past and future
- Word-count target: 4,000 words
- Payoff beats / emotion: hope ignites

**Module 2: Prior Context**
- Recap: chapter 1's massacre; Lin Yi fled with the jade pendant
- Core scenes: life in the ruins, discovering the jade pendant's secret
- Emotion line: oppression → discovery → hope

**Module 3: Characters' Immediate States**
- Lin Yi (10 years old): silent, alert, with fire inside
- The villager couple: kind, but unaware of Lin Yi's background
- Jade pendant: glowing, hiding an inheritance

**Module 4: This Chapter's Narrative Tasks**
- Scene breakdown:
  1. [Advance plot · setting] At the villagers' home, morning, Lin Yi in a daze
  2. [Advance plot · turning point] Deciding to return to the ruins
  3. [Build suspense · discovery] The ruins scene, digging out the box
  4. [Advance plot · climax] The jade pendant glows, revealing the technique
  5. [Build suspense · clue] The technique is incomplete; his father's message is cut off
  6. [Transition · ending] Deciding to leave for Qingyun Sect

**Module 5: Prose and Detail Requirements**
- Narrative point of view: third-person limited, focused on Lin Yi
- Description requirements: action description first, psychology hinted through expressions
- Prohibitions: suddenly becoming strong, system / cheat power

**Module 6: Human-Touch Supplement**
- Emotions must feel real: Lin Yi is oppressed but does not lose hope
- Half-classical, half-vernacular, xianxia (immortal cultivation) style

---

### 6.3 Prompt Acceptance

**[AI]** checks 6 items:

1. **Module completeness check**: Are all 6 modules present (positioning / context / characters / narrative tasks / prose requirements / human touch)?
2. **Field fill check**: Are every module's fields filled in? Are there any "______" placeholders left?
3. **writing-style injection check**: Are core_principles / possible_mistakes / depiction_techniques all written in?
4. **Word-count target check**: Is the word-count target clear?
5. **Narrative point-of-view check**: Is the narrative point of view locked in? (Third-person limited)
6. **Scene breakdown check**: Is the scene breakdown clear? (Each scene carries boundary signals)

---

**[AI]** shows the acceptance report:

```
## Prompt acceptance report: Chapter 2
✅ Passed

| Check Item | Result |
|--------|------|
| 6 modules complete | ✅ |
| Fields fully filled | ✅ |
| writing-style injected | ✅ |
| Word-count target clear | ✅ |
| Narrative point of view locked | ✅ |
| Scene breakdown clear | ✅ |
```

---

**[Author]** confirms it passed

---

**[AI]** updates `chapters/vol-1-ch-2.md` status → `draft`

---

### 6.4 Main Text Writing

**[AI]** writes the main text following the prompt, into `archives/vol-1-ch-2-废墟余生.draft.md`

---

### 6.5 Main Text Acceptance

**[AI]** runs the 10-dimension layered check:

---

**L1 Surface Text Check:**

| Check Item | Details |
|--------|----------|
| Tired words | suddenly, abruptly, unexpectedly, silently, gradually, and 6 other major categories |
| Sentence-pattern violations | 8 structural habits, 6 sentence-pattern rules |
| Dialogue rules | Tags / spacing / intent / exclamation marks |

---

**L2 Content Compliance Check:**

| Check Item | Details |
|--------|----------|
| Setting compliance | Worldview / OOC / taboos / continuity |
| Outline fulfillment | required_changes (from passively staying alive to actively seeking direction) |
| Hook fulfillment | Jade pendant advanced, carved words on the wall newly planted |

---

**L3+ Basic Quality Check:**

| Check Item | Details |
|--------|----------|
| Word count | ≥3,200 words (80% of the 4,000 target) |
| Point of view / tense | Third-person limited, past tense |
| Style | Low AI flavor, no tired words, no stacking |
| End-of-chapter pull | Has a hook, leading the reader to the next chapter |

---

**[AI]** shows the acceptance report:

```
## Main text acceptance report: Chapter 2
✅ Passed

L1 Surface text: ✅✅✅
  - Tired words: none
  - Sentence-pattern violations: none
  - Dialogue rules: passed

L2 Content compliance: ✅✅✅
  - Setting compliance: passed
  - Outline fulfillment: passed (required_changes completed)
  - Hook fulfillment: passed (jade pendant advanced / carved words on the wall newly planted)

L3+ Basic quality: ✅✅✅✅
  - Word count: 3,980 words ✓
  - Point of view / tense: passed ✓
  - Style: passed ✓

Word count: 3,980 words
Acceptance conclusion: 10 items passed / 0 items failed
```

---

**[AI]** asks:

> "The main text passed acceptance. **Archive it now, or do an in-depth review first?**"

---

**[Author]** answers:

> "Archive it."

---

### 6.6 Archiving

**[AI]** performs the archiving operations:

1. Draft → final: `vol-1-ch-2-废墟余生.draft.md` → `vol-1-ch-2-废墟余生.md`
2. Update chapter.md status → `archived`
3. Append character state history (Lin Yi):
   - State change: from "10-year-old silent orphan" to "10-year-old resolved on revenge"
   - Emotion arc: +hope (intensity: medium)
4. Update the hooks record:
   - "Qingyun swordsmanship": pending payoff (when Chen Feng appears in volume 2)
   - "Jade pendant": closed (technique appeared, inheritance begun)
   - "Junior Brother Chen": pending payoff (when the truth is exposed in volume 4)
   - "Carved words on the wall": newly planted, pending payoff
5. Detect the volume boundary: volume 1 has 10 chapters; chapter 2 archived

---

**[AI]** reports:

```
Chapter 2: Life Among the Ruins: archived

Character state updates:
- Lin Yi: 10-year-old silent orphan → 10-year-old resolved on revenge
- Emotion arc: +hope (intensity: medium)

Next step: chapter 3 outline
```

---

**[Author]** answers:

> "Continue with chapter 3."

---

### 6.7 The Core Value of AI-Assisted Outline Planning

| Scenario | What the AI Does Automatically | What the Author Does |
|------|-------------|-----------|
| Reading context | Detects archived chapters, reads state history, hooks records, and volume outlines | None |
| Direction input | Generates the character's voice based on state history | Confirm / adjust |
| Hook inventory | Checks the hooks planted in the previous chapter, marking which to pay off and which to keep | Confirm the direction is right |
| Expanding outline points | Smartly expands 7 key points combining position + state + hooks | Confirm the scene choices |
| Prohibition list | Asks about this chapter's taboos | Gives clear requirements |
| Memo filling | Auto-generates based on character state and story direction | Confirm / add to |
| Emotion design | Auto-generates based on the character's emotion arc | Confirm / adjust |
| Archiving | Appends state history, updates the hooks record | Confirm archiving |

## 7. Frequently Asked Questions

### Q1: How do I pause / resume writing?

**Pause**: just say "That is enough for today".

**Resume**: next time, type `@novel-agent` or say "Continue writing the novel".

---

### Q2: I found a problem in an earlier chapter?

Type "Revise chapter X" and the AI will handle it.

---

### Q3: I want to add a new character?

Type "Add a new character" and tell the AI the character's setup.

---

### Q4: The prompt failed acceptance?

The AI will point out the specific problems; fix them and re-run acceptance.

---

### Q5: The main text has too much AI flavor?

Main-text acceptance checks tired words and sentence-pattern violations, and failing items are flagged.

---

### Q6: What is SOLO mode?

Say "You write everything", "solo", or "standalone", and the AI enters SOLO mode, writing without stopping to wait for confirmation.

---

## Appendix: Acceptance Methods Overview

| Output | Acceptance Method | What Is Checked |
|------|----------|--------------|
| Worldview | Self-check | Geography completeness, politics plausibility, rules executability, conflict space |
| Characters | Self-check | Six-layer cognition completeness, motivation clarity, weakness presence, ability boundary clarity |
| Main arc breakdown | Three-way cross-check | Overall main arc → per-volume, volume sequence complete path, reverse inference of the overall main arc |
| Volume outline | 4 checks | Completeness, traceability, progress, title match |
| Chapter outline | 4-step acceptance | Structured feedback, self-check list, quick sniff test, AI-flavor self-check |
| Prompt | 6 checks | Module completeness, field filling, style injection, word count, point of view, scene breakdown |
| Main text | 10-dimension check | Tired words, sentence patterns, dialogue, setting compliance, outline fulfillment, hook fulfillment, word count, style, and more |

---

## Appendix: File Structure Example

```
青云志/
├── story.md              # Project index
├── settings/
│   ├── world-setting.md  # Worldview settings
│   ├── writing-style.md  # Writing style
│   ├── genre-setting.md  # Genre settings
│   └── character-setting/
│       ├── 林逸.md       # Protagonist
│       ├── 陈风.md       # Villain
│       ├── 苏晴.md       # Heroine
│       └── 云霄子.md     # Mentor
├── volumes/
│   └── volume-1.md      # Volume 1 outline
├── chapters/
│   ├── vol-1-ch-1.md    # Chapter 1 outline (archived)
│   └── vol-1-ch-2.md    # Chapter 2 outline
├── prompts/
│   ├── vol-1-ch-1-prompt.md   # Chapter 1 prompt
│   └── vol-1-ch-2-prompt.md   # Chapter 2 prompt
└── archives/
    ├── vol-1-ch-1-灭门之夜.md       # Chapter 1 final draft
    └── vol-1-ch-2-废墟余生.draft.md # Chapter 2 draft
```

---

**Manual version:** v4.12.0
**Applies to:** awesome-novel-agent v4.12.0+
