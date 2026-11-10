# short-scan skill: Short-Story Chart Scan (standalone tool)

> Not part of the short-agent dispatch chain: the entry point goes straight here when the author says "scan the charts / see what is hot / short-story market".
> Serves short-story topic decisions for platforms such as Zhihu Yanxuan, Fanqie Short Stories, Qimao, Heiyan, and Dianzhong.

## Core Philosophy

1. **The short-story market is an emotion market**: extract high-frequency emotions, trigger scenes, emotional eruption points, and the points readers want to forward, not just genre names.
2. **A short story's life is in its spread**: a high completion rate means the emotional pull is in place; a high share rate means there is resonance or a reversal people want to forward.
3. **Trends come and go fast**: a genre signal may expire within weeks; before a rescan, it MUST NOT be treated as a long-term trend.

## Phase 1: Confirm the Platform and Direction

Ask the author: "Which platform do you want to look at? (Zhihu Yanxuan / Fanqie Short Stories / Qimao / Heiyan / Dianzhong / other) Is there a type direction you want to write?"

- Has a direction → deep scan in that direction
- No direction → overview of the whole chart to find trends
- Wants a cross-platform comparison → platform comparison analysis

## Phase 2: Data Sources (three levels of fallback)

| Priority | Mode | When to use |
|--------|------|--------|
| 1 | **Real-time collection in the runtime** | When the current agent has a browser / web scraping tool, collect the chart pages using the field list in Appendix A |
| 2 | **Author-provided** | The author pastes chart screenshots / text / links (links use the runtime's built-in web reading ability) |
| 3 | **Built-in knowledge** | When neither of the first two levels is available, analyze using the historical trends in Appendix A |

Hard rules:

- When falling back to built-in knowledge, the report MUST be labeled "Based on historical trends, not verified in real time; usable only as a candidate hypothesis", and list the platform pages that need a rescan
- If a single platform's collection fails, mark it skipped and continue with the remaining platforms; the report labels that platform's data gap, and MUST NOT interrupt this round

## Phase 3: Seven-Dimension Analysis

For each platform, extract (each item needs a concrete finding; MUST NOT just list genre names):

1. **Emotion type distribution**: which kind of emotional pull is hottest right now (tormented love / reversal / suspense / healing / face-slapping)
2. **Genre hotspots**: settings / scenes that keep recurring
3. **Length distribution**: the word-count range where popular short stories cluster
4. **Opening patterns**: how the first paragraph / first sentence is written
5. **Ending types**: HE / BE / open-ending proportions
6. **Title patterns**: naming conventions
7. **Character models**: high-frequency protagonist types

See Appendix A.1 for the platform tone matching reference (judging whether a candidate direction holds on that platform).

## Phase 4: Output the Chart Scan Report

```
# Short-Story Chart Scan Report: {Platform}

## Market Overview
- Scan time: {date}    Sample credibility: High (real-time) / Medium (author-provided) / Low (built-in knowledge)
- Next rescan: {date or event}
- Core finding: {one sentence}

## Emotion Heat Ranking
| Rank | Emotion Type | Count on Chart | Trend | Representative Work |

## Genre Hotspots
| Genre | Heat | Competition | Barrier | Representative Work |

## Key Data Insights
(Length range / opening patterns / ending proportions / title features / character hot words)

## Trend Warnings
- 🔥 Breaking out now: {genre}: {basis}
- ⚡ About to take off: {genre}: {basis}
- ⚠️ About to saturate: {genre}: {basis}

## Directions Worth Writing
1. {direction + how the emotion pulls + feasibility}

## One Sentence
{Sharp summary}
```

The report language uses the author's language, and MUST NOT contain internal terms.

## Phase 5: Topic Matching

- **Low-complexity candidates**: reversal and face-slapping types (clear structure, low verification cost)
- **High-complexity candidates**: suspense and tormented love types (need foreshadowing, reversal, and emotion control skill)
- **Priority candidates**: the intersection of a strong current signal and what the author's ability can support

Judgment basis:

- Emotional pull > genre innovation (short-story readers care more about the emotional experience)
- The opening 3 sentences are a high-risk retention zone; they must have conflict, an identity gap, or an emotional hook
- **Spread risk fallback**: when a recommended direction contains no reversal, it MUST state that it is compensated by strong resonance / a strong topic / strong lingering resonance; without that statement it cannot stand as a recommended direction

## Appendix A: Built-In Market Knowledge (historical trends; use MUST carry the unverified label)

### A.1 Platform Tone Reference

| Platform | Tone | Core Metric | Main Readers | Suitable Types | Main Short-Story Word Count |
|------|------|----------|----------|-------------|-------------|
| Zhihu Yanxuan Stories | Quality short stories, emotional depth | Paid conversion, favorites | Urban readers aged 20-35 | Tormented love, reversal, suspense, realistic | 5,000-15,000 words |
| Qimao Short Stories | Down-market, mostly female readership | Completion rate | Mostly women (80%+) | CEO / realistic / household intrigue / period / suspense | 10,000-20,000 words (7-19 chapters) |
| Heiyan Short Stories | Extreme emotion, fast pace | Completion rate, paid | Mixed | Tormented love, revenge, identity reversal | 8,000-40,000 words |
| Dianzhong Short Stories | Quality, fast pace | Completion rate | Mixed | Family revenge, fake heiress, bullet-comment stream | 10,000-20,000 words (5-10 chapters) |
| Fanqie Short Stories | Smooth, fast pace | Completion rate | Down-market mixed | Straightforward golden finger, grand-slam ending | 8,000-20,000 words |

### A.2 Platform Opening Formula Quick Reference

- Zhihu Yanxuan: first person + an everyday-life sense of wrongness to enter ("there is a red hair on my husband's passenger seat", 老公副驾驶有根红头发) + peeling-the-onion chilling realization
- Mini-programs (Heiyan / Dianzhong): hell from the opening + public face-slapping + cliffhanger breakpoint
- Fanqie Short Stories: straightforward golden finger + smooth with no poison points + grand-slam ending

### A.3 Genre Hit Formula Quick Reference (historical samples)

| Genre | Hit Elements | Commonly Paired Emotion |
|------|----------|----------|
| Wife-chasing crematorium (追妻火葬场) | First-love trigger + plea-for-help turned humiliation + crematorium preview | Bittersweet regret (意难平) |
| Fake heiress (假千金) | Identity mismatch + public flip + numbers carrying weight | Satisfying release |
| Folk horror tales (民俗怪谈) | Rules + breaking the rules + the consequence confirmed | Chilling realization |
| Revenge rebirth (复仇重生) | Slow-motion humiliation + hole card held back + public execution | Satisfying release |
| Sweet romance mix-up (甜宠错位) | High-concept misunderstanding + forced sharing of scenes + everyday sweet moments | Healing |

> The above are candidate hypotheses for writing calibration; before any topic decision, MUST complete one real-time rescan or obtain the current data provided by the author.
