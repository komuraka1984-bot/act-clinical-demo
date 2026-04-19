from typing import List, Dict
import streamlit as st

st.set_page_config(
    page_title="ACT Clinical Decision Support",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# Language dictionary
# =========================================================
TEXT: Dict[str, Dict[str, str]] = {
    "en": {
        "page_title": "ACT Clinical Decision Support",
        "language": "Language",
        "about_title": "About this app",
        "about_1": "This demo provides ACT-based clinical decision support using multi-metric trajectory assessment.",
        "about_2": "It is intended for research demonstration and educational use. It does not replace clinical judgment.",
        "input": "Input",
        "output": "Output",
        "disease": "Disease",
        "duration": "Duration",
        "trajectory": "Trajectory",
        "response": "Response",
        "metric_guide": "Metric guide",
        "metrics": "Metrics",
        "run": "Run ACT Analysis",
        "input_summary": "Input Summary",
        "recommendation": "Recommendation",
        "clinical_interpretation": "Clinical interpretation",
        "case_summary": "Case summary",
        "demo_note": "Demo version for research presentation. This tool provides ACT-based trajectory interpretation and does not replace clinical judgment.",
        "enter_values": "This tool is a demonstration for clinical decision support. Enter values on the left and run the analysis.",
        "trajectory_improving": "Improving",
        "trajectory_stable": "Stable",
        "trajectory_worsening": "Worsening",
        "response_good": "Good",
        "response_partial": "Partial",
        "response_none": "None",
        "disease_ad": "Atopic Dermatitis",
        "disease_psoriasis": "Psoriasis",
        "adct_guide": "ADCT: patient-reported disease control",
        "easi_guide": "EASI: eczema severity",
        "itch_guide": "Itch NRS: itch severity",
        "sleep_guide": "Sleep NRS: sleep disturbance",
        "adct_prev": "ADCT prev",
        "adct_curr": "ADCT curr",
        "easi_prev": "EASI prev",
        "easi_curr": "EASI curr",
        "itch_prev": "Itch prev",
        "itch_curr": "Itch curr",
        "sleep_prev": "Sleep prev",
        "sleep_curr": "Sleep curr",
        "rec_escalate": "🔴 ESCALATE",
        "rec_optimize": "🟠 OPTIMIZE",
        "rec_maintain": "🟢 MAINTAIN",
        "rec_observe": "⚪ OBSERVE",
        "interp_escalate": "Current trajectory suggests insufficient control. Treatment intensification should be considered.",
        "interp_optimize": "Current trajectory suggests partial control. Optimization of the current strategy may be appropriate.",
        "interp_maintain": "Current trajectory suggests acceptable control. Continuation of the current strategy with monitoring may be appropriate.",
        "interp_observe": "Current trajectory suggests low immediate intervention pressure. Continued observation may be appropriate.",
        "case_disease": "Disease",
        "case_duration": "Duration",
        "case_trajectory": "Trajectory",
        "case_response": "Response",
        "pharma_note_title": "For partner discussion",
        "pharma_note_body": "This interface is intended to demonstrate ACT-based trajectory interpretation in a compact and presentation-ready format suitable for exploratory discussion with clinical and industry stakeholders.",
        "trajectory_impression": "Trajectory impression",
        "impression_high": "High transition pressure",
        "impression_mid": "Intermediate transition pressure",
        "impression_low": "Low transition pressure",
        "summary_improving": "Overall trajectory suggests structural improvement across multiple domains.",
        "summary_mixed": "Trajectory suggests mixed control with residual burden in selected domains.",
        "summary_worsening": "Trajectory suggests persistent or increasing pressure despite partial improvement in some domains.",
        "badge_improved": "Improved",
        "badge_worsened": "Worsened",
        "badge_unchanged": "Unchanged",
    },
    "ja": {
        "page_title": "ACT臨床意思決定支援",
        "language": "言語",
        "about_title": "このアプリについて",
        "about_1": "このデモは、複数指標の軌道評価に基づくACT型の臨床意思決定支援を提供します。",
        "about_2": "研究発表および教育目的のデモです。臨床判断そのものを置き換えるものではありません。",
        "input": "入力",
        "output": "出力",
        "disease": "疾患",
        "duration": "期間",
        "trajectory": "軌道",
        "response": "反応",
        "metric_guide": "指標ガイド",
        "metrics": "指標",
        "run": "ACT解析を実行",
        "input_summary": "入力サマリー",
        "recommendation": "推奨",
        "clinical_interpretation": "解釈",
        "case_summary": "症例サマリー",
        "demo_note": "研究発表向けデモ版です。本ツールはACTに基づく軌道解釈を提供するものであり、臨床判断を代替するものではありません。",
        "enter_values": "本ツールは臨床判断支援のデモです。左側に値を入力して解析を実行してください。",
        "trajectory_improving": "改善傾向",
        "trajectory_stable": "安定",
        "trajectory_worsening": "悪化傾向",
        "response_good": "良好",
        "response_partial": "部分反応",
        "response_none": "無効",
        "disease_ad": "アトピー性皮膚炎",
        "disease_psoriasis": "乾癬",
        "adct_guide": "ADCT: 患者報告による疾患コントロール指標",
        "easi_guide": "EASI: 湿疹重症度",
        "itch_guide": "Itch NRS: かゆみ重症度",
        "sleep_guide": "Sleep NRS: 睡眠障害重症度",
        "adct_prev": "ADCT 前回",
        "adct_curr": "ADCT 現在",
        "easi_prev": "EASI 前回",
        "easi_curr": "EASI 現在",
        "itch_prev": "かゆみ 前回",
        "itch_curr": "かゆみ 現在",
        "sleep_prev": "睡眠 前回",
        "sleep_curr": "睡眠 現在",
        "rec_escalate": "🔴 増強",
        "rec_optimize": "🟠 最適化",
        "rec_maintain": "🟢 維持",
        "rec_observe": "⚪ 経過観察",
        "interp_escalate": "現在の軌道はコントロール不十分を示唆します。治療強化を検討すべきです。",
        "interp_optimize": "現在の軌道は部分的コントロールを示唆します。現在の治療戦略の最適化が適切と考えられます。",
        "interp_maintain": "現在の軌道は許容可能なコントロールを示唆します。経過観察を伴う現行治療の維持が適切と考えられます。",
        "interp_observe": "現在の軌道は直ちに介入圧が高くないことを示唆します。経過観察が適切と考えられます。",
        "case_disease": "疾患",
        "case_duration": "期間",
        "case_trajectory": "軌道",
        "case_response": "反応",
        "pharma_note_title": "パートナー向け補足",
        "pharma_note_body": "この画面は、ACTに基づく軌道解釈をコンパクトかつ提示しやすい形式で示すためのものであり、臨床・企業双方の探索的議論に適しています。",
        "trajectory_impression": "軌道インプレッション",
        "impression_high": "高い転移圧",
        "impression_mid": "中等度の転移圧",
        "impression_low": "低い転移圧",
        "summary_improving": "複数ドメインで全体として構造的改善が示唆されます。",
        "summary_mixed": "一部に残存負荷を伴う混合的コントロールが示唆されます。",
        "summary_worsening": "一部改善があっても、全体として持続的または増大する圧が示唆されます。",
        "badge_improved": "改善",
        "badge_worsened": "悪化",
        "badge_unchanged": "不変",
    },
}

# =========================================================
# Helpers
# =========================================================
def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def safe_mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def scale01(x: float, min_v: float, max_v: float) -> float:
    width = max(max_v - min_v, 1e-9)
    return clamp((x - min_v) / width)


# =========================================================
# Metric processing
# =========================================================
def compute_metric_stats(name: str, prev: float, curr: float, min_v: float, max_v: float) -> dict:
    scale = max(max_v - min_v, 1e-9)
    delta = curr - prev

    return {
        "name": name,
        "prev": prev,
        "curr": curr,
        "delta": delta,
        "prev_norm": scale01(prev, min_v, max_v),
        "curr_norm": scale01(curr, min_v, max_v),
        "improvement_gain": max(0.0, scale01(prev, min_v, max_v) - scale01(curr, min_v, max_v)),
    }


# =========================================================
# Simplified public demo engine
# NOTE:
# - intentionally simplified
# - no exposed core weights / thresholds from internal model
# =========================================================
def summarize_state(metrics: List[dict], progression: str, response: str) -> dict:
    current_burden = safe_mean([m["curr_norm"] for m in metrics])
    improvement = safe_mean([m["improvement_gain"] for m in metrics])

    prog_map = {
        "Improving": 0.20,
        "Stable": 0.50,
        "Worsening": 0.80,
    }
    resp_map = {
        "Good": 0.20,
        "Partial": 0.50,
        "None": 0.85,
    }

    pressure = clamp(
        0.45 * current_burden +
        0.30 * prog_map[progression] +
        0.25 * resp_map[response] -
        0.20 * improvement
    )

    return {
        "pressure": pressure,
        "current_burden": current_burden,
        "improvement": improvement,
    }


def public_recommendation(disease: str, duration: float, progression: str, response: str, metrics: List[dict]) -> dict:
    s = summarize_state(metrics, progression, response)

    # Disease-specific light adjustment, intentionally broad
    disease_shift = 0.05 if disease == "Atopic Dermatitis" else 0.00
    duration_shift = 0.08 if duration >= 12 else 0.00

    decision_signal = clamp(s["pressure"] + disease_shift + duration_shift)

    if decision_signal >= 0.72:
        rec = "escalate"
    elif decision_signal >= 0.52:
        rec = "optimize"
    elif decision_signal >= 0.32:
        rec = "maintain"
    else:
        rec = "observe"

    return {
        "rec": rec,
        "pressure": decision_signal,
        "current_burden": s["current_burden"],
        "improvement": s["improvement"],
    }


# =========================================================
# UI helpers
# =========================================================
def metric_direction(name: str) -> str:
    # current supported metrics: lower is better
    return "lower_better"


def metric_badge(prev: float, curr: float, name: str, lang: str):
    diff = curr - prev
    if abs(diff) < 1e-9:
        return f"• {TEXT[lang]['badge_unchanged']}", "badge-neutral"

    lower_better = metric_direction(name) == "lower_better"
    improved = curr < prev if lower_better else curr > prev
    signed = f"{diff:+.1f}"

    if improved:
        arrow = "↓" if lower_better else "↑"
        return f"{arrow} {TEXT[lang]['badge_improved']} ({signed})", "badge-good"
    else:
        arrow = "↑" if lower_better else "↓"
        return f"{arrow} {TEXT[lang]['badge_worsened']} ({signed})", "badge-bad"


def rec_label(rec: str, lang: str) -> str:
    key_map = {
        "escalate": "rec_escalate",
        "optimize": "rec_optimize",
        "maintain": "rec_maintain",
        "observe": "rec_observe",
    }
    return TEXT[lang][key_map[rec]]


def interpretation_text(rec: str, lang: str) -> str:
    key_map = {
        "escalate": "interp_escalate",
        "optimize": "interp_optimize",
        "maintain": "interp_maintain",
        "observe": "interp_observe",
    }
    return TEXT[lang][key_map[rec]]


def trajectory_impression(result: dict, lang: str) -> str:
    p = result["pressure"]
    if p >= 0.72:
        return TEXT[lang]["impression_high"]
    if p >= 0.52:
        return TEXT[lang]["impression_mid"]
    return TEXT[lang]["impression_low"]


def summary_text(result: dict, lang: str) -> str:
    if result["rec"] == "escalate":
        return TEXT[lang]["summary_worsening"]
    if result["rec"] == "optimize":
        return TEXT[lang]["summary_mixed"]
    return TEXT[lang]["summary_improving"]


# =========================================================
# CSS
# =========================================================
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1500px;
        padding-top: 0.8rem;
        padding-bottom: 0.5rem;
        padding-left: 0.9rem;
        padding-right: 0.9rem;
    }

    h1 {
        margin-top: 0.2rem !important;
        margin-bottom: 0.45rem !important;
        line-height: 1.2 !important;
    }

    .panel {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 0.85rem 0.95rem 0.8rem 0.95rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
        height: 100%;
    }

    .section-label {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }

    .small-label {
        font-size: 0.82rem;
        color: #6b7280;
        margin-bottom: 0.12rem;
    }

    .rec-box {
        border-radius: 14px;
        padding: 0.95rem 0.8rem;
        text-align: center;
        font-weight: 800;
        font-size: 1.45rem;
        margin-bottom: 0.6rem;
        border: 1px solid transparent;
    }

    .rec-escalate {
        background: #fee2e2;
        color: #991b1b;
        border-color: #fecaca;
    }

    .rec-optimize {
        background: #ffedd5;
        color: #9a3412;
        border-color: #fed7aa;
    }

    .rec-maintain {
        background: #dcfce7;
        color: #166534;
        border-color: #bbf7d0;
    }

    .rec-observe {
        background: #f3f4f6;
        color: #374151;
        border-color: #e5e7eb;
    }

    .summary-box {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.8rem 0.85rem;
        margin-top: 0.25rem;
        line-height: 1.45;
    }

    .partner-box {
        background: #f9fafb;
        border-left: 4px solid #2563eb;
        border-radius: 10px;
        padding: 0.7rem 0.8rem;
        margin-top: 0.8rem;
        color: #374151;
    }

    .impression-box {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.7rem 0.8rem;
        margin-bottom: 0.6rem;
    }

    .metric-card {
        background: #fafafa;
        border: 1px solid #eeeeee;
        border-radius: 12px;
        padding: 0.7rem 0.75rem;
        margin-bottom: 0.5rem;
    }

    .metric-name {
        font-size: 0.9rem;
        color: #374151;
        margin-bottom: 0.15rem;
    }

    .metric-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.3rem;
    }

    .badge {
        display: inline-block;
        border-radius: 999px;
        padding: 0.18rem 0.5rem;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .badge-good {
        background: #dcfce7;
        color: #166534;
    }

    .badge-bad {
        background: #fee2e2;
        color: #b91c1c;
    }

    .badge-neutral {
        background: #f3f4f6;
        color: #374151;
    }

    .stButton > button {
        height: 2.55rem;
        font-weight: 700;
        border-radius: 10px;
    }

    .compact-note {
        font-size: 0.82rem;
        color: #6b7280;
        line-height: 1.4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Language selector
# =========================================================
if "lang" not in st.session_state:
    st.session_state.lang = "en"

lang_col1, lang_col2 = st.columns([6, 1])
with lang_col2:
    lang_choice = st.selectbox(
        TEXT[st.session_state.lang]["language"],
        options=["English", "日本語"],
        index=0 if st.session_state.lang == "en" else 1,
    )
    st.session_state.lang = "en" if lang_choice == "English" else "ja"

lang = st.session_state.lang
T = TEXT[lang]

# =========================================================
# Header
# =========================================================
st.title(T["page_title"])

with st.expander(T["about_title"]):
    st.write(T["about_1"])
    st.write(T["about_2"])

# =========================================================
# Session state
# =========================================================
if "act_has_run" not in st.session_state:
    st.session_state.act_has_run = False
if "act_result" not in st.session_state:
    st.session_state.act_result = None

# =========================================================
# Layout
# =========================================================
left, right = st.columns([1.0, 1.0], gap="small")

# ---------------------------------------------------------
# LEFT: INPUT
# ---------------------------------------------------------
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T["input"]}</div>', unsafe_allow_html=True)

    disease_options = {
        T["disease_ad"]: "Atopic Dermatitis",
        T["disease_psoriasis"]: "Psoriasis",
    }
    trajectory_options = {
        T["trajectory_improving"]: "Improving",
        T["trajectory_stable"]: "Stable",
        T["trajectory_worsening"]: "Worsening",
    }
    response_options = {
        T["response_good"]: "Good",
        T["response_partial"]: "Partial",
        T["response_none"]: "None",
    }

    c1, c2 = st.columns(2)
    with c1:
        disease_label = st.selectbox(T["disease"], list(disease_options.keys()))
        disease = disease_options[disease_label]
    with c2:
        duration = st.number_input(T["duration"], value=15.0, min_value=0.0, step=1.0)

    c3, c4 = st.columns(2)
    with c3:
        progression_label = st.selectbox(T["trajectory"], list(trajectory_options.keys()))
        progression = trajectory_options[progression_label]
    with c4:
        response_label = st.selectbox(T["response"], list(response_options.keys()))
        response = response_options[response_label]

    with st.expander(T["metric_guide"]):
        st.write(T["adct_guide"])
        st.write(T["easi_guide"])
        st.write(T["itch_guide"])
        st.write(T["sleep_guide"])

    st.markdown(f'<div class="small-label">{T["metrics"]}</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        adct_prev = st.number_input(T["adct_prev"], value=20.0, key="adct_prev")
    with m2:
        adct_curr = st.number_input(T["adct_curr"], value=1.0, key="adct_curr")

    m3, m4 = st.columns(2)
    with m3:
        easi_prev = st.number_input(T["easi_prev"], value=18.0, key="easi_prev")
    with m4:
        easi_curr = st.number_input(T["easi_curr"], value=2.0, key="easi_curr")

    m5, m6 = st.columns(2)
    with m5:
        itch_prev = st.number_input(T["itch_prev"], value=9.0, key="itch_prev")
    with m6:
        itch_curr = st.number_input(T["itch_curr"], value=5.0, key="itch_curr")

    m7, m8 = st.columns(2)
    with m7:
        sleep_prev = st.number_input(T["sleep_prev"], value=8.0, key="sleep_prev")
    with m8:
        sleep_curr = st.number_input(T["sleep_curr"], value=1.0, key="sleep_curr")

    run = st.button(T["run"], use_container_width=True)

    if run:
        metrics = [
            compute_metric_stats("ADCT", adct_prev, adct_curr, 0, 24),
            compute_metric_stats("EASI", easi_prev, easi_curr, 0, 72),
            compute_metric_stats("Itch NRS", itch_prev, itch_curr, 0, 10),
            compute_metric_stats("Sleep NRS", sleep_prev, sleep_curr, 0, 10),
        ]

        st.session_state.act_result = public_recommendation(
            disease=disease,
            duration=duration,
            progression=progression,
            response=response,
            metrics=metrics,
        )
        st.session_state.act_has_run = True

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# RIGHT: OUTPUT
# ---------------------------------------------------------
with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T["output"]}</div>', unsafe_allow_html=True)

    if st.session_state.act_has_run and st.session_state.act_result is not None:
        r = st.session_state.act_result

        st.markdown(f"**{T['input_summary']}**")
        s1, s2 = st.columns(2)
        with s1:
            badge_text, badge_class = metric_badge(adct_prev, adct_curr, "ADCT", lang)
            st.markdown(
                f'<div class="metric-card"><div class="metric-name">ADCT</div><div class="metric-value">{adct_curr:.1f}</div><span class="badge {badge_class}">{badge_text}</span></div>',
                unsafe_allow_html=True,
            )
            badge_text, badge_class = metric_badge(easi_prev, easi_curr, "EASI", lang)
            st.markdown(
                f'<div class="metric-card"><div class="metric-name">EASI</div><div class="metric-value">{easi_curr:.1f}</div><span class="badge {badge_class}">{badge_text}</span></div>',
                unsafe_allow_html=True,
            )
        with s2:
            badge_text, badge_class = metric_badge(itch_prev, itch_curr, "Itch NRS", lang)
            st.markdown(
                f'<div class="metric-card"><div class="metric-name">Itch NRS</div><div class="metric-value">{itch_curr:.1f}</div><span class="badge {badge_class}">{badge_text}</span></div>',
                unsafe_allow_html=True,
            )
            badge_text, badge_class = metric_badge(sleep_prev, sleep_curr, "Sleep NRS", lang)
            st.markdown(
                f'<div class="metric-card"><div class="metric-name">Sleep NRS</div><div class="metric-value">{sleep_curr:.1f}</div><span class="badge {badge_class}">{badge_text}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown(f"**{T['trajectory_impression']}**")
        st.markdown(
            f'<div class="impression-box">{trajectory_impression(r, lang)}</div>',
            unsafe_allow_html=True,
        )

        rec_class = {
            "escalate": "rec-escalate",
            "optimize": "rec-optimize",
            "maintain": "rec-maintain",
            "observe": "rec-observe",
        }[r["rec"]]

        st.markdown(f"**{T['recommendation']}**")
        st.markdown(
            f'<div class="rec-box {rec_class}">{rec_label(r["rec"], lang)}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(f"**{T['clinical_interpretation']}**")
        interp = f"{interpretation_text(r['rec'], lang)} {summary_text(r, lang)}"
        st.markdown(
            f'<div class="summary-box">{interp}</div>',
            unsafe_allow_html=True,
        )

        with st.expander(T["case_summary"]):
            st.write(f"{T['case_disease']}: {disease_label}")
            st.write(f"{T['case_duration']}: {duration:.1f}")
            st.write(f"{T['case_trajectory']}: {progression_label}")
            st.write(f"{T['case_response']}: {response_label}")

        st.markdown(
            f"""
            <div class="partner-box">
                <strong>{T["pharma_note_title"]}</strong><br>
                {T["pharma_note_body"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="compact-note">{T["demo_note"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info(T["enter_values"])

    st.markdown('</div>', unsafe_allow_html=True)
