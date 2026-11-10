#!/usr/bin/env python3
"""Unit tests for style_render + style_verify rules (TDD Task 4, keep long-term).

Usage: python tools/test_style_rules.py
Exit code 0 = all passed.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from style_common import force_utf8
force_utf8()

from style_render import range_for, enum_zh, pct_zh, _pct, _num, _flatten_dists, render_card, SCENE_INJECTION
from style_verify import verdict, should_reroll, pick_best, format_report, _is_violated, _violated_count, VIOLATED_STRINGS
from test_util import check, summary, exit_code

CARD = {
    "profile_version": "1.0", "profile_name": "测试卡", "scene_type": "general",
    "source_sample_length": 5000, "confidence": 75, "last_updated": "2026-08-11",
    "lexicon": {"adj_density_per_100": 5.8, "adv_density_per_100": 3.5,
                "four_phrase_freq_per_100": 1.8, "preferred_words": ["好想死"], "banned_words": ["宛如"],
                "name_pronoun_ratio": {"name": 45, "he_she": 50, "i_you": 5}},
    "syntax": {"avg_sentence_length": 16, "sentence_length_dist": {"short_le_8": 38, "medium_9_20": 45, "long_21_35": 14, "xlong_gt_35": 3},
               "single_sentence_paragraph_pct": 38, "avg_sentences_per_paragraph": 2.2, "question_ratio": 13, "exclamation_ratio": 7},
    "rhythm": {"dialogue_pct": 48, "action_pct": 16, "environment_pct": 6, "inner_thought_pct": 25, "narration_pct": 5},
    "rhetoric": {"metaphor_density_per_100": 1.2, "metaphor_preference": {"weapon_metal": 5, "nature": 10, "body": 20, "abstract": 30, "other": 35},
                 "sensory_dist": {"visual": 72, "auditory": 15, "tactile": 10, "olfactory": 2, "gustatory": 1}},
    "emotion_expression": {"direct_pct": 15, "action_physiology_pct": 45, "environment_projection_pct": 5, "inner_monologue_pct": 35},
    "narrative": {"perspective": "third_limited", "focal_character": "贺天然", "inner_monologue_style": "direct"},
    "dialogue_style": {"tag_style": "mixed", "avg_dialogue_length": 12, "interrupt_freq_per_100": 6, "subtext_ratio": 22},
    "cohesion": {"conjunction_freq_per_100": 2.6, "transition_sentence_ratio": 4, "paragraph_bridge_style": "action"},
    "verb_style": {"action_verb_ratio": 35, "mental_verb_ratio": 40, "state_verb_ratio": 25, "strength": "medium"},
    "hard_constraints": ["内心独白必须用引号包裹"],
    "soft_guidance": ["整体基调：轻松吐槽向"],
    "few_shot_examples": [{"type": "inner_thought", "text": "好想死啊", "reason": "口头禅式吐槽"}],
}

def test_range_for():
    check("5.8@75 → '5-6'", range_for(5.8, 75) == "5-6", range_for(5.8, 75))
    check("16@75 → '14-18'", range_for(16, 75) == "14-18", range_for(16, 75))
    check("5.8@50 → wider range '5-7' (±20%)", range_for(5.8, 50) == "5-7", range_for(5.8, 50))
    check("5.8@90 → '5-6'(±10%)", range_for(5.8, 90) == "5-6", range_for(5.8, 90))
    check("zero value → '0' (no invented 0-1)", range_for(0, 75) == "0", range_for(0, 75))
    check("very low value 0.2@75 → '0' (single value)", range_for(0.2, 75) == "0", range_for(0.2, 75))
    check("5@75 → '5-6' (half-up, not banker's rounding to 4)", range_for(5, 75) == "5-6", range_for(5, 75))
    check("15@75 → '14-17' (half-up boundary)", range_for(15, 75) == "14-17", range_for(15, 75))
    check("25@75 → '23-28' (half-up boundary)", range_for(25, 75) == "23-28", range_for(25, 75))
    check("_num(True) → 0 (bool excluded)", _num(True) == 0, _num(True))
    check("_num(nan) → 0 (non-finite filtered)", _num(float("nan")) == 0, _num(float("nan")))
    check("_num(inf) → 0", _num(float("inf")) == 0, _num(float("inf")))

def test_enum_zh():
    check("mixed → '标签混合使用'", enum_zh("tag_style", "mixed") == "标签混合使用", enum_zh("tag_style", "mixed"))
    check("pure_tags → \"标签用'XX说'为主\"", enum_zh("tag_style", "pure_tags") == "标签用'XX说'为主", enum_zh("tag_style", "pure_tags"))
    check("medium → '动词力度中等'", enum_zh("strength", "medium") == "动词力度中等", enum_zh("strength", "medium"))
    check("action → '段落靠动作衔接'", enum_zh("paragraph_bridge_style", "action") == "段落靠动作衔接", enum_zh("paragraph_bridge_style", "action"))
    check("direct → '内心独白用引号直接呈现'", enum_zh("inner_monologue_style", "direct") == "内心独白用引号直接呈现", enum_zh("inner_monologue_style", "direct"))
    check("unknown value falls back to the original", enum_zh("strength", "???") == "???", enum_zh("strength", "???"))

def test_pct_zh():
    check("48 → '近一半'", pct_zh(48) == "近一半", pct_zh(48))
    check("88 → '绝大多数'", pct_zh(88) == "绝大多数", pct_zh(88))

def test_scene_injection():
    check("dialogue scene contains dialogue_style", "dialogue_style" in SCENE_INJECTION["dialogue"], SCENE_INJECTION.get("dialogue"))
    check("fight scene contains verb_style", "verb_style" in SCENE_INJECTION["fight"], SCENE_INJECTION.get("fight"))

def test_render_card():
    out = render_card(CARD)
    check("produces the 【句式】 section", "句式" in out and any("平均句长" in x for x in out["句式"]), out.get("句式"))
    check("produces the 【词汇】 section with a density range", any("每百字 5-6" in x for x in out["词汇"]), out.get("词汇"))
    check("produces the 【对话风格】 section", "对话风格" in out, list(out))
    check("硬性规则 passed through item by item", any("引号包裹" in x for x in out["硬性规则"]), out.get("硬性规则"))
    check("风格参考例句 passed through grouped", any("inner_thought" in x for x in out["风格参考例句"]), out.get("风格参考例句"))

def test_render_card_verb():
    out = render_card(CARD)
    check("general renders verb strength", any("力度中等" in x for x in out["句式"]), out.get("句式"))
    check("general renders verb ratios", any("动作 35%" in x for x in out["句式"]), out.get("句式"))

def test_render_card_sparse():
    out = render_card(CARD, "dialogue")
    check("dialogue scene injects 词汇", bool(out.get("词汇")), out.get("词汇"))
    check("dialogue scene injects 对话风格", bool(out.get("对话风格")), out.get("对话风格"))
    check("dialogue scene has no 句式", not out.get("句式"), out.get("句式"))
    check("dialogue scene has no 节奏", not out.get("节奏"), out.get("节奏"))

def test_render_card_fallback():
    legacy = dict(CARD)
    legacy["lexicon"] = dict(CARD["lexicon"])
    legacy["lexicon"]["name_pronoun_ratio"] = 55                      # old jieba card single value
    legacy["emotion_expression"] = {k: v for k, v in CARD["emotion_expression"].items() if k != "inner_monologue_pct"}
    lo = render_card(legacy)
    check("single-value npr renders as a ratio", any("人名/代词使用比例 55%" in x for x in lo["词汇"]), lo.get("词汇"))
    check("missing inner_monologue_pct does not inject that sub-item", not any("内心独白" in x for x in lo["情绪表达"]), lo.get("情绪表达"))

def test_pct_normalize():
    # Decision A fix: 0-100 percentage semantics, no 0-1 fraction x100 assumption (the old engine produced 0-100 one-decimal percentages)
    check("13.4 → 13.4 (old-engine one-decimal percentage)", _pct(13.4) == 13.4, _pct(13.4))
    check("0.30 → 0.3 (low percentage, no x100)", _pct(0.30) == 0.3, _pct(0.30))
    check("0.99 → 0.99", _pct(0.99) == 0.99, _pct(0.99))
    check("2.31 → 2.31 (old-engine name/pronoun ratio)", _pct(2.31) == 2.31, _pct(2.31))
    check("integer 23 stays 23", _pct(23) == 23, _pct(23))
    check("23.0 → 23 (integer values converge to int)", _pct(23.0) == 23, _pct(23.0))
    check("0 → 0", _pct(0) == 0, _pct(0))
    check("string '13.4' → 13.4", _pct("13.4") == 13.4, _pct("13.4"))
    check("None → None (missing keys do not fake a 0)", _pct(None) is None, _pct(None))
    check("illegal string → None", _pct("abc") is None, _pct("abc"))
    check("out-of-range 150 → None (render side skips the line, does not clamp to 0)", _pct(150) is None, _pct(150))
    check("negative -5 → None", _pct(-5) is None, _pct(-5))
    check("bool True → None (bool excluded)", _pct(True) is None, _pct(True))

def test_render_percent_normalize():
    # Decision A fix: old-engine 0-100 one-decimal percentages render as-is (13.4%), no x100
    legacy = dict(CARD)
    legacy["syntax"] = dict(CARD["syntax"])
    legacy["syntax"]["question_ratio"] = 13.4
    legacy["syntax"]["exclamation_ratio"] = 7.2
    legacy["dialogue_style"] = dict(CARD["dialogue_style"])
    legacy["dialogue_style"]["subtext_ratio"] = 22.5
    lo = render_card(legacy)
    check("old percentage question_ratio 13.4 → 13.4% (少量)", any("疑问句占比：13.4%（少量）" in x for x in lo["句式"]), lo.get("句式"))
    check("old percentage exclamation_ratio 7.2 → 7.2%", any("感叹句占比：7.2%" in x for x in lo["句式"]), lo.get("句式"))
    check("old percentage subtext_ratio 22.5 → 22.5%", any("潜台词占比：22.5%" in x for x in lo["对话风格"]), lo.get("对话风格"))
    out = render_card(CARD)
    check("integer question_ratio 13 → renders 13% (少量)", any("疑问句占比：13%（少量）" in x for x in out["句式"]), out.get("句式"))
    check("integer subtext_ratio 22 → renders 22%", any("潜台词占比：22%" in x for x in out["对话风格"]), out.get("对话风格"))
    check("density fields are not normalized by _pct (X per hundred characters)", any("每百字 5-6" in x for x in out["词汇"]), out.get("词汇"))

def test_render_percent_all_fields_consistent():
    # All scalar percentage fields display uniformly as 0-100 (old-engine one-decimal percentages are neither multiplied by 100 nor swallowed as-is)
    legacy = dict(CARD)
    legacy["lexicon"] = dict(CARD["lexicon"]); legacy["lexicon"]["name_pronoun_ratio"] = 2.31   # old-engine name/pronoun ratio
    legacy["syntax"] = dict(CARD["syntax"]); legacy["syntax"]["single_sentence_paragraph_pct"] = 46.1
    legacy["rhythm"] = dict(CARD["rhythm"]); legacy["rhythm"]["dialogue_pct"] = 48.2
    legacy["emotion_expression"] = dict(CARD["emotion_expression"])
    legacy["emotion_expression"]["direct_pct"] = 15.1; legacy["emotion_expression"]["inner_monologue_pct"] = 34.8
    legacy["verb_style"] = dict(CARD["verb_style"]); legacy["verb_style"]["action_verb_ratio"] = 35.4
    lo = render_card(legacy)
    check("single-sentence paragraphs 46.1 → 46.1%", any("单句段占比 ≥ 46.1%" in x for x in lo["句式"]), lo.get("句式"))
    check("dialogue 48.2 → 48.2% (近一半)", any("对话约 48.2%（近一半）" in x for x in lo["节奏"]), lo.get("节奏"))
    check("direct statements 15.1 → 15.1%", any("直接陈述 15.1%" in x for x in lo["情绪表达"]), lo.get("情绪表达"))
    check("inner monologue 34.8 → 34.8%", any("内心独白 34.8%" in x for x in lo["情绪表达"]), lo.get("情绪表达"))
    check("verb action 35.4 → 35.4%", any("动作 35.4%" in x for x in lo["句式"]), lo.get("句式"))
    check("transition sentences 4 → 4% (cohesion render fills it in)", any("过渡句占比：4%" in x for x in lo["衔接"]), lo.get("衔接"))
    check("name ratio 2.31 → 2.31 (no x100)", any("人名/代词使用比例 2.31" in x for x in lo["词汇"]), lo.get("词汇"))

def test_render_density_skip_unmeasured():
    # Missing density key means unmeasured, so do not inject (prevents "or 0" treating unmeasured as a measured 0)
    sparse = dict(CARD)
    sparse["lexicon"] = dict(CARD["lexicon"])
    sparse["lexicon"].pop("adj_density_per_100")
    out = render_card(sparse)
    check("missing adjective-density key is not injected", not any("形容词密度" in x for x in out["词汇"]), out.get("词汇"))
    check("adverb density still present", any("副词密度：每百字 3-4" in x for x in out["词汇"]), out.get("词汇"))

def test_render_override_guard():
    # Unmerged scene card (override-only) raises a clear error, preventing silent all-zero rendering (spec section 6.3)
    scene = {"confidence": 75, "scene_type": "dialogue",
             "override": {"lexicon": {"adj_density_per_100": 5.8}, "dialogue_style": {"subtext_ratio": 22}},
             "inherits": "writing-style.md"}
    try:
        render_card(scene, "dialogue")
        check("unmerged scene card should raise ValueError", False, "no raise")
    except ValueError:
        check("unmerged scene card raises ValueError", True)

def test_flatten_dists_clean():
    check("negative bucket dropped", _flatten_dists({"short_le_8": -5}) == [], _flatten_dists({"short_le_8": -5}))
    check("illegal string bucket dropped", _flatten_dists({"short_le_8": "abc"}) == [], _flatten_dists({"short_le_8": "abc"}))
    check("string numbers converge ('35' → 35%)", _flatten_dists({"short_le_8": "35"}) == ["短句（≤8字）占比 35%"], _flatten_dists({"short_le_8": "35"}))
    check("legal 0.5 bucket kept", _flatten_dists({"short_le_8": 0.5}) == ["短句（≤8字）占比 0.5%"], _flatten_dists({"short_le_8": 0.5}))
    check("nan bucket dropped", _flatten_dists({"short_le_8": float("nan")}) == [], _flatten_dists({"short_le_8": float("nan")}))

def test_verify_string_bool():
    # #11 fix: string boolean convergence; strip trailing punctuation, then match against the whitelist (是。 to 是); anything outside the whitelist counts as not violated
    check("'是。' → violated", _is_violated("是。") is True, _is_violated("是。"))
    check("'违反。' → violated", _is_violated("违反。") is True, _is_violated("违反。"))
    check("'true。' → violated", _is_violated("true。") is True, _is_violated("true。"))
    check("'yes。' → violated", _is_violated("yes。") is True, _is_violated("yes。"))
    check("'是！' → violated", _is_violated("是！") is True, _is_violated("是！"))
    check("'YES' → violated", _is_violated("YES") is True, _is_violated("YES"))
    check("'否。' → not violated", _is_violated("否。") is False, _is_violated("否。"))
    check("'false' → not violated", _is_violated("false") is False, _is_violated("false"))
    check("'其余字符串' → not violated", _is_violated("其余字符串") is False, _is_violated("其余字符串"))
    check("None → not violated", _is_violated(None) is False, _is_violated(None))
    check("bool True/False as-is", _is_violated(True) is True and _is_violated(False) is False)
    check("'违反了' → violated (whitelist + 了)", _is_violated("违反了") is True, _is_violated("违反了"))
    check("'是；' → violated (semicolon stripped)", _is_violated("是；") is True, _is_violated("是；"))
    check("'违反；。' → violated", _is_violated("违反；。") is True, _is_violated("违反；。"))
    check("VIOLATED_STRINGS is the doc whitelist of 6 tokens", VIOLATED_STRINGS == frozenset({"true", "是", "yes", "1", "违反", "违反了"}))

def test_verify_verdict():
    ok = [{"no": 1, "require": "禁'宛如'", "evidence": "无", "violated": False}]
    bad = [{"no": 1, "require": "禁'宛如'", "evidence": "出现1次", "violated": True}]
    check("no violations → PASS", verdict(ok) == "PASS", verdict(ok))
    check("violations → FAIL", verdict(bad) == "FAIL", verdict(bad))

def test_verify_reroll():
    check("round 1 with violations → rewrite", should_reroll(1, 2) is True)
    check("round 3 with violations → no rewrite", should_reroll(3, 2) is False)
    check("no violations → no rewrite", should_reroll(1, 0) is False)

def test_verify_pick_best():
    rounds = [{"round": 1, "violated": 3}, {"round": 2, "violated": 1}, {"round": 3, "violated": 1}]
    check("pick the fewest violations", pick_best(rounds)["violated"] == 1, pick_best(rounds))
    check("latest on ties", pick_best(rounds)["round"] == 3, pick_best(rounds))

def test_verify_pick_best_coerce():
    # String-count convergence (the LLM may output "3"): mixed int/str does not crash, all-str picks by value (not lexicographic order)
    check("mixed int/str does not crash and picks correctly", pick_best([{"violated": 3}, {"violated": "1"}])["violated"] in (1, "1"))
    check("all strings pick the fewest by value (10 vs 3 → 3)", pick_best([{"violated": "10"}, {"violated": "3"}])["violated"] == "3")
    check("None violated → 0 (a None round counts as 0 violations)", pick_best([{"violated": None}, {"violated": 2}])["violated"] is None)

def test_verify_count_coerce():
    # Convergence behavior (previously untested because of an always-true assertion): '3.0' counts as 3, True does not count as 1, illegal to 0
    check("'3.0' → 3 (not 0)", _violated_count("3.0") == 3, _violated_count("3.0"))
    check("'10' → 10", _violated_count("10") == 10, _violated_count("10"))
    check("2.0 → 2", _violated_count(2.0) == 2, _violated_count(2.0))
    check("True → 0 (bool is not a count)", _violated_count(True) == 0, _violated_count(True))
    check("None → 0", _violated_count(None) == 0, _violated_count(None))
    check("'abc' → 0", _violated_count("abc") == 0, _violated_count("abc"))
    check("nan → 0", _violated_count(float("nan")) == 0, _violated_count(float("nan")))
    check("'3.0' round vs 2 round → pick the 2 round", pick_best([{"violated": "3.0"}, {"violated": 2}])["violated"] == 2)
    check("True round → 0 violations, selected", pick_best([{"violated": True}, {"violated": 2}])["violated"] is True)

def test_verify_report():
    r = format_report([{"no": 1, "require": "禁'宛如'", "evidence": "出现1次", "violated": True, "advice": "替换"}])
    check("contains the header", "原文要求" in r, r)
    check("contains the FAIL conclusion and summary", "FAIL" in r and "1/1" in r, r)

def test_render_missing_keys_no_fake_zero():
    # Missing key means unmeasured, so the line is not rendered (prevents fake measured values like "average sentence length: 0 characters")
    sparse = dict(CARD)
    for k in ("syntax", "rhythm", "emotion_expression", "dialogue_style"):
        sparse[k] = {}
    sparse["lexicon"] = dict(CARD["lexicon"])
    sparse["lexicon"]["name_pronoun_ratio"] = None
    out = render_card(sparse)
    checks = [
        ("句式 has no fake 0 lines", not any("0 字" in x or "0 句" in x or "≥ 0%" in x or "疑问句占比" in x or "感叹句占比" in x for x in out["句式"]), out.get("句式")),
        ("节奏 has no fake 0 lines", not out["节奏"], out.get("节奏")),
        ("情绪表达 has no fake 0 lines", not out["情绪表达"], out.get("情绪表达")),
        ("对话风格 has no fake 0 lines", not out["对话风格"], out.get("对话风格")),
        ("missing npr does not render the name/pronoun line", not any("人名/代词" in x for x in out["词汇"]), out.get("词汇")),
    ]
    for name, cond, detail in checks:
        check(name, cond, detail)

def test_render_out_of_range_skips_line():
    # Out-of-range values (hallucinated 150%) skip the line instead of rendering fake measured "0% (少量)"
    bad = dict(CARD)
    bad["syntax"] = dict(CARD["syntax"]); bad["syntax"]["question_ratio"] = 150
    bad["lexicon"] = dict(CARD["lexicon"]); bad["lexicon"]["name_pronoun_ratio"] = 250
    out = render_card(bad)
    check("150% question-ratio line skipped", not any("疑问句占比" in x for x in out["句式"]), out.get("句式"))
    check("250 npr line skipped", not any("人名/代词" in x for x in out["词汇"]), out.get("词汇"))

def test_render_few_shot_grouping():
    # Group by type (spec render step 6); mark missing text/reason as "（未填写）" instead of None
    fse_card = dict(CARD)
    fse_card["few_shot_examples"] = [
        {"type": "inner_thought", "text": "好想死啊", "reason": "口头禅式吐槽"},
        {"type": "inner_thought", "text": "又来了"},
        {"type": "dialogue", "text": "关我屁事。", "reason": "呛人"},
        {"type": None},
        {"text": "裸串"},
    ]
    out = render_card(fse_card)
    lines = out["风格参考例句"]
    check("no literal None", all("None" not in x for x in lines), lines)
    check("same type merges into one line", len(lines) == 3, lines)
    check("inner_thought line contains two examples", any(x.startswith("[inner_thought]") and "好想死啊" in x and "又来了" in x for x in lines), lines)
    check("missing text/reason marked （未填写）", any("（未填写）" in x for x in lines), lines)
    check("non-dict examples group under 未标注", any(x.startswith("[未标注]") and "裸串" in x for x in lines), lines)

def test_render_conf_zero():
    # conf=0: quantitative dimensions are not rendered (prevents fake 0-1 ranges); only the voice layer passes through, plus a note line
    zero = dict(CARD); zero["confidence"] = 0
    out = render_card(zero)
    quant = ["词汇", "句式", "节奏", "修辞与感官", "情绪表达", "对话风格", "衔接", "视角"]
    check("conf=0 quantitative sections all empty", all(not out[s] for s in quant), {s: out[s] for s in quant})
    check("conf=0 contains the undistilled note line", any("未蒸馏卡" in x for x in out["硬性规则"]), out.get("硬性规则"))
    check("conf=0 voice layer passes through", any("引号包裹" in x for x in out["硬性规则"]), out.get("硬性规则"))

BODY = """## 叙事身份（原 role）

冷硬汉派刑警

## 硬约束（原 core_principles）

- 不写内心戏

## AI 易犯错误（原 possible_mistakes）

- 堆形容词

## 描写层次和手法（原 depiction_techniques）

- 先动作后环境

## few-shot 例句

- 蒸馏后填入
"""

def test_render_sound_layer_fallback():
    # Section 6.0b: a distilled card missing its voice layer falls back to the four body-text qualitative fields
    legacy = dict(CARD)
    legacy.pop("hard_constraints"); legacy.pop("soft_guidance"); legacy.pop("few_shot_examples")
    out = render_card(legacy, body=BODY)
    check("硬性规则 falls back to body-text 硬约束 + AI 易犯错误",
          any("不写内心戏" in x for x in out["硬性规则"]) and any("堆形容词" in x for x in out["硬性规则"]),
          out.get("硬性规则"))
    check("整体基调 falls back to body-text 叙事身份", any("冷硬汉派刑警" in x for x in out["整体基调"]), out.get("整体基调"))
    check("风格参考例句 falls back to 描写层次", any("先动作后环境" in x for x in out["风格参考例句"]), out.get("风格参考例句"))
    # Without body text: the voice layer stays empty and nothing crashes
    out2 = render_card(legacy)
    check("voice layer empty without a body", not out2["硬性规则"] and not out2["整体基调"] and not out2["风格参考例句"],
          {k: out2[k] for k in ("硬性规则", "整体基调", "风格参考例句")})
    # Partially missing: only fall back for the missing keys
    part = dict(CARD); part.pop("hard_constraints")
    out3 = render_card(part, body=BODY)
    check("partially missing falls back only for 硬性规则", any("不写内心戏" in x for x in out3["硬性规则"]) and any("整体基调：轻松吐槽向" in x for x in out3["整体基调"]),
          out3.get("硬性规则"))

test_range_for(); test_enum_zh(); test_pct_zh(); test_scene_injection()
test_render_card(); test_render_card_verb(); test_render_card_sparse(); test_render_card_fallback()
test_pct_normalize(); test_render_percent_normalize(); test_render_percent_all_fields_consistent()
test_render_density_skip_unmeasured(); test_render_override_guard(); test_flatten_dists_clean()
test_render_missing_keys_no_fake_zero(); test_render_out_of_range_skips_line()
test_render_few_shot_grouping(); test_render_conf_zero(); test_render_sound_layer_fallback()
test_verify_verdict(); test_verify_reroll(); test_verify_pick_best(); test_verify_pick_best_coerce()
test_verify_count_coerce(); test_verify_report(); test_verify_string_bool()
print(f"\n{summary()}")
sys.exit(exit_code())
