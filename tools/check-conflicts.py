#!/usr/bin/env python3
"""Static check for anti-AI rule conflicts

Scan the rule files under knowledge/ and skills/ for two kinds of problems:

A. Threshold conflicts: the same object is given different numeric thresholds in different files.
   The authoritative source is knowledge/anti-ai/common-rules.md. If another file gives a threshold for the same object
   with a different number, report a conflict (the responsibility statement requires other files to reference, not redefine).

B. Boundary violations: methodology/exemption files (anti-ai-writing.md, boundary-cases.md)
   exist to explain "why" and "how", and must not contain numeric thresholds. Any found is reported as a violation.

C. Banned terms/anti-patterns (audit 2026-08-13 section 3-C5, decision P2-10):
   The prompt structure is unified as "6 elements", so the legacy terms below are banned from the injection side
   (agents/skills/knowledge); the anti-pattern sentence "叙事规则优先级高于所有约束"
   is banned everywhere except prompt-audit.md (acceptance probe definitions, which must be kept), to prevent old wording from returning.

Usage: python tools/check-conflicts.py
Exit code 0 = pass, non-zero = problems found (used by CI).

Threshold formats (two supported):
  - Code block: 单章阈值: 5 次 | 严重度: medium
  - Table:   | 疲劳词 | 3 次 | 替代策略 |
"""

import sys
import re
from pathlib import Path

for s in (sys.stdout, sys.stderr):
    try:
        s.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "knowledge"
SKILLS_DIR = ROOT / "skills"

# The single authoritative source; other files' thresholds defer to it
AUTHORITY = KNOWLEDGE_DIR / "anti-ai" / "common-rules.md"

# Boundary whitelist: these files are methodology/exemption files, so numeric thresholds are banned in them
METHODOLOGY_FILES = [
    "knowledge/anti-ai/anti-ai-writing.md",
    "knowledge/anti-ai/boundary-cases.md",
]

# Scan scope: all .md files under knowledge/ + skills/
SCAN_GLOBS = [
    (KNOWLEDGE_DIR, "knowledge"),
    (SKILLS_DIR, "skills"),
]

# Match "object | number 次" table rows (plain numbers: | 默默 | 3 次 |)
TBL_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(\d+)\s*(次)")
# Match "object | ≤N 次[/unit]" table rows (≤ format: | 突然/忽然 | ≤4次/章 |, or the bare quick-reference format | 然而/不过 | ≤4次 |)
TBL_LE_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(?:≤|≤)?(\d+)\s*(次)(?:/(?:章|500字|段|千字))?")
# Match "object | N 句" table rows (dialogue-density class: ≥8 consecutive sentences)
TBL_SEN_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(?:≥|>)?(\d+)\s*(句)")
# Match "单章阈值: number 次[/unit]"
CODE_RE = re.compile(r"单章阈值[:：]\s*(\d+)\s*(次)(?:/(章|500字|段|千字))?")
# Generic quantity threshold (for boundary detection; only "次" counts, sentence-count examples in methodology text do not count as violations)
ANY_COUNT_RE = re.compile(r"(?:≤|≤)?\d+\s*次(?:/(?:章|500字|段|千字))?")
# Lines referencing common-rules (exempt from boundary checks)
REFERENCE_RE = re.compile(r"common-rules\.md")

# --- C5 banned terms/anti-patterns (audit 2026-08-13 section 3-C5, decision P2-10) ---
# The prompt structure is unified as "6 elements"; legacy terms are banned to prevent regression.
# Precise regexes: exclude legitimate hits such as "2-4 层" (conflict ladder) and opening-hooks.md (a file name).
BANNED_TERMS = [
    (re.compile(r"(?<![0-9-])4 层"), "Legacy term \"4 层\" (now unified as 6 elements)"),
    (re.compile(r"9 层"), "Legacy term \"9 层\" (now unified as 6 elements)"),
    (re.compile(r"任务层"), "Legacy term \"任务层\""),
    (re.compile(r"prompt 模块 5"), "Legacy term \"prompt 模块 5\""),
    (re.compile(r"\bGoals\b"), "Legacy field name \"Goals\" (renamed to 叙事目标)"),
    (re.compile(r"(?<!-)hooks\.md"), "Legacy file name \"hooks.md\""),
    (re.compile(r"genre_profile"), "Legacy field name \"genre_profile\" (read the selected type in settings/genre-setting.md)"),
]

# Anti-pattern sentence: after the audit correction records (prompt-crafting) and acceptance probes (prompt-audit) are cleaned up/exempted,
# any remaining occurrence counts as old wording returning
BANNED_ANTI_PATTERN = re.compile(r"叙事规则优先级高于所有约束")
# Acceptance probes list the old wording as a FAIL signal; that is a detector definition, so it is exempt
ANTI_PATTERN_EXEMPT = {"skills/prompt-audit.md"}

# Object-name normalization: take the first keyword, drop parentheses, slash groups, and enumeration lists
def norm_obj(raw: str) -> str:
    obj = raw.strip().replace("**", "")
    obj = re.sub(r"[（(].*?[)）]", "", obj)  # drop parentheses
    obj = obj.split("、")[0].split("/")[0].split(",")[0].strip()
    return obj


def extract_thresholds(text: str, path: Path) -> dict:
    """Extract {normalized object@unit: {number, line number, original text}}.

    Same file, same object, same unit: skip when the numbers match (repeats in quick-reference tables/body text are not a problem);
    when they differ, record the later one (intra-file conflicts must also surface).
    """
    found = {}
    lines = text.split("\n")
    for i, ln in enumerate(lines, 1):
        hit = None
        m = TBL_RE.match(ln) or TBL_LE_RE.match(ln) or TBL_SEN_RE.match(ln)
        if m:
            obj = norm_obj(m.group(1))
            if not obj or obj in ("规则", "疲劳词", "检测项"):
                continue
            hit = (obj, m.group(2), m.group(3))
        else:
            m2 = CODE_RE.search(ln)
            if m2:
                # Code-block format: the object comes from the previous line's "命中模式"
                obj = None
                for j in range(i - 2, i):
                    if j >= 1:
                        pm = re.search(r"命中模式[:：]\s*[\"“]?([^\"”|]+)", lines[j - 1])
                        if pm:
                            obj = norm_obj(pm.group(1))
                            break
                if not obj:
                    obj = f"L{i}"
                hit = (obj, m2.group(1), m2.group(2))
        if hit is None:
            continue
        obj, num_str, unit = hit
        key = f"{obj}@{unit}"
        num = int(num_str)
        if key not in found:
            found[key] = {"num": num, "line": i, "raw": ln.strip()[:70], "obj": obj}
        elif found[key]["num"] != num:
            # Same object with different numbers in one file: overwrite with the later one, so check_conflicts exposes it in the cross-file comparison
            found[key] = {"num": num, "line": i, "raw": ln.strip()[:70], "obj": obj,
                          "same_file_conflict": True}
    return found


def check_conflicts() -> list:
    errors = []
    auth_text = AUTHORITY.read_text(encoding="utf-8")
    auth = extract_thresholds(auth_text, AUTHORITY)

    for base, label in SCAN_GLOBS:
        for f in sorted(base.rglob("*.md")):
            if f == AUTHORITY:
                continue
            rel = f.relative_to(ROOT).as_posix()
            text = f.read_text(encoding="utf-8")
            found = extract_thresholds(text, f)
            for key, info in found.items():
                # The same object appears with different numbers in one file: an intra-file conflict, report directly
                if info.get("same_file_conflict"):
                    errors.append(
                        f"{rel}:{info['line']} threshold for \"{info['obj']}\" is {info['num']} occurrences, inconsistent with definitions elsewhere in this file (intra-file conflict)"
                    )
                    continue
                # Cross-file: same object and unit as the authoritative source but a different number means a conflict
                if key in auth and auth[key]["num"] != info["num"]:
                    errors.append(
                        f"{rel}:{info['line']} threshold for \"{info['obj']}\" is {info['num']} occurrences, conflicting with the authoritative source "
                        f"common-rules.md:{auth[key]['line']} value of {auth[key]['num']} occurrences"
                    )
    return errors


def check_boundary() -> list:
    errors = []
    for rel in METHODOLOGY_FILES:
        f = ROOT / rel
        if not f.exists():
            errors.append(f"{rel}: file does not exist (boundary check skipped)")
            continue
        text = f.read_text(encoding="utf-8")
        lines = text.split("\n")
        for i, ln in enumerate(lines, 1):
            # Lines referencing common-rules are exempt
            if REFERENCE_RE.search(ln):
                continue
            if ANY_COUNT_RE.search(ln):
                errors.append(
                    f"{rel}:{i} methodology/exemption file contains a quantity threshold: \"{ln.strip()[:50]}\""
                    f"(thresholds may only be defined in common-rules.md)"
                )
    return errors


def check_banned_terms() -> list:
    """C5 regression guard: legacy terms + anti-pattern sentences are banned from the injection side (agents/skills/knowledge)."""
    errors = []
    for base, label in SCAN_GLOBS:
        for f in sorted(base.rglob("*.md")):
            rel = f.relative_to(ROOT).as_posix()
            text = f.read_text(encoding="utf-8")
            for pat, desc in BANNED_TERMS:
                for m in pat.finditer(text):
                    line = text[:m.start()].count("\n") + 1
                    errors.append(f"{rel}:{line} found {desc} (banned to prevent regression; delete or rewrite)")
            if rel in ANTI_PATTERN_EXEMPT:
                continue
            for m in BANNED_ANTI_PATTERN.finditer(text):
                line = text[:m.start()].count("\n") + 1
                errors.append(f"{rel}:{line} found anti-pattern \"叙事规则优先级高于所有约束\""
                              f"(corrected to below layers 1-5; see the prompt-crafting conflict ruling table)")
    return errors


def main() -> int:
    all_errors = []
    all_errors += check_conflicts()
    all_errors += check_boundary()
    all_errors += check_banned_terms()

    for e in all_errors:
        print(f"  ❌ {e}")

    if all_errors:
        print(f"\n{len(all_errors)} problem(s) in total")
        return 1
    print("✅ Rule conflict check passed (no threshold conflicts, no boundary violations, no legacy terms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
