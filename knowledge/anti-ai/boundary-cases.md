# Manslaughter Protection - No changes to the list

> When the anti-ai pipeline is executed, the following scenarios **skip detection**.
> Prevent excessive AI deodorization from leading to role homogeneity.

## 1. Role-based expression remains unchanged

### catchphrase/mantra

- The characters’ fixed mantras, modalities, and pause habits remain unchanged.
- Example: Character A likes to say "just say" when speaking, character B likes to say
  "you know" when speaking, character C will stutter when nervous.
- Regardless of whether the forbidden word list is hit or not, **character mantras do
  not trigger Gate A/B/C**

### Personalized grammar errors

- Grammatical errors caused by the character's cultural level/personality will not be
  corrected.
- Example: The illiterate character says "I don't know", the carefree character says
  "I'm not talking about you"
- Judgment criteria: Whether the error fits Layer 6 (originality) + Layer 2
  (self-positioning) in the character setting

### Specific Narrative Tone

- The first-person complaining style remains unchanged (psychological activities include
  a lot of colloquial/extreme/inaccurate expressions)
- The character’s abnormal expressions when facing extreme emotions remain unchanged
  (laughing when angry, silent when sad, talking too much when anxious)
- The special sentence patterns brought about by the narrator's age/temperament remain
  unchanged (children's perspective/old man's memories/veteran's oral narration)

## 2. Dialogue exceptions remain unchanged

### Complete sentence exemption

- The written language/complete sentences that appear in the dialogue are intentional
  changes to the character's personality.
- Example: The scholar character also uses complete sentences in the dialogue - this is
  not an AI flavor, but a character setting.
- Judgment criteria: Compare character setting layer 5 (skills) and basic information
  and language characteristics

### Conversational mood word exemption

- Do not change the emotional words that appear directly in the conversation - people
  will say "I am angry" or "I am sad" in the conversation.
- Change to mark "emotional words in dialogue", which is only used for quantitative
  statistics and **does not trigger replacement**

### Conversation tag exemption

- Basic dialogue tags such as "He Said" and "She Asked" remain unchanged because they
  are narrative infrastructure.
- Only handle **overmodified** tags (the adverbial parts of "he said angrily" and "she
  whispered")

## 3. Specific narrative functions remain unchanged

### Punctuation function exemption

| Scenario | Example | Processing |
|------|------|------|
| The conversation was interrupted | "You, " He was interrupted before he could finish his sentence | Keep the dash |
| The character's voice is elongated | "Wait - one - next -" | Reserved |
| Omission of inner activities | "She remembered... no, maybe she remembered it wrongly" | Keep the ellipses |
| List of commas | "There are pens, paper, mobile phones, and keys on the table" | Reserved (enumerated in daily life) |
| List of comma (AI template) | "This symbolizes courage, tenacity, hope, and future" | Tag (list of abstract concepts) |

### Function exemption of the word "了"

| Scene | Do not change | Change |
|------|------|----|
| Dialogue perfect state | "I understand" "Okay" "Let's go" | No change (spoken perfect state) |
| Action completed | "He stood up" | Can be changed → "He stood up" |
| Continuous perfect tense | "He stood up, walked out, and closed the door" | Keep one "了" |
| Status change | "He begins to understand" | Do not change (idiom) |

### Parallel sentence function exemption

| Scene | Do not change | Change |
|------|------|----|
| Roles are deliberately matched | Characters have speech/debate/sensational needs | Reserved, automatic replacement will not be triggered |
| Stream of consciousness | Characters use parallelism to enhance tone at emotional high points | Reserved, marked only |
| AI template ranking | "Maybe...maybe...maybe..." | Change |
| Mechanical enumeration | "First...Secondly...Last" | Change |

## 4. Gate G / Style deviation exemption

| Category | Description |
|------|------|
| Deliberate deviations in scene types | Short sentences are used in battle scenes, long dialogues/low dialogue proportions are deliberately used in dialogue scenes - if it is consistent with the override of the scene marked on the scene card, it is not a deviation |
| Character's oral habits | Repeated words/sentence patterns in character (already exempted in the previous group) |
| Uncertain | The judgment result is uncertain (suspected of manslaughter, no current gear can be applied - currently T1/T2/T3 gear + light/medium/heavy grade + Gate G PASS/FAIL) → mark `[疑: 疑似误杀]` and do not change, report to the author for confirmation |

## 5. Practical Guide to Writing

### anti-ai Agent Execution Rules

```
Check if hit → is in boundary-cases list? → Yes → Skip (mark SKIP)
                                           → No → Processed by common-rules
```

- Before each Phase 3 execution, read boundary-cases.md first
- For each Gate hit, first make a judgment on whether to save or not, and then decide
  whether to change it or not.
- Hit statistics marked as SKIP are included in quantitative indicators** but are not
  modified**

### Uncertain

- Ambiguous hits → keep original text, mark `[疑: 疑似误杀]` in Phase 4 report
- Those that require the author’s judgment → enter them in the report without
  modification.
