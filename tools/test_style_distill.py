#!/usr/bin/env python3
"""style-distiller LLM refactor verification script (template/flow/schema assertions; does not depend on exact LLM numbers).

Usage: python tools/test_style_distill.py
Exit code 0 = all passed (used by CI).

Coverage (spec section 10; the render/accept/reroll-decision parts live in tools/test_style_rules.py and are not repeated here):
- schema validity: check-agents card validation passes for main/scene card templates (including distributions summing to 100, and enums)
- 13-template methodology: all thirteen sections of feature-extract.md present + verify-checklist/rendering-rules exist, retired templates deleted
- Retirement cleanup: three tools deleted, no jieba in CI, no style-tool deployment in init/sync
- Reroll contract: rewrite_of/violations fields + no style-update-order leftovers (novel-agent/writer/dispatch docs) + writer does not use the card body-text four fields as its style source
- Dual states: undistilled template / distilled card / legacy jieba card all pass check_style_card (enhancement fields optional, validated only when present) + init templates keep locked (zero changes in the undistilled state)
"""
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from style_common import force_utf8
force_utf8()

from test_util import check, load_module, summary, exit_code

def test_feature_extract():
    t = (REPO / "knowledge/style-distill/prompt-templates/feature-extract.md").read_text(encoding="utf-8")
    for name in ["Template 1", "Template 2", "Template 3", "Template 4", "Template 5", "Template 6", "Template 7",
                 "Template 8", "Template 9", "Template 10", "Template 11", "Template 12", "Template 13", "Phase 1", "Phase 2", "Phase three"]:
        check(f"feature-extract contains {name}", name in t)
    # 13-template schema tokens (spec section 9: complete quantification-table keys, correct modeling-rule formats: sentence-card structural formula / dialogue-mode round sequence / rhythm-model key parameters / anchor-model chapter-opening/closing anchors)
    for token in ("quantification table", "structural formula", "round sequence",
                  "key\nparameters", "chapter beginning anchor", "chapter ending anchor point"):
        check(f"feature-extract contains schema token {token!r}", token in t)
    for f in ("rendering-rules.md", "verify-checklist.md"):
        check(f"{f} exists", (REPO / "knowledge/style-distill/prompt-templates" / f).exists())
    for gone in ("distill-prompt.md", "injection-template.md", "gate-g-checklist.md"):
        check(f"retired template {gone} deleted", not (REPO / "knowledge/style-distill/prompt-templates" / gone).exists())

def test_schema_templates():
    mod = load_module("check_agents", TOOLS / "check-agents.py")
    main_tpl = REPO / "templates/settings/writing-style.md"
    errs = mod.check_style_card(main_tpl)
    check("main card template passes card validation", not errs, "; ".join(errs))
    scenes = sorted((REPO / "templates/settings/style-profiles").glob("*.md"))
    check("scene card directory is non-empty", len(scenes) > 0, "style-profiles/ is empty, so validation would pass silently")   # review #49
    for scene in scenes:
        errs = mod.check_style_card(scene)
        check(f"scene card {scene.name} passes card validation", not errs, "; ".join(errs))

def test_retire_clean():
    for bad in ("tools/distill-style.py", "tools/compare-style.py", "tools/mix-style.py"):
        check(f"{bad} deleted", not (REPO / bad).exists())
    static = (REPO / ".github/workflows/static.yml").read_text(encoding="utf-8")
    check("no jieba in CI", "jieba" not in static)
    check("CI runs test_style_rules", "test_style_rules.py" in static)
    req = (REPO / "tools/requirements.txt").read_text(encoding="utf-8")
    check("no jieba in requirements", "jieba" not in req)
    init = (REPO / "tools/init.py").read_text(encoding="utf-8")
    check("no distill-style deployment in init", "distill-style.py" not in init)
    sync = (REPO / "tools/sync-project.py").read_text(encoding="utf-8")
    check("no _STYLE_TOOL_NAMES in sync", "_STYLE_TOOL_NAMES" not in sync)

def test_reroll_contract():
    for f in ("agents/novel-agent.md", "agents/writer.md", "skills/writing-execution.md", "skills/novel-dispatch.md"):
        t = (REPO / f).read_text(encoding="utf-8")
        check(f"{f} contains rewrite_of", "rewrite_of" in t)
        check(f"{f} contains violations", "violations" in t)
        check(f"{f} has no style-update-order", "style-update-order" not in t)
    writer_t = (REPO / "agents/writer.md").read_text(encoding="utf-8")
    check("writer does not use card body text as its style source",
          "写作风格方法论" not in writer_t and "depiction_techniques" not in writer_t
          and "possible_mistakes" not in writer_t)

def test_anti_ai_verify():
    skill = (REPO / "skills/anti-ai.md").read_text(encoding="utf-8")
    check("anti-ai contains instruction-following acceptance", "instruction following" in skill, "missing instruction-following wording")
    check("anti-ai contains case-2 acceptance", "Case 2" in skill, "missing Case 2 wording")
    check("anti-ai references verify-checklist", "verify-checklist" in skill, "missing verify-checklist reference")   # review #49: split the weak assertion
    check("anti-ai has no distill-style.py", "distill-style.py" not in skill)
    check("anti-ai has no gate-g-checklist", "gate-g-checklist" not in skill)

def test_dual_mode():
    import tempfile, yaml
    mod = load_module("check_agents", TOOLS / "check-agents.py")
    main_tpl = REPO / "templates/settings/writing-style.md"
    fm = yaml.safe_load(main_tpl.read_text(encoding="utf-8").split("---", 2)[1])
    # Undistilled state: zero template changes, confidence=0 passes validation (spec section 4)
    check("undistilled state (old template as-is) passes card validation", not mod.check_style_card(main_tpl))
    check("undistilled state confidence=0", fm.get("confidence") == 0, str(fm.get("confidence")))
    # Distilled card: original card structure plus voice layer + enhancement fields + confidence>0 passes validation
    fm["profile_name"] = "测试蒸馏卡"; fm["confidence"] = 75
    fm["lexicon"]["name_pronoun_ratio"] = {"name": 45, "he_she": 50, "i_you": 5}
    fm["rhetoric"]["metaphor_preference"] = {"weapon_metal": 5, "nature": 10, "body": 20, "abstract": 30, "other": 35}
    fm["rhetoric"]["sensory_dist"] = {"visual": 72, "auditory": 15, "tactile": 10, "olfactory": 2, "gustatory": 1}
    fm["emotion_expression"]["inner_monologue_pct"] = 35
    fm["verb_style"]["strength"] = "medium"
    fm["hard_constraints"] = ["内心独白必须用引号包裹"]
    fm["soft_guidance"] = ["整体基调：轻松吐槽向"]
    fm["few_shot_examples"] = [{"type": "inner_thought", "text": "好想死啊", "reason": "口头禅式吐槽"}]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "writing-style.md"
        p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
        errs = mod.check_style_card(p)
        check("distilled card (voice layer + enhancement fields + confidence>0) passes card validation", not errs, "; ".join(errs))
    # Legacy jieba distilled card: confidence>0, no voice layer/enhancement fields, passes validation (spec section 6.0b fallback compatibility)
    fm2 = yaml.safe_load(main_tpl.read_text(encoding="utf-8").split("---", 2)[1])
    fm2["confidence"] = 70
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "writing-style.md"
        p.write_text("---\n" + yaml.safe_dump(fm2, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
        errs = mod.check_style_card(p)
        check("legacy jieba card (confidence>0, no voice layer) passes card validation", not errs, "; ".join(errs))
    # init templates keep locked (zero changes in the undistilled state, no migration)
    init = (REPO / "tools/init.py").read_text(encoding="utf-8")
    check("init templates keep locked (zero changes in the undistilled state)", "locked" in init)
    # prompt-crafting dual-state branch (spec section 6: undistilled = body-text qualitative four-field injection unchanged / distilled = case-2 rendering)
    pc = (REPO / "skills/prompt-crafting.md").read_text(encoding="utf-8")
    check("prompt-crafting contains a confidence branch", "confidence" in pc)
    check("prompt-crafting keeps the undistilled qualitative injection section (Writing Style Constraints)", "Writing Style Constraints" in pc)
    check("prompt-crafting references rendering-rules (distilled rendering)", "rendering-rules" in pc)
    check("prompt-crafting references the Case 2 structure", "Case 2" in pc)

def test_unit_convergence():
    """Decision A fix: percentage fields are always 0-100 percentages (old-engine one-decimal percentages 13.4/2.31 pass;
    0.3 = 0.3%, no multiplying by 100; 1.5 is a legal percentage). Out-of-range values (>100) are rejected."""
    import tempfile, yaml
    mod = load_module("check_agents", TOOLS / "check-agents.py")
    base = REPO / "templates/settings/writing-style.md"

    fm = yaml.safe_load(base.read_text(encoding="utf-8").split("---", 2)[1])
    fm["confidence"] = 75
    fm["syntax"]["question_ratio"] = 13.4          # old-engine one-decimal percentage
    fm["syntax"]["exclamation_ratio"] = 7.2
    fm["syntax"]["single_sentence_paragraph_pct"] = 46.1
    fm["dialogue_style"]["subtext_ratio"] = 22.5
    fm["lexicon"]["name_pronoun_ratio"] = 2.31     # old-engine name/pronoun ratio
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "writing-style.md"
        p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
        errs = mod.check_style_card(p)
        check("decision A: old-engine 0-100 one-decimal percentage card passes validation", not errs, "; ".join(errs))

    fm2 = yaml.safe_load(base.read_text(encoding="utf-8").split("---", 2)[1])
    fm2["confidence"] = 75
    fm2["syntax"]["question_ratio"] = 150
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "writing-style.md"
        p.write_text("---\n" + yaml.safe_dump(fm2, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
        errs = mod.check_style_card(p)
        check("decision A: question_ratio=150 rejected (over 0-100)", any("question_ratio" in e for e in errs), errs)

    fm3 = yaml.safe_load(base.read_text(encoding="utf-8").split("---", 2)[1])
    fm3["confidence"] = 75
    fm3["dialogue_style"]["subtext_ratio"] = 1.5
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "writing-style.md"
        p.write_text("---\n" + yaml.safe_dump(fm3, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
        errs = mod.check_style_card(p)
        check("decision A: subtext_ratio=1.5 passes (1.5% is legal; the old engine can produce it)", not errs, "; ".join(errs))

def test_scalar_percent_validation():
    """Validation-side additions: single rhythm bucket >100, transition_sentence_ratio out of range, preferred_words type, self-inherits."""
    import tempfile, yaml
    mod = load_module("check_agents", TOOLS / "check-agents.py")
    base = REPO / "templates/settings/writing-style.md"

    def _check(card_mut, contains):
        fm = yaml.safe_load(base.read_text(encoding="utf-8").split("---", 2)[1])
        fm["confidence"] = 75
        card_mut(fm)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "writing-style.md"
            p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
            return mod.check_style_card(p)

    errs = _check(lambda fm: fm["rhythm"].update({"dialogue_pct": 110, "action_pct": 0, "environment_pct": 0, "inner_thought_pct": 0, "narration_pct": 0}), "rhythm")
    check("single rhythm bucket >100 rejected (dialogue_pct:110)", any("rhythm.dialogue_pct" in e for e in errs), errs)
    errs = _check(lambda fm: fm["cohesion"].update({"transition_sentence_ratio": 120}), "transition")
    check("transition_sentence_ratio>100 rejected", any("transition_sentence_ratio" in e for e in errs), errs)
    errs = _check(lambda fm: fm["lexicon"].update({"preferred_words": "好想死"}), "preferred")
    check("preferred_words rejected when not a list", any("preferred_words" in e for e in errs), errs)
    errs = _check(lambda fm: fm["lexicon"].update({"banned_words": "宛如"}), "banned")
    check("banned_words rejected when not a list", any("banned_words" in e for e in errs), errs)

    # self-referencing inherits is caught by single-card validation
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "writing-style.md"
        fm = yaml.safe_load(base.read_text(encoding="utf-8").split("---", 2)[1])
        fm["confidence"] = 75
        fm["scene_type"] = "dialogue"
        fm["override"] = {"syntax": {"avg_sentence_length": 12}}
        fm["inherits"] = "writing-style.md"
        p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
        errs = mod.check_style_card(p)
        check("self-referencing inherits rejected", any("self-referential" in e for e in errs), errs)

def test_inherits_cycle_detected():
    """Inheritance cycle (A to B to A) is caught by check_style_cards across files."""
    import tempfile, yaml
    mod = load_module("check_agents", TOOLS / "check-agents.py")
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        tpl = root / "templates" / "settings"
        tpl.mkdir(parents=True)
        (tpl / "writing-style.md").write_text("---\nprofile_version: '1.0'\nscene_type: general\nconfidence: 70\nlast_updated: ''\nsource_sample_length: 100\n---\n", encoding="utf-8")
        sp = tpl / "style-profiles"; sp.mkdir()
        fm_a = {"profile_version": "1.0", "scene_type": "dialogue", "confidence": 70, "last_updated": "", "source_sample_length": 100, "override": {}, "inherits": "b.md"}
        fm_b = {"profile_version": "1.0", "scene_type": "dialogue", "confidence": 70, "last_updated": "", "source_sample_length": 100, "override": {}, "inherits": "a.md"}
        (sp / "a.md").write_text("---\n" + yaml.safe_dump(fm_a, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
        (sp / "b.md").write_text("---\n" + yaml.safe_dump(fm_b, allow_unicode=True, sort_keys=False) + "---", encoding="utf-8")
        old_root = mod.ROOT
        mod.ROOT = root
        try:
            errs = mod.check_style_cards()
        finally:
            mod.ROOT = old_root
        check("A to B to A inheritance cycle caught", any("inherits cycle" in e for e in errs), errs)

def test_project_cards_skips_analysis():
    """check_project_cards excludes analysis/ (quantification table + modeling rules + author portrait, no frontmatter)
    to avoid false "style card missing frontmatter" reports."""
    import tempfile
    mod = load_module("check_agents", TOOLS / "check-agents.py")
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "settings" / "style-profiles" / "analysis").mkdir(parents=True)
        (root / "settings" / "style-profiles" / "analysis" / "general.md").write_text(
            "# 分析稿\n\n量化表全文……\n\n## 作者画像\n\n这是你的文风……\n", encoding="utf-8")
        (root / "settings" / "writing-style.md").write_text(
            "---\nprofile_version: '1.0'\nscene_type: general\nconfidence: 70\nlast_updated: ''\nsource_sample_length: 100\n---\n",
            encoding="utf-8")
        (root / "settings" / "style-profiles" / "dialogue.md").write_text(
            "---\nprofile_version: '1.0'\nscene_type: dialogue\nconfidence: 70\nlast_updated: ''\nsource_sample_length: 100\noverride: {}\n---\n",
            encoding="utf-8")
        errs = mod.check_project_cards(root)
        check("check_project_cards does not scan analysis/ (no false reports)",
              not any("general.md" in e for e in errs), errs)
        check("check_project_cards still validates real scene cards (dialogue)",
              not any("dialogue.md" in e for e in errs), errs)

def test_verify_doc_code_alignment():
    """#11 fix cross-assertions: verify-checklist.md wording matches style_verify.py code behavior.
    The doc's violation whitelist tokens (`` `true/是/yes/1/违反/违反了` ``) equal the code's VIOLATED_STRINGS;
    the doc's "其余字符串 → not violated" equals the code returning False for strings outside the whitelist, with trailing punctuation stripped (是。 to 是)."""
    import re
    import style_verify
    doc = (REPO / "knowledge/style-distill/prompt-templates/verify-checklist.md").read_text(encoding="utf-8")
    m = re.search(r"`([^`]+)` → violated", doc)
    check("verify-checklist contains a violation whitelist line", m is not None, "no `...` → violated wording found")
    if m:
        doc_tokens = set(m.group(1).split("/"))
        check("doc whitelist equals code VIOLATED_STRINGS",
              doc_tokens == set(style_verify.VIOLATED_STRINGS),
              f"doc={sorted(doc_tokens)} vs code={sorted(style_verify.VIOLATED_STRINGS)}")
    check("doc \"其余字符串 → not violated\" equals code behavior",
          style_verify._is_violated("其余字符串") is False and style_verify._is_violated("是。") is True,
          style_verify._is_violated("是。"))

def run_all():
    test_feature_extract(); test_schema_templates(); test_retire_clean()
    test_reroll_contract(); test_anti_ai_verify(); test_dual_mode(); test_unit_convergence()
    test_scalar_percent_validation(); test_inherits_cycle_detected()
    test_project_cards_skips_analysis()
    test_verify_doc_code_alignment()
    print(f"\n{summary()}")
    return exit_code()

if __name__ == "__main__":
    sys.exit(run_all())
