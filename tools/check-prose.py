#!/usr/bin/env python3
"""Check a finished Chinese manuscript for AI-flavor hard bans and statistical patterns. Reports only; never edits the text automatically.

Ported from the human-writing skill's scripts/check_prose.py
（MIT License, Copyright (c) 2026 Human Writing Skill contributors），
Adjusted to this project's knowledge/anti-ai/common-rules.md:
- Colons are not checked (web novels have no such ban);
- Dashes are not hard-banned; when a paragraph has 3 or more, prompt a case-by-case usage check (common-rules.md dash rule);
- Paragraphs are split by line (in web-novel chapters each paragraph is one line; blank lines are only separators).

Usage: python3 tools/check-prose.py <manuscript path|->    (- reads from standard input)
Exit codes: 0 = no failures (reviewable warnings may remain); 1 = failures found; 2 = read failure
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from dataclasses import dataclass
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")


HARD_STOPS = (
    "说白了",
    "说穿了",
    "先说结论",
)

HARD_JARGON = (
    "赋能",
    "抓手",
    "商业闭环",
    "价值闭环",
    "能力沉淀",
    "拉通",
    "底层逻辑",
    "顶层设计",
    "认知跃迁",
    "价值释放",
    "能力建设",
    "降本增效",
    "内容矩阵",
    "全链路",
    "组合拳",
    "打开想象空间",
    "结构性机会",
    "关键命题",
    "深层逻辑",
    "技术底座",
    "公共底座",
    "技术主权",
    "单点风险",
    "主脊柱",
    "材料锚点",
    "认知增量",
    "迭代闭环",
)

CONTEXT_JARGON = (
    "沉淀",
    "颗粒度",
    "对齐",
    "协同",
    "链路",
    "生态位",
    "心智",
    "范式",
    "方法论",
    "核心变量",
    "打法",
    "想象空间",
    "闭环",
    "不丢",
)

LYRIC_WORDS = (
    "安放",
    "抵达",
    "微光",
    "褶皱",
    "丰盈",
    "滚烫",
    "轻盈",
    "赤裸",
    "剥开",
)

ROAD_SIGNS = (
    "更微妙的是",
    "还有一层",
    "只说对了一半",
    "值得注意的是",
    "需要指出的是",
    "从某种意义上说",
)

ROAD_STRIP_CHARS = "。！？!? \n"

DASH_OCCURRENCE = re.compile(r"——|—|–")

PIVOT_PATTERNS = (
    re.compile(r"(?:并)?不是[^。！？\n]{0,90}而是"),
    re.compile(r"并非[^。！？\n]{0,90}而是"),
    re.compile(r"不在于[^。！？\n]{0,90}而在于"),
    re.compile(r"与其说[^。！？\n]{0,90}(?:不如|毋宁|倒不如)"),
    re.compile(r"[。！？!?]\s*而是"),
    re.compile(r"表面(?:上)?[^。！？\n]{0,90}(?:其实|实际|实则)"),
    re.compile(r"看似[^。！？\n]{0,90}(?:其实|实际|实则)"),
)

SEMANTIC_PIVOT_PATTERNS = (
    re.compile(r"(?:总|一直|曾|都)?以为[^！？\n]{2,60}?(?:其实|才发现|才明白|才知道|后来才)"),
    re.compile(r"(?:总|都|一直)以为[^！？\n]{2,60}?[。，](?:可|但|其实)"),
    re.compile(r"回头(?:看|一看)?才(?:发现|明白|知道)"),
    re.compile(r"(?:并)?不是[^。！？\n]{1,40}，(?:更|才)?是[^，。！？\n]"),
    re.compile(r"从来(?:都)?(?:不是|与[^。！？，\n]{1,12}无关)"),
    re.compile(r"答案(?:是否定的|恰恰相反)|恰恰相反"),
    re.compile(r"表面(?:上)?[^！？\n]{0,60}。[^！？\n]{0,12}(?:其实|实际|实则)"),
    re.compile(r"看似[^！？\n]{0,60}。[^！？\n]{0,12}(?:其实|实际|实则)"),
    re.compile(r"[^，。！？\n]{1,12}不重要，(?:重要|要紧)的是"),
    re.compile(r"真正[^，。！？\n]{0,16}的(?:，)?是"),
    re.compile(r"不只(?:是)?[^。！？\n]{0,90}(?:还|也)"),
)

NOMINALIZATION_PATTERNS = (
    re.compile(r"进行(?:了|一次|一场|着)?[^。，！？\n]{0,10}(?:调整|优化|升级|分析|讨论|沟通|梳理|复盘|迭代|探索|尝试|思考|规划|布局)"),
    re.compile(r"实现了?[^。，！？\n]{0,14}的?[^。，！？\n]{0,6}(?:提升|增长|突破|转变|跃升|落地)"),
    re.compile(r"完成了?对[^。，！？\n]{0,16}的"),
    re.compile(r"起到了?[^。，！？\n]{0,12}的?作用"),
    re.compile(r"具有[^。，！？\n]{0,10}(?:意义|价值)"),
)

CONJUNCTIONS = (
    "因为",
    "所以",
    "但是",
    "然而",
    "同时",
    "此外",
    "而且",
    "并且",
    "因此",
    "不仅",
)

ROAD_SIGN_PATTERNS = (
    re.compile(
        rf"(?:^|[。！？!?]\s*){re.escape(ROAD_SIGNS[0])}[^。！？!?\n]{{0,24}}",
        re.MULTILINE,
    ),
    re.compile(
        rf"(?:^|[。！？!?]\s*){re.escape(ROAD_SIGNS[1])}(?=(?:更|原因|问题|意思|考虑|变化|逻辑|价值|作用|风险|影响|值得|很少|不容易|常被|往往))[^。！？!?\n]{{0,24}}",
        re.MULTILINE,
    ),
    *(
        re.compile(
            rf"(?:^|[。！？!?]\s*){re.escape(phrase)}[^。！？!?\n]{{0,24}}",
            re.MULTILINE,
        )
        for phrase in ROAD_SIGNS[2:]
    ),
)

SOFT_MARKERS = (
    "真正",
    "本质上",
    "更深层次",
    "归根结底",
    "换句话说",
    "不可否认",
    "核心是",
    "关键在于",
    "这意味着",
)

REPEATED_OPENERS = (
    "其实",
    "不过",
    "当然",
    "所以",
    "但是",
    "后来",
    "当时",
    "很多人",
    "问题是",
    "更重要的是",
    "说到这里",
)

LEFT_BRANCH_PATTERNS = (
    re.compile(r"(?:^|[。！？]\s*)在[^，。！？\n]{12,70}(?:以后|之后|之前|以前|过程中|情况下|背景下)，"),
    re.compile(r"(?:^|[。！？]\s*)那些[^，。！？\n]{10,60}的[^，。！？\n]{2,30}[，。]"),
    re.compile(r"(?:^|[。！？]\s*)(?:真正|最终|最后)让[^，。！？\n]{8,70}的，是"),
)

METAPHOR_FIELDS = {
    "温度": ("降温", "升温", "冷却", "余温", "温度最高"),
    "生死战争": ("杀死", "死因", "枪响", "开火", "战场", "引爆", "弹药"),
    "建筑灾害": ("坍塌", "崩塌", "地基", "砖头", "支柱", "废墟"),
    "仓储租赁": ("仓库", "库房", "租金", "取货", "入库", "库存"),
    "道路竞赛": ("赛道", "跑道", "岔路", "十字路口", "终点线", "门票"),
    "机器器官": ("齿轮", "引擎", "发动机", "血管", "骨架", "肌肉"),
    "海洋航行": ("蓝海", "浪潮", "潮水", "航船", "灯塔", "彼岸"),
}


@dataclass
class Paragraph:
    position: int
    text: str
    han: int
    sentences: int


def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def excerpt(value: str, width: int = 72) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= width else value[: width - 1] + "…"


def mask_non_prose(text: str) -> str:
    """Mask code, URLs, and machine metadata while keeping character positions and line breaks."""

    def mask(match: re.Match[str]) -> str:
        return "".join("\n" if char == "\n" else " " for char in match.group())

    patterns = (
        re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL),
        re.compile(r"```.*?```", re.DOTALL),
        re.compile(r"`[^`\n]*`"),
        re.compile(r"\]\([^\n)]*\)"),
        re.compile(r"https?://[^\s)>]+"),
        re.compile(r"<[^>\n]+>"),
    )
    masked = text
    for pattern in patterns:
        masked = pattern.sub(mask, masked)
    return masked


def non_overlapping_terms(text: str, terms: tuple[str, ...]):
    matches = []
    occupied = []
    for term in sorted(terms, key=len, reverse=True):
        for match in re.finditer(re.escape(term), text):
            start, end = match.span()
            if any(start < old_end and end > old_start for old_start, old_end in occupied):
                continue
            matches.append((start, term))
            occupied.append((start, end))
    return sorted(matches)


def all_matches(text: str, patterns: tuple[re.Pattern[str], ...]):
    matches = []
    for pattern in patterns:
        matches.extend(pattern.finditer(text))
    return sorted(matches, key=lambda match: match.start())


def heavy_de_sentences(text: str):
    """Find long sentences whose main clause may be pushed back by multiple "的"."""

    matches = []
    pattern = re.compile(r"[^。！？!?\n]+(?:[。！？!?]|$)")
    for match in pattern.finditer(text):
        value = match.group()
        if han_count(value) >= 38 and value.count("的") >= 4:
            matches.append(match)
    return matches


def anaphora_runs(text: str, minimum: int = 3):
    """Find parallelism where three or more clauses in one sentence share the same opening."""

    matches = []
    for sentence in re.finditer(r"[^。！？!?\n]+(?:[。！？!?]|$)", text):
        clauses = [
            clause.strip()
            for clause in re.split(r"[，、；,;]", sentence.group())
            if han_count(clause) >= 3
        ]
        if len(clauses) < minimum:
            continue
        run = 1
        for previous, current in zip(clauses, clauses[1:]):
            if previous[:2] == current[:2] and re.match(r"[一-鿿]{2}", current):
                run += 1
                if run >= minimum:
                    matches.append(sentence)
                    break
            else:
                run = 1
    return matches


def sentence_length_cv(text: str):
    """Sentence-length coefficient of variation. Human writing mixes long and short sentences widely; model sentence lengths stay close together."""

    lengths = [
        han_count(match.group())
        for match in re.finditer(r"[^。！？!?\n]+[。！？!?]", text)
        if han_count(match.group()) >= 4
    ]
    if len(lengths) < 12:
        return None
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return None
    variance = sum((value - mean) ** 2 for value in lengths) / len(lengths)
    return (variance ** 0.5) / mean, len(lengths)


def bracket_highlights(text: str):
    """Phrases wrapped in 「」. Too many means golden lines are being mass-produced."""

    return list(re.finditer(r"[「『][^」』\n]{1,6}[」』]", text))


def prose_paragraphs(text: str) -> list[Paragraph]:
    """Split paragraphs by line (in web-novel chapters each paragraph is one line; blank lines are only separators)."""

    paragraphs = []
    position = 0
    for line in text.splitlines():
        start = position
        position += len(line) + 1
        clean = re.sub(r"[>*_`]", "", line).strip()
        if not clean or clean.startswith(("#", "http", "![", "```")):
            continue
        if re.match(r"^(?:[-+*]|\d+[.、])\s", clean):
            continue
        count = han_count(clean)
        if count < 4:
            continue
        sentences = max(1, len(re.findall(r"[。！？!?]", clean)))
        paragraphs.append(Paragraph(start, clean, count, sentences))
    return paragraphs


def metaphor_cluster(text: str, distance: int = 800):
    hits = []
    for field, words in METAPHOR_FIELDS.items():
        for word in words:
            for match in re.finditer(re.escape(word), text):
                hits.append((match.start(), field, word))
    hits.sort()
    for index, (start, _, _) in enumerate(hits):
        window = [hit for hit in hits[index:] if hit[0] - start <= distance]
        fields = {hit[1] for hit in window}
        if len(fields) >= 3:
            return window, fields
    return None


def short_streak(paragraphs: list[Paragraph], limit: int = 4):
    streak = []
    for paragraph in paragraphs:
        if paragraph.han <= 24 and paragraph.sentences <= 1:
            streak.append(paragraph)
            if len(streak) >= limit:
                return streak
        else:
            streak = []
    return None


def opener_counts(paragraphs: list[Paragraph]):
    counts = collections.Counter()
    examples = {}
    for paragraph in paragraphs:
        value = paragraph.text.lstrip("“‘\"（(")
        for opener in REPEATED_OPENERS:
            if value.startswith(opener):
                counts[opener] += 1
                examples.setdefault(opener, paragraph.position)
                break
    return counts, examples


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a finished Chinese manuscript for AI-flavor hard bans and statistical patterns")
    parser.add_argument("path", help="Path to a Markdown or text file. Use - to read from standard input")
    args = parser.parse_args()

    try:
        text = read_text(args.path)
    except (OSError, UnicodeError) as error:
        print(f"Cannot read the manuscript. {error}", file=sys.stderr)
        return 2

    prose = mask_non_prose(text)
    total_han = han_count(prose)
    if total_han == 0:
        print("No Chinese characters detected.", file=sys.stderr)
        return 2

    failures = []
    warnings = []

    stop_matches = non_overlapping_terms(prose, HARD_STOPS)
    for position, phrase in stop_matches:
        failures.append(f"Hard-stop word, line {line_number(text, position)}: {phrase}")

    jargon_matches = non_overlapping_terms(prose, HARD_JARGON)
    for position, phrase in jargon_matches:
        failures.append(f"Jargon, line {line_number(text, position)}: {phrase}")

    context_jargon_matches = non_overlapping_terms(prose, CONTEXT_JARGON)
    hard_spans = [
        (position, position + len(phrase)) for position, phrase in jargon_matches
    ]
    context_jargon_matches = [
        (position, phrase)
        for position, phrase in context_jargon_matches
        if not any(
            position < end and position + len(phrase) > start
            for start, end in hard_spans
        )
    ]
    if context_jargon_matches:
        samples = "、".join(
            dict.fromkeys(phrase for _, phrase in context_jargon_matches)
        )
        lines = "、".join(
            dict.fromkeys(
                str(line_number(text, position))
                for position, _ in context_jargon_matches[:8]
            )
        )
        warnings.append(
            f"{len(context_jargon_matches)} word(s) need a context check."
            f"They appear on line(s) {lines}: {samples}. Keep them when the literal meaning is accurate; rewrite them when they are used to inflate the writing."
        )

    road_signs = all_matches(prose, ROAD_SIGN_PATTERNS)
    for match in road_signs:
        failures.append(
            f"Model signpost, line {line_number(text, match.start())}:"
            f"“{excerpt(match.group().lstrip(ROAD_STRIP_CHARS))}”"
        )

    pivots = all_matches(prose, PIVOT_PATTERNS)
    for match in pivots:
        failures.append(
            f"Banned reversal sentence, line {line_number(text, match.start())}:"
            f"“{excerpt(match.group())}”"
        )

    occupied_spans = [match.span() for match in pivots]
    semantic_pivots = []
    for match in all_matches(prose, SEMANTIC_PIVOT_PATTERNS):
        if any(
            match.start() < end and match.end() > start
            for start, end in occupied_spans
        ):
            continue
        semantic_pivots.append(match)
        occupied_spans.append(match.span())
    for match in semantic_pivots:
        warnings.append(
            f"Suspected reversal-rhetoric variant, line {line_number(text, match.start())}:"
            f"\u201c{excerpt(match.group(), 44)}\u201d. If it sets up a misunderstanding only to overturn it, rewrite it as a direct statement; keep normal usage."
        )

    anaphoras = anaphora_runs(prose)
    for match in anaphoras[:4]:
        warnings.append(
            f"Parallelism of three or more identical structures, line {line_number(text, match.start())}:"
            f"\u201c{excerpt(match.group(), 44)}\u201d. Keep two items; rephrase or delete the third."
        )

    lyric_matches = non_overlapping_terms(prose, LYRIC_WORDS)
    if len(lyric_matches) >= 2:
        samples = "、".join(dict.fromkeys(term for _, term in lyric_matches))
        warnings.append(
            f"Model-favored lyrical words, {len(lyric_matches)} occurrences: {samples}."
            "Keep them when describing concrete things; delete them when they dress up abstract concepts."
        )

    nominalizations = all_matches(prose, NOMINALIZATION_PATTERNS)
    for match in nominalizations[:4]:
        warnings.append(
            f"Nominalized sentence, line {line_number(text, match.start())}:"
            f"\u201c{excerpt(match.group(), 36)}\u201d. Restore it to a direct verb."
        )

    conjunction_hits = non_overlapping_terms(prose, CONJUNCTIONS)
    if total_han >= 600 and len(conjunction_hits) * 1000 / total_han > 7:
        samples = "、".join(
            f"{term} {count} times"
            for term, count in collections.Counter(
                term for _, term in conjunction_hits
            ).most_common(4)
        )
        warnings.append(
            f"Conjunction density is high: {len(conjunction_hits) * 1000 // total_han} per thousand characters. {samples}."
            "In Chinese, short clauses connect by word order and logic; try deleting half of them."
        )

    highlights = bracket_highlights(prose)
    highlight_limit = max(3, total_han // 700)
    if len(highlights) > highlight_limit:
        samples = "、".join(dict.fromkeys(match.group() for match in highlights[:6]))
        warnings.append(
            f"{len(highlights)} phrases wrapped in 「」. {samples}. Too many means golden lines are being mass-produced."
        )

    cv_result = sentence_length_cv(prose)
    if cv_result and cv_result[0] < 0.42:
        warnings.append(
            f"{cv_result[1]} sentences in the whole text are too close in length (coefficient of variation {cv_result[0]:.2f})."
            "In human-written paragraphs a ten-character sentence sits next to a forty-character one; loosen a few sentences and shorten a few."
        )

    marker_matches = non_overlapping_terms(prose, SOFT_MARKERS)
    marker_limit = max(2, total_han // 900)
    if len(marker_matches) > marker_limit:
        samples = "、".join(dict.fromkeys(term for _, term in marker_matches))
        warnings.append(
            f"{len(marker_matches)} insight signposts in total; the current alert threshold is {marker_limit}."
            f"Check {samples} closely."
        )

    left_branches = all_matches(prose, LEFT_BRANCH_PATTERNS)
    left_limit = max(2, total_han // 1200)
    if len(left_branches) > left_limit:
        samples = "；".join(
            f"第 {line_number(text, match.start())} 行“{excerpt(match.group(), 44)}”"
            for match in left_branches[:4]
        )
        warnings.append(
            f"{len(left_branches)} long front-loaded elements; they may delay the main clause too long. {samples}"
        )

    dense_de = heavy_de_sentences(prose)
    dense_de_limit = max(1, total_han // 1500)
    if len(dense_de) > dense_de_limit:
        samples = "；".join(
            f"第 {line_number(text, match.start())} 行“{excerpt(match.group(), 44)}”"
            for match in dense_de[:4]
        )
        warnings.append(
            f"{len(dense_de)} long sentence(s) contain more than four \u201c的\u201d; introduce the people and actions first. {samples}"
        )

    paragraphs = prose_paragraphs(prose)

    dash_dense_paragraphs = 0
    for paragraph in paragraphs:
        dash_count = len(DASH_OCCURRENCE.findall(paragraph.text))
        if dash_count >= 3:
            dash_dense_paragraphs += 1
            warnings.append(
                f"Paragraph on line {line_number(text, paragraph.position)} has {dash_count} dashes;"
                "Judge each one by usage: delete a dash (and the content on both sides) when the meaning stays the same without it (common-rules.md dash rule)."
            )

    if len(paragraphs) >= 10:
        one_sentence = sum(paragraph.sentences <= 1 for paragraph in paragraphs)
        ratio = one_sentence / len(paragraphs)
        if ratio >= 0.75:
            warnings.append(
                f"{ratio:.0%} of recognizable paragraphs have only one sentence, which may form a uniform short-paragraph drumbeat."
            )

    streak = short_streak(paragraphs)
    if streak:
        first = streak[0]
        warnings.append(
            f"{len(streak)} short single-sentence paragraphs appear in a row starting from line {line_number(text, first.position)};"
            "Check whether they are queuing up to shout conclusions."
        )

    counts, opener_examples = opener_counts(paragraphs)
    repeated = [(opener, count) for opener, count in counts.items() if count >= 4]
    if repeated:
        details = "、".join(f"{opener} {count} times" for opener, count in repeated)
        first_position = min(opener_examples[opener] for opener, _ in repeated)
        warnings.append(
            f"Repeated paragraph openings, starting near line {line_number(text, first_position)}. {details}."
        )

    metaphors = metaphor_cluster(prose)
    if metaphors:
        window, fields = metaphors
        samples = "、".join(dict.fromkeys(hit[2] for hit in window))
        warnings.append(
            f"{len(fields)} metaphor system(s) appear within eight hundred characters. {'、'.join(sorted(fields))}."
            f"Example words: {samples}."
        )

    print(f"Chinese character count: {total_han}")
    print(
        f"Reversal sentences {len(pivots)}, reversal-rhetoric variants {len(semantic_pivots)},"
        f"Parallel structures {len(anaphoras)}, nominalizations {len(nominalizations)},"
        f"Jargon {len(jargon_matches)}, hard-stop words {len(stop_matches)},"
        f"Model signposts {len(road_signs)}, context-check words {len(context_jargon_matches)},"
        f"Lyrical words {len(lyric_matches)}, insight signposts {len(marker_matches)},"
        f"Long front-loaded elements {len(left_branches)}, heavy-\u201c的\u201d sentences {len(dense_de)},"
        f"Dash-dense paragraphs {dash_dense_paragraphs}"
    )

    if failures:
        print("\nNeeds changes")
        for item in failures:
            print(f"- {item}")

    if warnings:
        print("\nNeeds human review")
        for item in warnings:
            print(f"- {item}")

    if not failures and not warnings:
        print("\nNo problems covered by this checker were found.")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
