#!/usr/bin/env python3
"""style-distiller LLM refactor: acceptance aggregation rules module (case-2 acceptance report + reroll decision).

Pure data + pure functions, no LLM calls:
- CHECK_CATEGORIES: four acceptance check categories (spec 7.1)
- verdict: aggregate a violation report into PASS/FAIL (spec 7.1)
- should_reroll: reroll decision, round < 3 with a violation this round means rewrite (spec 7.2)
- pick_best: pick the best when over the limit, the round with the fewest violations, latest on ties
- format_report: render the violation report table (item no. / original requirement / body performance / violated or not / advice + conclusion row)

anti-ai outputs violation reports in this format (see verify-checklist.md); this module is the deterministic test encoding.

Usage: python tools/style_verify.py < violations.json
Exit code 0 = success (the PASS/FAIL conclusion is on the last report line).
"""
from __future__ import annotations

import sys

from style_common import force_utf8

force_utf8()

# 1) Four acceptance check categories (spec 7.1)
CHECK_CATEGORIES = ["numeric/percentage items", "hard-rule items", "modeling-rule items", "soft-guidance items"]

# Violation-decision convergence whitelist (spec 7.1 / verify-checklist.md): string booleans from LLM output all converge through this list;
# before matching, strip trailing punctuation and particles ('是。' to '是', '违反了' to '违反', '是；' to '是'); anything outside the whitelist counts as not violated
# ('false' / '否' / empty / any other string).
VIOLATED_STRINGS = frozenset({"true", "是", "yes", "1", "违反", "违反了"})

def _is_violated(v) -> bool:
    """violated decision: bool and string booleans both converge; the LLM may output strings like '是。' / '违反了' / '是；', and a misjudgment would trigger a wrong reroll.
    Strings follow truthy semantics: 'true' / '是' / 'yes' / '1' / '违反' / '违反了' (including trailing punctuation/particles) mean violated; everything else ('false' / '否' / empty) means not violated."""
    if v is None:
        return False
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        s = v.strip().strip("。？！…，,.!? ；; 　").strip("了")
        return s.lower() in VIOLATED_STRINGS
    return bool(v)

def verdict(items: list[dict]) -> str:
    """No violations at all means PASS; any violation means FAIL"""
    return "FAIL" if any(_is_violated(i.get("violated")) for i in items) else "PASS"

def should_reroll(round_no: int, violated: int) -> bool:
    """Reroll decision (spec 7.2): round < 3 with a violation this round means rewrite"""
    return round_no < 3 and violated > 0

def _violated_count(v) -> int:
    """violated count convergence: int/float as-is, numeric strings to int ('3.0' to 3, '10' to 10), bool/None/illegal/non-finite to 0.
    The LLM may output a count as a string ("3"); a raw comparison would raise TypeError or pick wrongly by lexicographic order ("10" < "3"); True is a boolean, not a count."""
    if v is None or isinstance(v, bool):
        return 0
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0
    if f != f or f in (float("inf"), float("-inf")):   # filter nan/inf
        return 0
    return int(f)

def pick_best(rounds: list[dict]) -> dict:
    """Pick the best when over the limit (spec 7.2): the round with the fewest violations, latest on ties.
    Ties are broken by list position (later means newer) to avoid relying on dict == (identical dicts would degenerate to picking the oldest).
    An empty round list returns an empty dict (the caller treats it as no violations), so min() never raises ValueError."""
    if not rounds:
        return {}
    return min(enumerate(rounds), key=lambda ir: (_violated_count(ir[1].get("violated", 0)), -ir[0]))[1]

def format_report(items: list[dict]) -> str:
    """Render the violation report table (spec 7.1 output format)"""
    lines = ["| 条号 | 原文要求 | 正文表现 | 违反与否 | 建议 |", "|---|---|---|---|---|"]
    for i, it in enumerate(items, 1):
        lines.append(
            f"| {it.get('no', i)} | {it.get('require', '')} | {it.get('evidence', '')} | "
            f"{'是' if _is_violated(it.get('violated')) else '否'} | {it.get('advice', '')} |"
        )
    n_v = sum(1 for i in items if _is_violated(i.get("violated")))
    lines.append(f"\n结论：{verdict(items)}（{n_v}/{len(items)}）")   # the conclusion row reuses verdict() (review #42)
    return "\n".join(lines)

if __name__ == "__main__":
    import json, sys
    items = json.load(sys.stdin)          # Example: [{"no":1,"require":"ban '宛如'","evidence":"appears 1 time","violated":true,"advice":"replace"}]
    print(format_report(items))
