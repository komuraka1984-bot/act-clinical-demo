from typing import List
import streamlit as st

st.set_page_config(
    page_title="ACT Clinical Decision Support",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

    burden_prev = (prev - min_v) / scale
    burden_curr = (curr - min_v) / scale

    return {
        "name": name,
        "prev": prev,
        "curr": curr,
        "delta": delta,
        "normalized_delta": norm,
        "burden_prev": clamp(burden_prev),
        "burden_curr": clamp(burden_curr),
        "improvement_gain": max(0.0, burden_prev - burden_curr),
        "weight": weight,
    }

# =========================================================
# Convergence
# =========================================================
def compute_convergence(metrics: List[dict]) -> float:
    weighted = []

    for m in metrics:
        weighted.append(m.get("weight", 1.0) * m["normalized_delta"])

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

    return clamp(
        0.60 * coherence +
        0.30 * magnitude +
        0.10 * compactness
    )

# =========================================================
# ACT score
# =========================================================
def score_act(disease, duration, progression, response, metrics):
    if not metrics:
        return None

    total_w = sum(m.get("weight", 1.0) for m in metrics)
    residual = sum(m["burden_curr"] * m.get("weight", 1.0) for m in metrics) / total_w
    improvement = sum(m["improvement_gain"] * m.get("weight", 1.0) for m in metrics) / total_w
    convergence = compute_convergence(metrics)

    response_factor = {"Good": 1.0, "Partial": 0.8, "None": 0.5}[response]
    traj_factor = {"Improving": 0.8, "Stable": 0.9, "Worsening": 1.0}[progression]

    duration_factor = clamp(duration / 24.0)

    safety = clamp(
        0.30 * convergence +
        0.25 * response_factor +
        0.20 * traj_factor +
        0.15 * residual +
        0.10 * duration_factor
    )

    residual_opportunity = clamp(
        0.50 * residual +
        0.30 * improvement +
        0.20 * convergence
    )

    eie_core = 0.35 * safety + 0.65 * residual_opportunity
    eie = clamp(eie_core * (0.40 + 0.60 * convergence))

    metric_map = {m["name"]: m for m in metrics}

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

    else:  # Psoriasis
        dlqi = metric_map.get("DLQI", {}).get("curr", None)
        pasi = metric_map.get("PASI", {}).get("curr", None)

        severe_psoriasis = False
        if dlqi is not None and dlqi >= 10:
            severe_psoriasis = True
        if pasi is not None and pasi >= 10:
            severe_psoriasis = True

        if convergence < 0.25:
            rec = "observe"
        elif severe_psoriasis and eie >= 0.50:
            rec = "escalate"
        elif eie >= 0.60:
            rec = "escalate"
        elif eie >= 0.40:
            rec = "optimize"
        elif safety >= 0.40:
            rec = "maintain"
        else:
            rec = "observe"

    return {
        "eie": eie,
        "convergence": convergence,
        "residual": residual,
        "safety": safety,
        "improvement": improvement,
        "rec": rec,
        "score": int(eie * 100),
    }

# =========================================================
# UI helpers
# =========================================================
def rec_label(rec: str) -> str:
    return {
        "escalate": "🔴 ESCALATE",
        "optimize": "🟠 OPTIMIZE",
        "maintain": "🟢 MAINTAIN",
        "observe": "⚪ OBSERVE",
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
st.title("ACT Clinical Decision Support")

with st.expander("About this app"):
    st.write(
        "Compact single-screen layout: Input on the left, Output on the right. "
        "For psoriasis, DLQI is always used and PASI can be added with the Use PASI option."
    )

# =========================================================
# Session state
# =========================================================
if "act_has_run" not in st.session_state:
    st.session_state.act_has_run = False
if "act_result" not in st.session_state:
    st.session_state.act_result = None
if "act_metrics" not in st.session_state:
    st.session_state.act_metrics = []

# =========================================================
# Layout
# =========================================================
left, right = st.columns([1.0, 1.05], gap="small")

# ---------------------------------------------------------
# LEFT: INPUT
# ---------------------------------------------------------
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Input</div>', unsafe_allow_html=True)

    top1, top2 = st.columns(2)
    with top1:
        disease = st.selectbox("Disease", ["Atopic Dermatitis", "Psoriasis"])
    with top2:
        duration = st.number_input("Duration / observation window", value=15.0, min_value=0.0, step=1.0)

    top3, top4 = st.columns(2)
    with top3:
        progression = st.selectbox("Trajectory", ["Improving", "Stable", "Worsening"])
    with top4:
        response = st.selectbox("Response", ["Good", "Partial", "None"])

    st.markdown('<div class="small-label">Metrics</div>', unsafe_allow_html=True)

    metrics = []

    if disease == "Atopic Dermatitis":
        with st.expander("Metric guide"):
            st.write("ADCT: patient-reported disease control, 0–24")
            st.write("EASI: eczema severity, 0–72")
            st.write("Itch NRS: itch severity, 0–10")
            st.write("Sleep NRS: sleep disturbance, 0–10")

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
        with st.expander("Metric guide"):
            st.write("DLQI: dermatology quality of life, 0–30")
            st.write("PASI: psoriasis area and severity index, 0–72")
            st.write("Use PASI can be turned off when only DLQI is available.")

        use_pasi = st.checkbox("Use PASI", value=True)

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

    run = st.button("Run ACT Analysis", use_container_width=True)

    if run:
        st.session_state.act_result = score_act(disease, duration, progression, response, metrics)
        st.session_state.act_metrics = metrics
        st.session_state.act_has_run = True

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# RIGHT: OUTPUT
# ---------------------------------------------------------
with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Output</div>', unsafe_allow_html=True)

    if st.session_state.act_has_run and st.session_state.act_result is not None:
        r = st.session_state.act_result
        metrics_out = st.session_state.act_metrics

        upper1, upper2 = st.columns([1.0, 1.0])

        with upper1:
            st.markdown("**Input Summary**")
            for m in metrics_out:
                st.metric(
                    m["name"],
                    f"{m['curr']:.1f}",
                    metric_delta_text(m["prev"], m["curr"])
                )

        with upper2:
            st.markdown("**ACT Core**")
            st.metric("Convergence", f"{r['convergence']:.2f}")
            st.metric("Residual", f"{r['residual']:.2f}")
            st.metric("EIE", f"{r['eie']:.2f}")
            st.metric("Score", r["score"])

        rec_class = {
            "escalate": "rec-escalate",
            "optimize": "rec-optimize",
            "maintain": "rec-maintain",
            "observe": "rec-observe",
        }[r["rec"]]

        st.markdown("**Recommendation**")
        st.markdown(
            f'<div class="rec-box {rec_class}">{rec_label(r["rec"])}</div>',
            unsafe_allow_html=True
        )

        low1, low2 = st.columns(2)
        with low1:
            st.metric("Safety", f"{r['safety']:.2f}")
        with low2:
            st.metric("Improvement", f"{r['improvement']:.2f}")

        with st.expander("Interpretation"):
            st.write(f"Disease: {disease}")
            st.write(f"Duration / observation window: {duration:.1f}")
            st.write(f"Trajectory: {progression}")
            st.write(f"Response: {response}")
            st.write(
                "Recommendation is derived from convergence, residual burden, EIE, "
                "and disease-specific logic."
            )

    else:
        st.info("Enter values on the left and run the analysis.")

    st.markdown('</div>', unsafe_allow_html=True)
