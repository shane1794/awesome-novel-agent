#!/usr/bin/env python3
"""Chapter-delivery deterministic check. Reports only; never edits the text automatically.

Division of labor with check-prose.py: check-prose handles AI-flavor statistical patterns (anti-ai Phase 2/4),
while this tool handles hard chapter-delivery defects (quote sandwiching, nested quotes, half-width quotes, word-count reconciliation, regression strings).
Punctuation follows knowledge/anti-ai/common-rules.md: dashes/ellipses are not hard-banned;
when a paragraph has 3 or more, prompt a case-by-case usage check.

Project-level assets live outside the tool (skipped when missing; search up to 5 parent directories):
  sandbox/prose-regressions.txt  regression pattern library (exact strings that failed before, one per line; a hit is a hard failure)
  sandbox/locked-lines.txt       locked-lines whitelist (one per line; a hit line skips adjudication checks)

Usage: python3 check-chapter.py <manuscript path|directory> [more paths...]   (a directory scans its *.md files)
Exit codes: 0 = no hard hits (reviewable warnings may remain); 1 = hard hits found; 2 = usage error or read failure
"""

from __future__ import annotations

import re
import sys
from glob import glob
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

MAX_PARENTS = 5

# ---- Hard checks (a hit means failure) ----
SANDWICH_TAG = re.compile(r"。”[^”\n]{0,14}，“")
NESTED_QUOTE = re.compile(r"“[^”]*“[^”]*”")
HALFWIDTH_QUOTE = re.compile(r"[\"']")

# Word-count claims auto-checked: number before the quote / quote before the number
NUM = r"[一二两三四五六七八九十俩仨]{1,3}"
COUNT_QUOTE_AFTER = re.compile(
    r"(?:这|那|就|才|整整|刚好|一共|第)?(" + NUM + r")个字[，。：：]?[“‘]([^”’‘\n]{1,30})[”’]"
)
QUOTE_COUNT_BEFORE = re.compile(
    r"[“‘]([^”’‘\n]{1,30})[”’](?:这|那)?(" + NUM + r")个字"
)
# Word-count claims with no quote to check against: prompt a manual character-by-character check
COUNT_BARE = re.compile(r"(?:这|那|就|才|整整|刚好|一共)?" + NUM + r"个字")

CN_NUM = {"零": 0, "一": 1, "二": 2, "两": 2, "俩": 2, "三": 3, "仨": 3, "四": 4,
          "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn2int(s: str):
    if s in CN_NUM:
        return CN_NUM[s]
    if s == "十":
        return 10
    if len(s) == 2 and s[0] in CN_NUM and s[1] == "十":
        return CN_NUM[s[0]] * 10
    if len(s) == 2 and s[0] == "十" and s[1] in CN_NUM:
        return 10 + CN_NUM[s[1]]
    return None


def han_count(s: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", s))


# ---- Warning-level checks (need human review, do not fail) ----
# Dashes/ellipses: follow the common-rules usage check, prompt only when a paragraph has 3 or more (web novels use one line per paragraph)
DASH_DENSE = re.compile(r"——|—|--|……")
SPEECH_VERB = r"(?:说|问|答|回|喊|叫|道|念)"
# General sandwich: two quoted passages separated by a short narration containing a speech verb (attribution needs review)
SANDWICH_BROAD = re.compile(r"”[^”\n]{1,18}“")
SANDWICH_MID_VERB = re.compile(SPEECH_VERB + r"|接话|插|补|应|骂|叹|劝|拦")
# Multi-turn Q&A in one paragraph: 3 or more "pronoun + speech verb" occurrences in the same paragraph
QA_DENSITY = re.compile(r"(?:我|他|她|他们|她们)" + SPEECH_VERB)
QA_DENSITY_LIMIT = 3
# Trailing-tag narrow set (ends with pronoun + speech verb; the character-name table is a book-level asset and does not belong in this general tool)
TRAILING_TAG = re.compile(r"”[^”\n]{0,12}(?:我|他|她|他们|她们)" + SPEECH_VERB + r"。")
# Weak-adverb density: warn when the per-thousand-character share exceeds the threshold (3 per thousand characters, matching the anti-ai rule)
WEAK_ADVERB = re.compile(r"缓缓|微微|轻轻|淡淡")
WEAK_ADVERB_PER_KILO = 3


def load_lines_file(start: Path, name: str) -> list[str]:
    """Search upward from start and its parent directories for sandbox/<name>; return the list of non-empty lines."""
    cur = start.resolve().parent
    for _ in range(MAX_PARENTS):
        f = cur / "sandbox" / name
        if f.exists():
            try:
                return [ln.strip() for ln in
                        f.read_text(encoding="utf-8-sig").splitlines()
                        if ln.strip() and not ln.strip().startswith("#")]
            except OSError:
                return []
        if cur.parent == cur:
            break
        cur = cur.parent
    return []


def iter_prose_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(Path(f) for f in sorted(glob(str(path / "*.md"))))
        else:
            files.append(path)
    return files


def check_file(path: Path, regressions: list[str], hard_hits: list[str]) -> None:
    print(f"== {path.name} ==")
    text = path.read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    whitelist = set(load_lines_file(path, "locked-lines.txt"))

    warned_words = False
    for lineno, ln in enumerate(lines, 1):
        locked = ln.strip() in whitelist
        excerpt = ln[:60]

        def report(tag: str, hard: bool, ctx: str = excerpt) -> None:
            prefix = "" if hard else "(needs review) "
            print(f"  [{tag}] {prefix}L{lineno}: {ctx}")

        # Whitelist line: skip adjudication checks and note the reason
        if locked:
            print(f"  [whitelist skipped] L{lineno}: {ln.strip()[:40]}")
            continue

        # --- Hard ---
        if SANDWICH_TAG.search(ln):
            report("sandwich (labelled)", True)
            hard_hits.append(f"{path.name}:{lineno} sandwich (labelled)")
        if NESTED_QUOTE.search(ln):
            report("nested double quotes", True)
            hard_hits.append(f"{path.name}:{lineno} nested double quotes")
        if HALFWIDTH_QUOTE.search(ln):
            report("half-width quotes", True)
            hard_hits.append(f"{path.name}:{lineno} half-width quotes")
        for m in COUNT_QUOTE_AFTER.finditer(ln):
            want, got = cn2int(m.group(1)), han_count(m.group(2))
            if want is not None and want != got:
                report(f"word-count claim mismatch (claimed {want}, actual {got})", True)
                hard_hits.append(f"{path.name}:{lineno} word-count claim mismatch")
        for m in QUOTE_COUNT_BEFORE.finditer(ln):
            want, got = cn2int(m.group(2)), han_count(m.group(1))
            if want is not None and want != got:
                report(f"word-count claim mismatch (claimed {want}, actual {got})", True)
                hard_hits.append(f"{path.name}:{lineno} word-count claim mismatch")
        for pat in regressions:
            if pat in ln:
                report(f"regression library ({pat[:10]}...)", True)
                hard_hits.append(f"{path.name}:{lineno} regression library")
                break

        # --- Warnings (need review) ---
        if len(DASH_DENSE.findall(ln)) >= 3:
            report("dense dashes/ellipses", False)
        if any(SANDWICH_MID_VERB.search(m.group(0))
               for m in SANDWICH_BROAD.finditer(ln)):
            report("sandwich (general)", False)
        if len(QA_DENSITY.findall(ln)) >= QA_DENSITY_LIMIT:
            report("multi-turn Q&A in one paragraph", False)
        if TRAILING_TAG.search(ln):
            report("trailing tag", False)
        if COUNT_BARE.search(ln) and not (COUNT_QUOTE_AFTER.search(ln)
                                          or QUOTE_COUNT_BEFORE.search(ln)):
            report("word-count claim (verify character by character)", False)

    # Weak-adverb density (file level)
    n_adv = len(WEAK_ADVERB.findall(text))
    n_han = han_count(text)
    if n_han > 0 and n_adv > WEAK_ADVERB_PER_KILO * n_han / 1000:
        print(f"  [weak-adverb density exceeded] (needs review) {n_adv} occurrences / {n_han} characters")

    # Platform word count (counted only, no threshold; word-count requirements are book-level settings)
    body = text.split("\n", 1)[1] if text.startswith("#") else text
    han = han_count(body)
    full = len(re.findall(r"[\u3000-\u303f\uff00-\uffef]", body))
    quotes = body.count("\u201c") + body.count("\u201d")
    digits = len(re.findall(r"[0-9]", body))
    print(f"  Platform word count: {han + full + quotes + digits}"
          f"  Chinese chars {han}, full-width {full}, quotes {quotes}, digits {digits}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    files = iter_prose_files(sys.argv[1:])
    if not files:
        print("No files found to check")
        return 2
    regressions = load_lines_file(files[0], "prose-regressions.txt")

    hard_hits: list[str] = []
    for path in files:
        try:
            check_file(path, regressions, hard_hits)
        except OSError as e:
            print(f"  Read failed: {path}: {e}")
            return 2

    if hard_hits:
        print(f">>> {len(hard_hits)} hard hit(s) found; clear them all or adjudicate each one before delivery <<<")
        return 1
    print(">>> No hard hits (warnings still need human review) <<<")
    return 0


if __name__ == "__main__":
    sys.exit(main())
