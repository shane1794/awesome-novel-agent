# Psychological activities/inner monologue

> Core principles: **Psychology is mainly presented with physiological reactions,
> thought fragments, and cognitive collapse, supplemented by emotional words.
> **Priority is given to using physical reactions (chills running through the body,
> trembling fingertips, clenched teeth) instead of emotional nouns, but it is allowed
> to use 1-2 emotional words at key emotional nodes to assist readers in understanding
> ("A trace of fear flashed in his heart"), and do not rely on emotional words for
> expression throughout the text. Each technique begins with `[tag]`.

## Injection timing

Psychological description is not a scene type and cannot be automatically detected by
the input scene raw material scene type. prompt-crafter additionally loads this file to
inject output and writing specs when any of the following conditions are met:

| Trigger conditions | Judgment basis | Example |
|---------|---------|------|
| **The character encounters a major event** | L3 core suspense/turning involves the character receiving shocking information | Learning that a loved one has been murdered, discovering that he has been betrayed, and the truth being revealed |
| **Character emotions fluctuate violently** | Input / scene raw materials Scene emotions are strong emotions such as fear/anger/collapse/ecstasy | Confrontation breaks out, life and death, reunion after a long separation |
| **The character faces a major choice** | This chapter involves the character making key decisions (key_choices) | Choosing a camp, who to sacrifice, whether to take a gamble |
| **face-slapping/reversal scene** | The opponent's progressive process from disbelief to collapse | The villain is crushed and the conspiracy is exposed |
| **Inner conflict of the character** | Conflict between what the character wants to do and what he should do | Want to save but cannot save, want to love but cannot love |

### Loading method

Not in the regular scene type loading process. After the input scene raw material scene
sequence is filled in, **extra check** whether the core events + emotional design + key
decisions of each scene trigger the above conditions. If triggered, load
`inner-mono/universal.md` + `inner-mono/{genre}.md` (if it exists), and append to output
and writing specs after four steps of conversion.

## Label Selection Guide

| Scene characteristics | Matching tags | Reason for selection |
|---------|---------|---------|
| The character feels fear, tension, and anxiety | [Physiology] | Replace "fear" with physical reactions such as chills running through the body, ringing in the ears, and trembling fingertips |
| The character is angry, depressed, and tolerant | [Physiology] | Replace "anger" with twitching temples, clenched teeth, and heavy breathing |
| The character's heartbeat, embarrassment, and nervousness | [Physiological] | Replace "heartbeat" with tightness in the chest, hot ears, and stiff limbs |
| The character encounters great tragedy, collapse, and ecstasy | [Fragment] | Thoughts are illogical, and the contrast between behavior and emotion is inconsistent |
| The character witnesses a fact that subverts his cognition | [Collapse] | Three stages of progression: arrogance and questioning → self-deception → complete collapse |
| face-slapping/reversal scenes need to be amplified | [Collapse] | Let readers see the whole process of the villain from disbelief to collapse |


## [Physiology] Physiological synaesthesia - mapping emotions through body reactions

**Core:** It does not label emotional words directly, but indirectly reflects the inner
state through the human body's senses, limbs, and body instinctive reactions.

### Emotion → Physiological Response Mapping Table

| Emotions | Physiological signals |
|------|---------|
| **Fear** | Chills traveling through the body, tinnitus, dry mouth, trembling fingertips, hearing loss, and tight throat |
| **Angry** | The temples are pounding, the jaws are tense and sore, the nails are digging into the flesh, the breathing is heavy, and the blood is rushing to the top of the head |
| **Heartbeat/constriction** | Chest tightness, shortness of breath, hot ears, stiff limbs, sweaty palms |
| **Suppression/Forbearance** | Clenched fingers, rolled Adam's apple, clenched teeth, paused in silence, and had a tight breath in the chest |

```
❌ After learning the truth, he was filled with fear and panic.

✅ A chill shot straight to the top of my head, my ears were ringing, and all the surrounding sounds were gone.
   He wanted to swallow, but his throat was so dry that it smoked, and his fingertips trembled uncontrollably.
```

**Controlled usage:** Prioritize using physiological reactions instead of direct
emotional adjectives ("fear" → "fingertips shaking"). It is allowed to use 1-2 emotional
words at key emotional nodes to assist readers in understanding, but do not rely on
emotional words for the entire text.


## [Fragmentation] Thought fragmentation method - fragmented thoughts under extreme emotions

**Core:** When people fall into strong emotions such as great sadness, ecstasy, and
collapse, their thinking loses logic, the word order is messy, and their thoughts jump
and fragment. Use confusing self-talk and contradictory behaviors to enhance emotional
tension.

### Implementation details

- Contrast between behavior and emotion: calm on the surface but out of control in
  actions
- Thoughts jump around without logic, interspersed with irrelevant daily thoughts
- The movements gradually lose control, and the details reveal the true state of mind.

```
❌ Looking at the fallen man, he shouted in grief and couldn't stop his tears from flowing.

✅ He looked calm, raised his hand and kept stuffing pills into the other person's mouth, muttering to himself:
   "It's just an ordinary fireball technique. After taking the medicine, we will go to the temple fair tomorrow...
   The clothes are dirty. I'll wash them for you later. "
   The movements became more and more rapid, and the elixir mixed with black blood spilled all over the floor.
```

**Disabled:** When emotional, the logic is still clear and the speech is regular; cry
outright and shout to vent.


## [Collapse] Progressive psychological collapse - layered description of cognitive dissonance

**Core:** When a character encounters a reality that subverts his cognition, his
psychology slides down layer by layer in three stages, gradually amplifying the sense of
pleasure/shock.

### Three stages of progression

| Stage | Mental state | Performance |
|------|---------|------|
| **Phase 1** | Contempt, ridicule | Believe that the other party is playing tricks, having an accident, and it cannot be true |
| **Stage 2** | Self-deception | The facts are in front of you, and you forcefully make excuses and refuse to accept them |
| **The third stage** | Complete collapse | Disillusionment, complete collapse of self-esteem and cognition, accompanied by physical loss of posture |

```
❌ The senior brother was shocked and thought: This is impossible, how could he be so strong?

✅ He had a sneer on his lips, thinking that the other party was being mysterious and tampering.
   Coercion swept over him, his smile suddenly froze, and cold sweat covered his forehead.
   I kept arguing in my heart: He must have used witchcraft and he couldn't last long.
   The moment the spirit stone exploded, the debris scratched his cheek.
   He backed away continuously, the luster in his eyes lost all - the talent he was so proud of was now reduced to a joke.
```

**Disabled:** The psychological description is written in one stroke, with only a single
"I can't believe it"; there is no hierarchy or transition and it is written directly to
collapse.
