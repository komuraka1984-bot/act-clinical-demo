from typing import List
import streamlit as st

st.set_page_config(
    page_title="ACT Clinical Decision Support",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# Language
# =========================================================
LANG = {
    "English": {
        "title": "ACT Clinical Decision Support",
        "about": "About this app",
        "about_text": (
            "For psoriasis, DLQI is always used and PASI can be added with Use PASI. "
            "DLQI–PASI divergence is used to reduce overconfident structural convergence. "
            "The psoriasis logic is tuned to support escalation when residual burden and "
            "structural convergence coexist."
        ),
        "input": "Input",
        "output": "Output",
        "disease": "Disease",
        "ad": "Atopic Dermatitis",
        "psoriasis": "Psoriasis",
        "duration": "Duration / observation window",
        "trajectory": "Trajectory",
        "response": "Response",
        "improving": "Improving",
        "stable": "Stable",
        "worsening": "Worsening",
        "good": "Good",
        "partial": "Partial",
        "none": "None",
        "metrics": "Metrics",
        "metric_guide": "Metric guide",
        "use_pasi": "Use PASI",
        "run": "Run ACT Analysis",
        "input_summary": "Input Summary",
        "act_core": "ACT Core",
        "recommendation": "Recommendation",
        "convergence": "Convergence",
        "residual": "Residual",
        "eie": "EIE",
        "score": "Score",
        "safety": "Safety",
        "improvement": "Improvement",
        "divergence": "DLQI–PASI Divergence",
        "severity": "Severity",
        "interpretation": "Interpretation",
        "empty": "Enter values on the left and run the analysis.",
        "psoriasis_logic": (
            "Psoriasis logic uses DLQI/PASI residual burden, structural convergence, "
            "DLQI–PASI divergence, and severity-adjusted EIE. Escalation is favored "
            "when residual disease burden and structural convergence coexist."
        ),
        "duration_note": (
            "Duration is intentionally weakly reflected as a supporting factor, "
            "not as a dominant driver."
        ),
        "ad_logic": (
            "AD logic uses ADCT-weighted residual burden, convergence, EIE, "
            "and disease-control thresholds."
        ),
        "escalate": "🔴 ESCALATE",
        "optimize": "🟠 OPTIMIZE",
        "maintain": "🟢 MAINTAIN",
        "observe": "⚪ OBSERVE",
    },
    "日本語": {
        "title": "ACT 臨床意思決定支援",
        "about": "このアプリについて",
        "about_text": (
            "乾癬ではDLQIを必須指標とし、Use PASIをオンにするとPASIを追加できます。"
            "DLQI–PASIの乖離を用いて、構造的一致性の過大評価を抑制します。"
            "乾癬ロジックでは、残存負荷と構造的一致性が共存する場合に、"
            "治療強化が出やすいように調整しています。"
        ),
        "input": "入力",
        "output": "出力",
        "disease": "疾患",
        "ad": "アトピー性皮膚炎",
        "psoriasis": "乾癬",
        "duration": "期間 / 観察ウィンドウ",
        "trajectory": "経過",
        "response": "治療反応",
        "improving": "改善",
        "stable": "安定",
        "worsening": "悪化",
        "good": "良好",
        "partial": "部分的",
        "none": "なし",
        "metrics": "指標",
        "metric_guide": "指標ガイド",
        "use_pasi": "PASIを使用",
        "run": "ACT解析を実行",
        "input_summary": "入力サマリー",
        "act_core": "ACTコア",
        "recommendation": "推奨",
        "convergence": "構造的一致性",
        "residual": "残存負荷",
        "eie": "EIE",
        "score": "スコア",
        "safety": "安全性",
        "improvement": "改善度",
        "divergence": "DLQI–PASI乖離",
        "severity": "重症度",
        "interpretation": "解釈",
        "empty": "左側に値を入力し、解析を実行してください。",
        "psoriasis_logic": (
            "乾癬ロジックでは、DLQI/PASIの残存負荷、構造的一致性、"
            "DLQI–PASI乖離、重症度補正EIEを用いています。"
            "残存負荷と構造的一致性が共存する場合、治療強化を支持しやすくしています。"
        ),
        "duration_note": (
            "期間は意図的に弱く反映しており、主要因ではなく補助因子として扱います。"
        ),
        "ad_logic": (
            "ADロジックでは、ADCTを重視した残存負荷、構造的一致性、EIE、"
            "疾患コントロール閾値を用いています。"
        ),
        "escalate": "🔴 強化",
        "optimize": "🟠 最適化",
        "maintain": "🟢 維持",
        "observe": "⚪ 経過観察",
    }
}

language = st.sidebar.selectbox("Language / 言語", ["English", "日本語"])
T = LANG[language]

DISEASE_MAP = {
    T["ad"]: "Atopic Dermatitis",
    T["psoriasis"]: "Psoriasis",
}

TRAJECTORY_MAP = {
    T["improving"]: "Improving",
    T["stable"]: "Stable",
    T["worsening"]: "Worsening",
}

RESPONSE_MAP = {
    T["good"]: "Good",
    T["partial"]: "Partial",
    T["none"]: "None",
}

# =========================================================
# Helpers
# =========================================================
def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def safe_mean(values):
    return sum(values) / len(values) if values else 0.0

# =========================================================
# Metric processing
# =========================================================
def compute_metric_stats(name, prev, curr, min_v, max_v, weight=1.0):
    scale = max(max_v - min_v, 1e-9)
    delta = curr - prev
    norm = delta / scale

    burden_prev = clamp((prev - min_v) / scale)
    burden_curr = clamp((curr - min_v) / scale)

    return {
        "name": name,
        "prev": prev,
        "curr": curr,
        "delta": delta,
        "normalized_delta": norm,
        "burden_prev": burden_prev,
        "burden_curr": burden_curr,
        "improvement_gain": max(0.0, burden_prev - burden_curr),
        "weight": weight,
    }

# =========================================================
# Convergence
# =========================================================
def compute_convergence(metrics: List[dict]) -> float:
    if not metrics:
        return 0.0

    weighted = [m.get("weight", 1.0) * m["normalized_delta"] for m in metrics]

    signs = [1 if v > 0 else -1 if v < 0 else 0 for v in weighted]
    nz = [s for s in signs if s != 0]

    if not nz:
        coherence = 1.0
    else:
        dom = 1 if sum(nz) >= 0 else -1
        coherence = sum(1 for s in nz if s == dom) / len(nz)

    abs_vals = [abs(v) for v in weighted]
    mean_val = safe_mean(abs_vals)
    magnitude = clamp(mean_val * 3.0)

    var = safe_mean([(x - mean_val) ** 2 for x in abs_vals])
    compactness = 1 / (1 + 5 * var)

    convergence = clamp(
        0.60 * coherence +
        0.30 * magnitude +
        0.10 * compactness
    )

    # Single-indicator ACT should not overclaim structural convergence
    if len(metrics) == 1:
        convergence *= 0.60

    return clamp(convergence)

# =========================================================
# Psoriasis-specific logic
# =========================================================
def compute_psoriasis_divergence(metric_map):
    dlqi = metric_map.get("DLQI")
    pasi = metric_map.get("PASI")

    if dlqi is None or pasi is None:
        return 0.0

    return clamp(abs(dlqi["burden_curr"] - pasi["burden_curr"]))

def compute_psoriasis_severity(metric_map):
    dlqi = metric_map.get("DLQI")
    pasi = metric_map.get("PASI")

    vals = []
    if dlqi is not None:
        vals.append(dlqi["burden_curr"])
    if pasi is not None:
        vals.append(pasi["burden_curr"])

    return clamp(max(vals) if vals else 0.0)

# =========================================================
# ACT score
# =========================================================
def score_act(disease, duration, progression, response, metrics):
    if not metrics:
        return None

    metric_map = {m["name"]: m for m in metrics}

    total_w = sum(m.get("weight", 1.0) for m in metrics)
    residual = sum(m["burden_curr"] * m.get("weight", 1.0) for m in metrics) / total_w
    improvement = sum(m["improvement_gain"] * m.get("weight", 1.0) for m in metrics) / total_w

    convergence = compute_convergence(metrics)

    response_factor = {"Good": 1.0, "Partial": 0.8, "None": 0.5}[response]
    traj_factor = {"Improving": 0.8, "Stable": 0.9, "Worsening": 1.0}[progression]

    # Duration is intentionally weak
    duration_factor = clamp(duration / 60.0)

    divergence = 0.0
    severity = residual

    if disease == "Psoriasis":
        divergence = compute_psoriasis_divergence(metric_map)
        severity = compute_psoriasis_severity(metric_map)

        # Penalize convergence when DLQI and PASI are structurally discordant
        convergence = clamp(convergence * (1.0 - 0.45 * divergence))

    safety = clamp(
        0.32 * convergence +
        0.23 * response_factor +
        0.18 * traj_factor +
        0.20 * residual +
        0.07 * duration_factor
    )

    residual_opportunity = clamp(
        0.48 * residual +
        0.27 * improvement +
        0.20 * convergence +
        0.05 * duration_factor
    )

    eie_core = 0.35 * safety + 0.65 * residual_opportunity
    eie = clamp(eie_core * (0.40 + 0.60 * convergence))

    if disease == "Psoriasis":
        # Slightly more escalation-sensitive psoriasis tuning
        severity_boost = 0.88 + 0.32 * severity
        divergence_penalty = 1.0 - 0.28 * divergence
        eie = clamp(eie * severity_boost * divergence_penalty)

    if disease == "Atopic Dermatitis":
        adct = metric_map.get("ADCT", {}).get("curr", None)
        adct_delta = metric_map.get("ADCT", {}).get("delta", 0)

        if convergence < 0.25:
            rec = "observe"
        elif adct is not None and adct <= 2:
            rec = "observe"
        elif adct_delta > 2 and eie > 0.5:
            rec = "escalate"
        elif adct is not None and adct >= 7:
            rec = "escalate" if convergence >= 0.40 and eie >= 0.60 else "optimize"
        elif eie >= 0.40:
            rec = "optimize"
        elif safety >= 0.40:
            rec = "maintain"
        else:
            rec = "observe"

    else:
        dlqi_curr = metric_map.get("DLQI", {}).get("curr", None)
        pasi_curr = metric_map.get("PASI", {}).get("curr", None)

        severe_psoriasis = False
        if dlqi_curr is not None and dlqi_curr >= 10:
            severe_psoriasis = True
        if pasi_curr is not None and pasi_curr >= 10:
            severe_psoriasis = True

        # -------------------------------------------------
        # Revised psoriasis recommendation logic
        # Aim:
        # - Reduce excessive OPTIMIZE calls
        # - Increase ESCALATE when residual burden + convergence coexist
        # - Avoid over-escalation when DLQI/PASI are discordant
        # -------------------------------------------------
        if convergence < 0.22:
            rec = "observe"

        elif severe_psoriasis and residual >= 0.38 and convergence >= 0.35 and divergence < 0.45:
            rec = "escalate"

        elif eie >= 0.52 and residual >= 0.32 and convergence >= 0.30 and divergence < 0.50:
            rec = "escalate"

        elif divergence >= 0.45 and severity >= 0.40:
            rec = "optimize"

        elif eie >= 0.42 and residual >= 0.28:
            rec = "optimize"

        elif safety >= 0.42 and residual < 0.30:
            rec = "maintain"

        elif safety >= 0.38:
            rec = "maintain"

        else:
            rec = "observe"

    return {
        "eie": eie,
        "convergence": convergence,
        "residual": residual,
        "safety": safety,
        "improvement": improvement,
        "divergence": divergence,
        "severity": severity,
        "rec": rec,
        "score": int(eie * 100),
    }

# =========================================================
# UI helpers
# =========================================================
def rec_label(rec: str) -> str:
    return {
        "escalate": T["escalate"],
        "optimize": T["optimize"],
        "maintain": T["maintain"],
        "observe": T["observe"],
    }.get(rec, rec.upper())

def metric_delta_text(prev: float, curr: float) -> str:
    diff = curr - prev
    sign = "+" if diff > 0 else ""
    return f"{sign}{diff:.1f}"

# =========================================================
# CSS
# =========================================================
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1500px;
        padding-top: 0.8rem;
        padding-bottom: 0.35rem;
        padding-left: 0.9rem;
        padding-right: 0.9rem;
    }
    h1 {
        margin-top: 0.3rem !important;
        margin-bottom: 0.4rem !important;
        line-height: 1.35 !important;
    }
    h2, h3 {
        margin-top: 0rem !important;
        margin-bottom: 0.3rem !important;
    }
    .panel {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 0.7rem 0.8rem 0.65rem 0.8rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
        height: 100%;
    }
    .section-label {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .small-label {
        font-size: 0.8rem;
        color: #6b7280;
        margin-bottom: 0.1rem;
    }
    .rec-box {
        border-radius: 14px;
        padding: 0.8rem 0.7rem;
        text-align: center;
        font-weight: 800;
        font-size: 1.4rem;
        margin-bottom: 0.45rem;
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
    div[data-testid="stMetric"] {
        background: #fafafa;
        border: 1px solid #eeeeee;
        padding: 0.22rem 0.42rem;
        border-radius: 10px;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.74rem !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.15rem !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 0.76rem !important;
    }
    .stButton > button {
        height: 2.4rem;
        font-weight: 700;
        border-radius: 10px;
    }
    .compact-note {
        font-size: 0.78rem;
        color: #6b7280;
        line-height: 1.25;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# Header
# =========================================================
st.title(T["title"])

with st.expander(T["about"]):
    st.write(T["about_text"])

# =========================================================
# Session state
# =========================================================
if "act_has_run" not in st.session_state:
    st.session_state.act_has_run = False
if "act_result" not in st.session_state:
    st.session_state.act_result = None
if "act_metrics" not in st.session_state:
    st.session_state.act_metrics = []
if "act_disease" not in st.session_state:
    st.session_state.act_disease = None
if "act_display_disease" not in st.session_state:
    st.session_state.act_display_disease = None
if "act_duration" not in st.session_state:
    st.session_state.act_duration = None
if "act_progression_label" not in st.session_state:
    st.session_state.act_progression_label = None
if "act_response_label" not in st.session_state:
    st.session_state.act_response_label = None

# =========================================================
# Layout
# =========================================================
left, right = st.columns([1.0, 1.05], gap="small")

# ---------------------------------------------------------
# LEFT: INPUT
# ---------------------------------------------------------
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T["input"]}</div>', unsafe_allow_html=True)

    top1, top2 = st.columns(2)
    with top1:
        disease_label = st.selectbox(T["disease"], [T["ad"], T["psoriasis"]])
        disease = DISEASE_MAP[disease_label]
    with top2:
        duration = st.number_input(
            T["duration"],
            value=15.0,
            min_value=0.0,
            step=1.0
        )

    top3, top4 = st.columns(2)
    with top3:
        progression_label = st.selectbox(T["trajectory"], [T["improving"], T["stable"], T["worsening"]])
        progression = TRAJECTORY_MAP[progression_label]
    with top4:
        response_label = st.selectbox(T["response"], [T["good"], T["partial"], T["none"]])
        response = RESPONSE_MAP[response_label]

    st.markdown(f'<div class="small-label">{T["metrics"]}</div>', unsafe_allow_html=True)

    metrics = []

    if disease == "Atopic Dermatitis":
        with st.expander(T["metric_guide"]):
            st.write("ADCT: 0–24")
            st.write("EASI: 0–72")
            st.write("Itch NRS: 0–10")
            st.write("Sleep NRS: 0–10")

        m1, m2 = st.columns(2)
        with m1:
            adct_prev = st.number_input("ADCT prev", value=20.0, min_value=0.0, max_value=24.0, key="adct_prev")
        with m2:
            adct_curr = st.number_input("ADCT curr", value=1.0, min_value=0.0, max_value=24.0, key="adct_curr")

        m3, m4 = st.columns(2)
        with m3:
            easi_prev = st.number_input("EASI prev", value=18.0, min_value=0.0, max_value=72.0, key="easi_prev")
        with m4:
            easi_curr = st.number_input("EASI curr", value=2.0, min_value=0.0, max_value=72.0, key="easi_curr")

        m5, m6 = st.columns(2)
        with m5:
            itch_prev = st.number_input("Itch NRS prev", value=9.0, min_value=0.0, max_value=10.0, key="itch_prev")
        with m6:
            itch_curr = st.number_input("Itch NRS curr", value=5.0, min_value=0.0, max_value=10.0, key="itch_curr")

        m7, m8 = st.columns(2)
        with m7:
            sleep_prev = st.number_input("Sleep NRS prev", value=8.0, min_value=0.0, max_value=10.0, key="sleep_prev")
        with m8:
            sleep_curr = st.number_input("Sleep NRS curr", value=1.0, min_value=0.0, max_value=10.0, key="sleep_curr")

        metrics = [
            compute_metric_stats("ADCT", adct_prev, adct_curr, 0, 24, weight=2.0),
            compute_metric_stats("EASI", easi_prev, easi_curr, 0, 72, weight=1.0),
            compute_metric_stats("Itch NRS", itch_prev, itch_curr, 0, 10, weight=1.2),
            compute_metric_stats("Sleep NRS", sleep_prev, sleep_curr, 0, 10, weight=1.2),
        ]

    else:
        with st.expander(T["metric_guide"]):
            st.write("DLQI: 0–30")
            st.write("PASI: 0–72")
            st.write(T["duration_note"])

        use_pasi = st.checkbox(T["use_pasi"], value=True)

        p1, p2 = st.columns(2)
        with p1:
            dlqi_prev = st.number_input("DLQI prev", value=20.0, min_value=0.0, max_value=30.0, key="dlqi_prev")
        with p2:
            dlqi_curr = st.number_input("DLQI curr", value=10.0, min_value=0.0, max_value=30.0, key="dlqi_curr")

        metrics = [
            compute_metric_stats("DLQI", dlqi_prev, dlqi_curr, 0, 30, weight=1.4),
        ]

        if use_pasi:
            p3, p4 = st.columns(2)
            with p3:
                pasi_prev = st.number_input("PASI prev", value=18.0, min_value=0.0, max_value=72.0, key="pasi_prev")
            with p4:
                pasi_curr = st.number_input("PASI curr", value=3.0, min_value=0.0, max_value=72.0, key="pasi_curr")

            metrics.append(
                compute_metric_stats("PASI", pasi_prev, pasi_curr, 0, 72, weight=1.6)
            )

    run = st.button(T["run"], use_container_width=True)

    if run:
        st.session_state.act_result = score_act(disease, duration, progression, response, metrics)
        st.session_state.act_metrics = metrics
        st.session_state.act_disease = disease
        st.session_state.act_display_disease = disease_label
        st.session_state.act_duration = duration
        st.session_state.act_progression_label = progression_label
        st.session_state.act_response_label = response_label
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
        metrics_out = st.session_state.act_metrics
        disease_out = st.session_state.act_disease

        upper1, upper2 = st.columns([1.0, 1.0])

        with upper1:
            st.markdown(f"**{T['input_summary']}**")
            for m in metrics_out:
                st.metric(
                    m["name"],
                    f"{m['curr']:.1f}",
                    metric_delta_text(m["prev"], m["curr"])
                )

        with upper2:
            st.markdown(f"**{T['act_core']}**")
            st.metric(T["convergence"], f"{r['convergence']:.2f}")
            st.metric(T["residual"], f"{r['residual']:.2f}")
            st.metric(T["eie"], f"{r['eie']:.2f}")
            st.metric(T["score"], r["score"])

        rec_class = {
            "escalate": "rec-escalate",
            "optimize": "rec-optimize",
            "maintain": "rec-maintain",
            "observe": "rec-observe",
        }[r["rec"]]

        st.markdown(f"**{T['recommendation']}**")
        st.markdown(
            f'<div class="rec-box {rec_class}">{rec_label(r["rec"])}</div>',
            unsafe_allow_html=True
        )

        low1, low2 = st.columns(2)
        with low1:
            st.metric(T["safety"], f"{r['safety']:.2f}")
        with low2:
            st.metric(T["improvement"], f"{r['improvement']:.2f}")

        if disease_out == "Psoriasis":
            p_low1, p_low2 = st.columns(2)
            with p_low1:
                st.metric(T["divergence"], f"{r['divergence']:.2f}")
            with p_low2:
                st.metric(T["severity"], f"{r['severity']:.2f}")

        with st.expander(T["interpretation"]):
            st.write(f"{T['disease']}: {st.session_state.act_display_disease}")
            st.write(f"{T['duration']}: {st.session_state.act_duration:.1f}")
            st.write(f"{T['trajectory']}: {st.session_state.act_progression_label}")
            st.write(f"{T['response']}: {st.session_state.act_response_label}")

            if disease_out == "Psoriasis":
                st.write(T["psoriasis_logic"])
                st.write(T["duration_note"])
            else:
                st.write(T["ad_logic"])

    else:
        st.info(T["empty"])

    st.markdown('</div>', unsafe_allow_html=True)
    
