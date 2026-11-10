#!/usr/bin/env python3
"""style-distill shared utilities (single-sourced, review #36/#38/#39/#40).

Shared by style_render / style_verify / check-agents / platforms / tests to avoid drift across copies:
- force_utf8         force UTF-8 on stdout/stderr (prevents Windows GBK crashes, replacing the reconfigure copied into each script)
- frontmatter_text   extract the raw frontmatter text (locate the closing line by line, so a value containing '---' does not misalign; BOM-compatible)
- split_frontmatter  frontmatter to (dict, body) (missing closing line / parse failure / non-map to ({}, raw text))
- SCENE_INJECTION    scene sparse-injection matrix (the single authority; check-agents derives its scene/dimension enumeration from it)
- pct_ok             decision A unit check: a legal percentage value in 0-100 (type excludes bool)
"""
from __future__ import annotations

import sys


def force_utf8() -> None:
    """Force UTF-8 on stdout/stderr to avoid Windows GBK console errors (AGENTS.md:79)."""
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass


def frontmatter_text(text: str) -> str | None:
    """Raw frontmatter text (between the two --- lines). Locate the closing line by line, so body text containing '---' (a markdown divider) does not misalign;
    return None when the closing line is missing. BOM-compatible (init's utf-8-sig convention, review #23)."""
    text = text.lstrip("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def split_frontmatter(text: str) -> tuple:
    """frontmatter to (dict, body). Missing closing line / parse failure / non-map to ({}, raw text)."""
    import yaml
    text = text.lstrip("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = "\n".join(lines[1:i])
            try:
                data = yaml.safe_load(fm)
            except Exception:
                data = None
            return (data if isinstance(data, dict) else {}), "\n".join(lines[i + 1:])
    return {}, text


# Scene sparse-injection matrix (spec 6.3 / old injection-template table), the single authority; check-agents derives its enumeration from it
SCENE_INJECTION = {
    "general": ["lexicon", "syntax", "rhythm", "rhetoric", "emotion_expression",
                "narrative", "dialogue_style", "cohesion", "verb_style"],
    "dialogue": ["lexicon", "dialogue_style"],
    "fight": ["verb_style", "syntax"],
    "environment": ["rhetoric", "rhythm"],
    "inner-mono": ["emotion_expression", "narrative"],
    "transition": ["cohesion", "rhythm"],
    "group-scene": ["rhythm", "dialogue_style"],
}

STYLE_CARD_SCENE_TYPES = frozenset(SCENE_INJECTION)
STYLE_CARD_DIMS = list(SCENE_INJECTION["general"])


def pct_ok(v) -> bool:
    """Decision A unit check: a legal percentage value in 0-100 (type excludes bool, since True/False are int subclasses).
    The old jieba engine produced 0-100 percentages with one decimal place (13.4), so 0.3 means 0.3%, not 30%."""
    return type(v) in (int, float) and not isinstance(v, bool) and 0 <= v <= 100
