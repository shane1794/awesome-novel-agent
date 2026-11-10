# short-plan SOP: Set the Emotion and Lay Out the Outline

> Executed by short-planner. Covers two phases: setup (set the emotion and the direction, producing setting.md) and planning (conceive and lay out the outline, producing outline.md).

## Phase setup: Set the Emotion and the Direction

1. **Set the emotion first**: If the author has a clear idea, adopt it directly. If it is vague, offer a choice of six (bittersweet regret / shocking reversal / satisfying release / healing warmth / chilling realization / resonant emotion), each with suitable scenes, difficulty, and commonly paired genres
2. **Set the genre direction**: Recommend genres based on the emotion, then load `.claude/knowledge/short-genres/{genre}.md`
3. **Set the submission platform tone**: Zhihu Yanxuan (first-person immersion, chilling realization, a detail at the end of each chapter that overturns what the reader thought, lots of blank space) / mini-program (hell from the opening, public face-slapping, a cliffhanger breakpoint, blunt satisfaction) / Fanqie short stories (smooth, a straightforward golden finger, a grand-slam ending)
4. **Produce `stories/{slug}/setting.md`**, which must contain:
   - Basic info: provisional title / target word count (8000-20000) / target platform / emotional goal
   - One-sentence hook: protagonist + predicament + reversal + emotional landing
   - Core reversal: type / content / at least 3 planted clues
   - Four-part emotional design: opening / middle / reversal / ending, each with an intensity of 1-10; mark that the reversal climax does not drop sharply (the section before the reversal warms up, the reversal section peaks, the section after the reversal holds)
   - Character sketches: protagonist / key characters / relationships
   - **Naming record**: All character names are written down (checked against the banned list in Section 9 of `.claude/knowledge/short-anti-ai.md`); later revisions use this as the standard

## Phase planning: Conceive and Lay Out the Outline

Execute in order; an item that does not apply may be skipped after noting the reason:

1. **Pick the emotional chain**: Pick one chain (4-6 stages) from the genre pack's "emotional chain library" as the skeleton of the whole story; the number of stages is not forced to equal the five parts
2. **Pick techniques**: Pick 2-3 core techniques from the genre pack's technique library (each is a formula plus an example, and must be converted when used)
3. **Design the villain** (if any): identity + motive + ladder of wrongdoing (moral, then economic, then life-threatening) + fatal weakness + retribution
4. **Decide the reveal method**: physical evidence / witness / eavesdropping / peeling the onion, pick one (for the mechanism details see `.claude/knowledge/short-craft/villain-and-reveal.md`; for reversal types and planting techniques see `.claude/knowledge/short-craft/reversal-toolkit.md`; for how to lay bonds and lingering resonance see `.claude/knowledge/short-craft/emotional-methods.md`; for lead and paywall point details see `.claude/knowledge/short-craft/submission-craft.md`; for unregistered niche genres outside the registry, use the structural skeleton in `.claude/knowledge/short-craft/genre-writing-formulas.md` as the fallback)
5. **Write `outline.md`**:
   - **One line per section**, with fields: `structural part / five-part function | main event | sub-events x3-5 (connected with ->, each with a function tag: dialogue/conflict/foreshadowing/flashback/discovery/escalation, described concretely as who did what) | emotion | character/relationship change | causal chain | what the reader newly learns | ending carryover/hook | foreshadowing/object | movement/stillness | dialogue density | target word count`
   - **Fixed causal chain shape**: `carryover point → motive and action → core event → direct consequence → ending hook`; the carryover point states what is inherited, the direct consequence states what it causes, and the connecting slots MUST NOT be omitted
   - **Emotional chain landing points**: chain name + the section numbers each stage covers (every section in the whole story is covered, with no section outside the chain)
   - **Technique landing table**: for each technique, mark its carrying section and its payoff section, leaving planting distance in between; carrying and payoff in the same section is forbidden
   - **No functionless sections**: every section carries at least one of advancing a technique / raising pressure / planting foreshadowing / changing a relationship / paying off an emotion / developing a supporting-character subplot; a supporting-character subplot must have a memorable point and act on the main line; a pure transition section is merged or given a function
   - **Villain wrongdoing is preceded by planting**: before each act of wrongdoing there is planting that accumulates danger
   - **Catalytic anomaly**: at the 60-75% point of the whole text, place one contradiction that the current explanatory framework cannot explain (for genres where a reversal cannot hold, such as pure sweet romance, mark it not applicable)
6. **Two verifications**:
   - **Reversal position**: reveal section number divided by total section count. Below 50%, go back and adjust the outline; 50-60% is a gray zone, re-check the misleading clues; above 60% passes. Also requires at least 1 successful misleading false clue
   - **Foreshadowing back-check**: every key element in the ending has at least 1 earlier planting; the throughline prop appears three times (harmless, then attention-grabbing, then truth-revealing), all present; the gap between a planting section and its reveal section is at least 3 sections

## Acceptance

- [ ] setting.md has all seven parts, naming record written down
- [ ] outline.md has all fields for every section, causal chains in the complete five-part shape
- [ ] Emotional chain landing points / technique landing table complete, no functionless sections
- [ ] Both verifications leave a trace (percentage, back-check list)
- [ ] The summary for the author uses everyday language, with no internal field names
