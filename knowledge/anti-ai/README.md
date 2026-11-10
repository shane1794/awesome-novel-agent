# Anti-AI Writing Rule Library

> Anti-ai pipeline core reference. It includes the positive method of living human
> beings, hierarchical prohibition table, AI removal methodology, and positive and
> negative examples of themes.

## Directory

| Documentation | Purpose |
|------|------|
| `living-voice.md` | Positive methodology of human feeling (three levels of human feeling/character and scene crafts/anti-performance, transplanted from human-writing, common to all themes) |
| `common-rules.md` | Graded banned word list, sentence templates, replacement strategies (common to all themes) |
| `anti-ai-writing.md` | A complete guide to removing the AI flavor (fingerprinting/systematic modification/example library) |
| `urban.md` | Urban general |
| `urban-romance.md` | Urban Romance |
| `urban-daily.md` | Urban Daily |
| `urban-farming.md` | Urban Farming |
| `urban-brained.md` | Urban wild idea/gaowu/cultivation |
| `war-god.md` | The God of War live-in son-in-law |
| `xianxia.md` | oriental xianxia (immortal cultivation) |
| `xuanhuan.md` | xuanhuan (Eastern fantasy) |
| `suspense-crime.md` | Suspense criminal investigation |
| `suspense-paranormal.md` | Suspense and Supernatural |
| `historical.md` | History and Antiquity |
| `ancient-politics.md` | Historical politics/ancient style tactics |
| `western-fantasy.md` | Western Fantasy |
| `scifi-apocalypse.md` | Science fiction apocalypse |
| `anti-japanese-war.md` | Anti-war spy war |
| `anime-derivative.md` | Animation/game derivatives |
| `derivative.md` | male-oriented derivative |
| `fanqie.md` | Fanqie wind |

## Usage scenarios

```
When anti-ai agent is executed to remove AI flavor:
    ↓
Read living-voice.md (positive methodology of living voice: first let’s talk about how to write it)
    ↓
Read common-rules.md (hierarchical ban table)
    ↓
Read anti-ai-writing.md (methodology guide)
    ↓
Read {genre}.md (positive and negative examples of the theme)
    ↓
Perform replacement by Phase 1-4 pipeline
```

### anti-ai Phase 3
Check the corresponding positive and negative examples according to the topic and make
accurate replacements

### prompt-crafter
Inject theme rules on demand when generating prompt words

## Format

### common-rules.md, Common rules

Common to all themes. Contains:
- **Graded banned word list**, ★★★★★ The most poisonous sentence patterns / Level 1 /
  Level 2
- **Sentence Template**, Metaphor/Structure/Punctuation Rules
- **Quick Replacement Strategy**, Emotional Externalization/Dialogue Tags/Perspective
  Control
- **Fatigue Word Threshold**, Original Threshold Quick Look

### anti-ai-writing.md, Methodology Guide

The methodological basis of each phase of anti-ai. Contains:
- **AI writing fingerprint**, high-frequency words/end-of-chapter summary/superimposed
  description/even distribution
- **Show Don't Tell**, Core Formula + Five Senses Check
- **7 AI Writing Pattern Detections**, Signals/Characteristics/Fixes for Each
- **Systematic AI three-pass method**, De-generalize/de-literate/return to a sense of
  nature
- **Rewrite Example Library**, Emotional Externalization/Scene/Fight/Ending/Rhythm

### {genre}.md, Positive and Negative Examples of the Theme

Each theme is a separate file. Contains:
- **Incorrect vs. correct examples of high-frequency AI-style bad sentences**, ❌ AI flavor vs. ✅ human voice
  feeling comparison
- **Writing Points**, Special considerations for this subject matter

## Format specifications

All theme files follow a unified format:

```markdown
# {Subject Name} Anti-AI Rules

> Applicable themes: {genre-id-1}, {genre-id-2}

## High-Frequency AI-Style Bad Sentences: Incorrect vs. Correct Examples

### 1. {Question Type}

❌ "AI flavor writing"
✅ "Realistic writing style"

### 2. {Question Type}

...

## Writing points

1. **{Point Title}**, Specific instructions
2. ...
```

## How to contribute new topics

### Method 1: Create a new theme file

1. Create new `{genre-id}.md` under `knowledge/anti-ai/`
2. Copy the following template and fill it out:

```markdown
# {Subject Name} Anti-AI Rules

> Applicable themes: {genre-id}

## High-Frequency AI-Style Bad Sentences: Incorrect vs. Correct Examples

### 1. {Question Type}

❌ "AI flavor writing"
✅ "Realistic writing style"

### 2. {Question Type}

❌ "..."
✅ "..."

## Writing points

1. **{Key Points}**, Description
2. **{Key Points}**, Description
```

### Method 2: Expand existing themes

When the writing points in existing documents are not enough:
1. Find the corresponding file
2. Add new question types under "High Frequency AI Ill Sentences Positive and Negative
   Examples"
3. Each question type contains a pair of ❌/✅ controls

## Contribution Guide

### Principle of Positive and Negative Examples

1. **❌ Be specific**, Give real AI-flavored sentences, not abstract descriptions
2. **✅ It needs to be executable**, Give a replicable real-life writing method, not "be
   natural"
3. **Contrast should be obvious**, same scene, same emotion, ❌→✅ clear transformation

### Writing Points and Principles

1. **Concrete, not abstract**, "Writing about shaking hands" is not "writing about
   nervousness"
2. **Executable**, "Shaking hands = unable to hold the cup" is not "must have details"
3. **Theme Features**, The key points of each theme should reflect the particularity of
   the theme

### Self-check before submission

- [ ] Is ❌ of each positive and negative example a real AI-flavored sentence?
- [ ] Can the ✅ of each positive and negative example be copied directly into the text?
- [ ] Do the writing points address specific issues in the subject matter?
- [ ] Have you avoided duplicate content already in other files?

## Example

Suppose you want to add a new file for the "Game Sports" theme:

```markdown
# Game Sports Anti-AI Rules

> Applicable themes: game-sports

## High-Frequency AI-Style Bad Sentences: Incorrect vs. Correct Examples

### 1. Description of game victory

❌ "He won the game and the audience cheered"
✅ "The final whistle sounded. He froze in place, and his teammates rushed over to pick him up. His legs were weak and he could not stand firmly."

### 2. Parallel psychology

❌ "Maybe the pressure is too much, maybe the opponent is too strong, maybe I am not ready yet"
✅ "He took a deep breath. The referee looked down at his watch. He moved his ankle and the shoelaces were a little loose."

## Writing points

1. **Write about the body during the competition**, Panting, shaking, weak legs, and thirst are not "nervous"
2. **Training Write and Repeat**, What do you practice every day? How many times did you make a mistake? Which bottle of water?
3. **Writing Contrast in Victory**, What do you do after you win? Not cheering, but stunned, weak legs, looking for water
```

---

*If you have any questions or suggestions, please submit an Issue or PR. *
