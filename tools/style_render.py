#!/usr/bin/env python3
"""style-distiller LLM refactor: rendering rules module (card to case-2 prompt).

Pure data + pure functions, no LLM calls:
- RANGE_TIERS: confidence to density-value range formulas (spec section 6.1a)
- ENUM_ZH: category enum to Chinese rendering map (spec section 6.2)
- pct_zh: percentage to Chinese qualitative label (spec section 6.1a percentage class)
- SCENE_INJECTION: scene sparse-injection matrix (spec section 6.3)
- render_card: card to case-2 rendered items per section (prompt-crafter references read-only; tests import directly)

Usage: python tools/style_render.py --card settings/writing-style.md
Exit codes: 0 = success; 2 = card missing frontmatter.
"""
from __future__ import annotations

import argparse
import math
import sys

from style_common import force_utf8, split_frontmatter, SCENE_INJECTION

force_utf8()

# 0) Numeric defense: the LLM or hand-edited YAML may write numbers as strings/bool/nan/inf; the rendering side converges them uniformly (spec says card values should be numeric)
def _num(v, default: float = 0.0) -> float:
    """String/numeric to float; None/bool/nan/inf/illegal to default. Purely defensive, never raises."""
    if v is None or isinstance(v, bool):
        return default
    if isinstance(v, (int, float)):
        f = float(v)
        return f if math.isfinite(f) else default
    if isinstance(v, str):
        try:
            f = float(v.strip())
        except ValueError:
            return default
        return f if math.isfinite(f) else default
    return default

# 1) Density ranges: confidence to ±% (spec 6.1a)
RANGE_TIERS = [(70, 0.10), (50, 0.20), (0, 0.30)]

def range_for(value: float, confidence: int) -> str:
    """5.8 @ 75 to '5-6' (X times (1±tier), rounded half-up to integers). value/confidence strings also converge to numbers."""
    value = _num(value)
    confidence = int(_num(confidence))
    tier = 0.30
    for floor, t in RANGE_TIERS:
        if confidence >= floor:
            tier = t
            break
    # half-up: round() is banker's rounding (round(4.5)=4), so card values 5/15/25 would be off by 1
    lo = max(0, math.floor(value * (1 - tier) + 0.5))
    hi = math.floor(value * (1 + tier) + 0.5)
    if hi <= lo:
        return str(lo)   # zero/very low values: a single value (0 items / 0 characters), never invent a non-zero range (prevents fake measured values like "0-1 per hundred characters")
    return f"{lo}-{hi}"

# 2) Category enums to Chinese (spec 6.2, verbatim alignment)
ENUM_ZH = {
    "tag_style": {
        "pure_tags": "标签用'XX说'为主", "mixed": "标签混合使用", "no_tags": "不用标签，动作替代"},
    "strength": {"weak": "动词力度轻", "medium": "动词力度中等", "strong": "动词力度烈"},
    "paragraph_bridge_style": {"action": "段落靠动作衔接", "dialogue": "靠对话衔接", "transition": "少用过渡句"},
    "inner_monologue_style": {"direct": "内心独白用引号直接呈现", "indirect": "间接转述"},
    "perspective": {"first_person": "第一人称", "second_person": "第二人称",
                    "third_limited": "第三人称有限视角", "third_omniscient": "第三人称全知视角"},
}

def enum_zh(key: str, value: str) -> str:
    return ENUM_ZH.get(key, {}).get(value, str(value))

# 3) Percentages to Chinese qualitative labels (spec 6.1a)
def pct_zh(value: float) -> str:
    value = _num(value)
    if value >= 80: return "绝大多数"
    if value >= 60: return "大部分"
    if value >= 40: return "近一半"
    if value >= 20: return "一部分"
    return "少量"

def _pct(v, default=None):
    """Percentage/ratio field unit convergence (spec decision A fix): always display as 0-100 percentages, never multiply by 100.

    The old jieba engine (distill-style.py) produced 0-100 percentages with one decimal place from round(100*x/n,1) (e.g. 13.4),
    and never produced 0-1 fractions; so 0<v<1 counts as a legal low percentage (0.3 = 0.3%), removing the old x100 error that misread 0.3 as 30%.

    Missing key/None/illegal/out-of-range (<0 or >100) to default (None): the caller skips that line instead of faking "0% (少量)".
    Applies to all scalar percentage fields (question/exclamation/subtext/single-sentence paragraphs/five-layer rhythm/emotion pct/verb ratios/transition sentences/name_pronoun single values).
    Distribution buckets (sentence_length_dist etc., where 0.5 as a bucket is legal = 0.5%) and density fields (X per hundred characters) must not use it."""
    v = _num(v, None)
    if v is None or v < 0 or v > 100:
        return default
    return int(v) if float(v).is_integer() else v

# 4) Scene sparse-injection matrix (spec 6.3); SCENE_INJECTION is single-sourced in style_common (review #36)

# 5) Card to case-2 rendered items per section
def _flatten_dists(d: dict) -> list[str]:
    """Distributions such as sentence_length_dist to per-threshold items. Numeric convergence: strings to numbers; zero/negative/nan/inf dropped (a legal 0.5 bucket is kept)."""
    zh = {"short_le_8": "短句（≤8字）", "medium_9_20": "中句（9-20字）",
          "long_21_35": "长句（21-35字）", "xlong_gt_35": "超长句（>35字）",
          "weapon_metal": "兵器金属", "nature": "自然", "body": "身体", "abstract": "抽象", "other": "其他",
          "visual": "视觉", "auditory": "听觉", "tactile": "触觉", "olfactory": "嗅觉", "gustatory": "味觉",
          "name": "人名", "he_she": "他/她", "i_you": "我/你"}
    out = []
    for k, v in d.items():
        v = _num(v)
        if v <= 0:
            continue
        out.append(f"{zh.get(k, k)}占比 {v:g}%")
    return out

def render_card(card: dict, scene_type: str = "general", body: str = "") -> dict[str, list[str]]:
    """Card to case-2 rendered items per section. body is the card body text (used for the section 6.0b voice-layer fallback); without it the fallback does not apply.
    Missing keys/out-of-range values mean unmeasured, so the line is not rendered (prevents fake measured values like "average sentence length: 0 characters")."""
    conf = int(_num(card.get("confidence")))
    out: dict[str, list[str]] = {k: [] for k in
        ["词汇", "句式", "节奏", "修辞与感官", "情绪表达", "对话风格", "衔接", "视角",
         "硬性规则", "整体基调", "风格参考例句"]}
    if not conf:
        # Undistilled cards (confidence=0): all quantitative dimensions are zero, and rendering a 0-1 range would mislead; per spec they should use the four body-text qualitative fields instead,
        # so here only the voice layer is passed through with a note, and no false quantitative ranges are produced.
        _sound_layer(out, card)
        out["硬性规则"].insert(0, "（未蒸馏卡：量化维未填充，请按正文定性四字段注入，不走案例 2 渲染）")
        return out
    dims = SCENE_INJECTION.get(scene_type, SCENE_INJECTION["general"])   # sparse injection (spec 6.3)

    # Scene-card guard (spec section 6.3): a card with an unmerged override (the style-distill on-disk shape) raises a clear error, preventing silent all-zero rendering
    if "override" in card and not any(d in card for d in SCENE_INJECTION["general"]):
        raise ValueError(
            "render_card received an unmerged scene card (it has override but no top-level 9 dimensions); stack the main card first"
            "(inherits parsing + override deep merge) and then render")

    # 词汇
    if "lexicon" in dims:
        lex = card.get("lexicon") or {}
        for _k, _zh in (("adj_density_per_100", "形容词密度"), ("adv_density_per_100", "副词密度"),
                        ("four_phrase_freq_per_100", "四字短语频率")):
            _v = lex.get(_k)
            if _v is not None:                                    # missing key/unmeasured: do not inject (in the old engine None meant unmeasured, unlike 0)
                out["词汇"].append(f"{_zh}：每百字 {range_for(_v, conf)} 个")
        pw = _as_list(lex.get("preferred_words"))                 # wrap a string as a single item to prevent splitting it character by character
        if pw:
            out["词汇"].append("偏好词：" + "、".join(pw))
        npr = lex.get("name_pronoun_ratio")
        if isinstance(npr, dict):
            out["词汇"].extend(_flatten_dists(npr))                       # three dimensions, bucket by bucket
        elif isinstance(npr, (int, float)):
            _npr = _pct(npr)                                              # single value to a 0-100 percentage; skip out-of-range/illegal values
            if _npr is not None:
                out["词汇"].append(f"人名/代词使用比例 {_npr}%")
    # 句式
    if "syntax" in dims:
        syn = card.get("syntax") or {}
        if syn.get("avg_sentence_length") is not None:
            out["句式"].append(f"平均句长：{range_for(syn['avg_sentence_length'], conf)} 字左右")
        sld = syn.get("sentence_length_dist")
        if isinstance(sld, dict):
            out["句式"].extend(_flatten_dists(sld))
        if (_ssp := _pct(syn.get('single_sentence_paragraph_pct'))) is not None:
            out["句式"].append(f"单句段占比 ≥ {_ssp}%")
        if syn.get('avg_sentences_per_paragraph') is not None:
            out["句式"].append(f"每段平均句数：{syn['avg_sentences_per_paragraph']} 句")
        if (_qr := _pct(syn.get('question_ratio'))) is not None:
            out["句式"].append(f"疑问句占比：{_qr}%（{pct_zh(_qr)}）")
        if (_er := _pct(syn.get('exclamation_ratio'))) is not None:
            out["句式"].append(f"感叹句占比：{_er}%")
        # verb_style merges into the sentence-style section (fight scenes are injected via SCENE_INJECTION; render only when present and legal)
        vs = card.get("verb_style") or {}
        if vs.get("strength"):
            out["句式"].append(enum_zh("strength", vs["strength"]))
        _vr = []
        for _k, _zh in (("action_verb_ratio", "动作"), ("mental_verb_ratio", "心理"), ("state_verb_ratio", "状态")):
            _v = _pct(vs.get(_k))
            if _v is not None:
                _vr.append(f"{_zh} {_v}%")
        if _vr:
            out["句式"].append("动词：" + " / ".join(_vr))
    # 节奏
    if "rhythm" in dims:
        rhy = card.get("rhythm") or {}
        if (_dp := _pct(rhy.get("dialogue_pct"))) is not None:
            out["节奏"].append(f"对话约 {_dp}%（{pct_zh(_dp)}）")
        _ac, _en = _pct(rhy.get('action_pct')), _pct(rhy.get('environment_pct'))
        if _ac is not None and _en is not None:
            out["节奏"].append(f"动作约 {_ac}%、环境约 {_en}%")
        _it, _na = _pct(rhy.get('inner_thought_pct')), _pct(rhy.get('narration_pct'))
        if _it is not None and _na is not None:
            out["节奏"].append(f"内心独白约 {_it}%、叙述约 {_na}%")
    # 修辞
    if "rhetoric" in dims:
        rhe = card.get("rhetoric") or {}
        _md = rhe.get("metaphor_density_per_100")
        if _md is not None:
            out["修辞与感官"].append(f"比喻密度：每百字 {range_for(_md, conf)} 个")
        mp = rhe.get("metaphor_preference")
        if isinstance(mp, dict):
            out["修辞与感官"].append("常用喻体：" + "、".join(_flatten_dists(mp)))
        sd = rhe.get("sensory_dist")
        if isinstance(sd, dict):
            out["修辞与感官"].append("感官通道：" + "、".join(_flatten_dists(sd)))
    # 情绪
    if "emotion_expression" in dims:
        emo = card.get("emotion_expression") or {}
        _dp2, _ap = _pct(emo.get('direct_pct')), _pct(emo.get('action_physiology_pct'))
        if _dp2 is not None and _ap is not None:
            out["情绪表达"].append(f"直接陈述 {_dp2}%、动作/生理 {_ap}%")
        if emo.get("inner_monologue_pct") is not None:                    # skip this sub-item when absent (spec 6.0b/4.1)
            _ep, _ip = _pct(emo.get('environment_projection_pct')), _pct(emo.get('inner_monologue_pct'))
            if _ep is not None and _ip is not None:
                out["情绪表达"].append(f"环境投射 {_ep}%、内心独白 {_ip}%")
        elif (_ep := _pct(emo.get('environment_projection_pct'))) is not None:
            out["情绪表达"].append(f"环境投射 {_ep}%")
    # 对话
    if "dialogue_style" in dims:
        dia = card.get("dialogue_style") or {}
        if dia.get("tag_style"):
            out["对话风格"].append(enum_zh("tag_style", dia["tag_style"]))
        if dia.get('avg_dialogue_length') is not None:
            out["对话风格"].append(f"平均对话长度：{range_for(dia['avg_dialogue_length'], conf)} 字")
        _if = dia.get('interrupt_freq_per_100')
        if _if is not None:
            out["对话风格"].append(f"打断频率：每百字 {range_for(_if, conf)} 次")
        if (_sr := _pct(dia.get('subtext_ratio'))) is not None:
            out["对话风格"].append(f"潜台词占比：{_sr}%")
    # 衔接
    if "cohesion" in dims:
        coh = card.get("cohesion") or {}
        _cf = coh.get('conjunction_freq_per_100')
        if _cf is not None:
            out["衔接"].append(f"连接词频率：每百字 {range_for(_cf, conf)} 次")
        if (_ts := _pct(coh.get('transition_sentence_ratio'))) is not None:   # declared by the spec; the render/verify side fills it in (review #22)
            out["衔接"].append(f"过渡句占比：{_ts}%")
        if coh.get("paragraph_bridge_style"):
            out["衔接"].append(enum_zh("paragraph_bridge_style", coh["paragraph_bridge_style"]))
    # 视角
    if "narrative" in dims:
        nar = card.get("narrative") or {}
        if nar.get("perspective"):
            out["视角"].append(enum_zh("perspective", nar["perspective"]))
        if nar.get("focal_character"):
            out["视角"].append(f"聚焦角色：{nar['focal_character']}")
        if nar.get("inner_monologue_style"):
            out["视角"].append(enum_zh("inner_monologue_style", nar["inner_monologue_style"]))
    _sound_layer(out, card, body)
    return out

def _sound_layer(out: dict[str, list[str]], card: dict, body: str = "") -> None:
    """Voice-layer passthrough: hard_constraints/soft_guidance/few_shot_examples are kept as-is (spec case-2 voice layer).
    When a distilled card lacks voice-layer keys, fall back per section 6.0b to the four body-text qualitative fields (硬约束 + AI 易犯错误 to 硬性规则, 叙事身份 to 整体基调,
    描写层次 to 风格参考例句). Defense: wrap string or non-list input as a single item to avoid list('string') splitting it character by character."""
    hc = _as_list(card.get("hard_constraints"))
    sg = _as_list(card.get("soft_guidance"))
    fse = card.get("few_shot_examples")
    if not isinstance(fse, list):
        fse = [fse] if fse else []
    if body:
        sec = None
        if not hc:
            sec = _body_sections(body)
            hc = sec.get("硬约束", []) + sec.get("AI 易犯错误", [])
        if not sg:
            if sec is None:
                sec = _body_sections(body)
            sg = sec.get("叙事身份", [])
        if not fse:
            if sec is None:
                sec = _body_sections(body)
            fse = [{"type": "描写层次", "text": t} for t in sec.get("描写层次和手法", [])]
    out["硬性规则"] = hc
    out["整体基调"] = sg
    # Group by type (spec render step 6): merge the same type into one line; mark missing text/reason as "（未填写）" instead of a literal None
    groups: dict[str, list[str]] = {}
    for e in fse:
        if not isinstance(e, dict):
            e = {"type": "未标注", "text": str(e)}
        t = e.get("type") or "未标注"
        txt = e.get("text") or "（未填写）"
        reason = e.get("reason")
        item = f"{txt}: {reason}" if reason else txt
        groups.setdefault(t, []).append(item)
    out["风格参考例句"] = [f"[{t}] " + "；".join(items) for t, items in groups.items()]

def _body_sections(body: str) -> dict[str, list[str]]:
    """Split the card body text by '## ' subsections (for the section 6.0b fallback): section name (strip the "（原 X）" suffix) to non-empty content lines (strip the '- ' prefix)."""
    sections: dict[str, list[str]] = {}
    cur = None
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("## "):
            cur = s[3:].split("（")[0].strip()
            sections.setdefault(cur, [])
        elif cur is not None and s:
            sections[cur].append(s[2:].strip() if s.startswith("- ") else s)
    return sections

def _as_list(v) -> list[str]:
    """String to a single-element list; already a list stays as-is; None/empty to []."""
    if v is None:
        return []
    if isinstance(v, list):
        return list(v)
    if isinstance(v, (str, int, float)):
        return [str(v)]
    return []

def _parse_frontmatter(text: str) -> tuple:
    """frontmatter to (dict, body) (single-source implementation in style_common.split_frontmatter, review #38)."""
    return split_frontmatter(text)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--card", required=True)
    args = ap.parse_args()
    text = __import__("pathlib").Path(args.card).read_text(encoding="utf-8")
    card, body = _parse_frontmatter(text)
    if not card:
        print("Card is missing frontmatter", file=sys.stderr)
        return 2
    for sec, items in render_card(card, scene_type=card.get("scene_type") or "general", body=body).items():
        if items:
            print(f"【{sec}】")
            for it in items:
                print(f"  - {it}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
