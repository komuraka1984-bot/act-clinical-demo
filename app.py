import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import requests


APP_TITLE = "Shirabeo Labs | Patient Insight"

CSV_PATH_ADCT = Path("adct_results.csv")
CSV_PATH_DLQI = Path("dlqi_results.csv")

ADMIN_EMAIL = "komura@shirabeo.com"


def send_to_google_form(row):
    url = "https://docs.google.com/forms/d/e/1FAIpQLScC3M0830zqkGnnNsD8D_lOFoRwzyqFrd0ljMP6tAB530Jp1w/formResponse"

    data = {
        "entry.1599902592": row.get("visit_code", ""),
        "entry.1495391757": row.get("total_score", ""),
        "entry.1432435158": row.get("decision", ""),
        "entry.1577092948": row.get("timestamp", ""),
    }

    try:
        res = requests.post(url, data=data, timeout=10)
        print("FORM STATUS:", res.status_code)
        return res.status_code in [200, 302]
    except Exception as e:
        print("FORM ERROR:", e)
        return False


DLQI_QUESTIONS_JA = [
    "この1週間で、皮膚のかゆみ・痛み・ヒリヒリ感・しみる感じはどの程度ありましたか？",
    "この1週間で、皮膚のために恥ずかしい、または人目が気になると感じたことはどの程度ありましたか？",
    "この1週間で、皮膚のために買い物、家事、庭仕事などにどの程度支障がありましたか？",
    "この1週間で、皮膚のために着る服にどの程度影響がありましたか？",
    "この1週間で、皮膚のために社交・余暇活動にどの程度影響がありましたか？",
    "この1週間で、皮膚のためにスポーツがどの程度困難でしたか？",
    "この1週間で、皮膚のために仕事や勉強ができませんでしたか？",
    "この1週間で、皮膚のために配偶者、友人、家族との関係にどの程度問題がありましたか？",
    "この1週間で、皮膚のために性的な困難がどの程度ありましたか？",
    "この1週間で、皮膚の治療がどの程度問題になりましたか？ 例：家が汚れる、時間がかかるなど。",
]

DLQI_QUESTIONS_EN = [
    "Over the last week, how itchy, sore, painful or stinging has your skin been?",
    "Over the last week, how embarrassed or self-conscious have you been because of your skin?",
    "Over the last week, how much has your skin interfered with you going shopping or looking after your home or garden?",
    "Over the last week, how much has your skin influenced the clothes you wear?",
    "Over the last week, how much has your skin affected any social or leisure activities?",
    "Over the last week, how much has your skin made it difficult for you to do any sport?",
    "Over the last week, has your skin prevented you from working or studying?",
    "Over the last week, how much has your skin created problems with your partner or any of your close friends or relatives?",
    "Over the last week, how much has your skin caused any sexual difficulties?",
    "Over the last week, how much of a problem has the treatment for your skin been, for example by making your home messy, or by taking up time?",
]

DLQI_OPTIONS_JA = {
    "全くない / 該当しない": 0,
    "少し": 1,
    "かなり": 2,
    "非常に": 3,
}

DLQI_OPTIONS_EN = {
    "Not at all / Not relevant": 0,
    "A little": 1,
    "A lot": 2,
    "Very much": 3,
}

DLQI_Q7_OPTIONS_JA = {
    "はい、仕事または勉強ができなかった": 3,
    "いいえ、ただし仕事または勉強に支障があった": 2,
    "いいえ": 0,
    "該当しない": 0,
}

DLQI_Q7_OPTIONS_EN = {
    "Yes — prevented work or studying": 3,
    "No, but skin was a problem at work or studying": 2,
    "No": 0,
    "Not relevant": 0,
}


ADCT_QUESTIONS_JA = [
    "この1週間、アトピー性皮膚炎の症状はどの程度でしたか。",
    "この1週間、アトピー性皮膚炎のために激しいかゆみが起こったことは何日ありましたか。",
    "この1週間、アトピー性皮膚炎にどの程度悩まされましたか。",
    "この1週間、アトピー性皮膚炎のためになかなか寝付けなかったり、途中で目が覚めたりすることが何晩ありましたか。",
    "この1週間、アトピー性皮膚炎がどの程度日常の活動に影響しましたか。",
    "この1週間、アトピー性皮膚炎がどの程度気分や感情に影響しましたか。",
]

ADCT_QUESTIONS_EN = [
    "Over the last week, how would you rate your eczema symptoms?",
    "Over the last week, on how many days did you have intense episodes of itching because of your eczema?",
    "Over the last week, how bothered have you been by your eczema?",
    "Over the last week, on how many nights did you have difficulty falling asleep or wake up during the night because of your eczema?",
    "Over the last week, how much did your eczema affect your daily activities?",
    "Over the last week, how much did your eczema affect your mood or emotions?",
]

ADCT_OPTIONS_JA = [
    {"なし": 0, "軽い": 1, "中くらい": 2, "ひどい": 3, "かなりひどい": 4},
    {"全くなかった": 0, "1〜2日": 1, "3〜4日": 2, "5〜6日": 3, "毎日": 4},
    {"全くなかった": 0, "少し": 1, "ある程度": 2, "とても": 3, "極めて": 4},
    {"全くなかった": 0, "1〜2晩": 1, "3〜4晩": 2, "5〜6晩": 3, "毎晩": 4},
    {"全くなかった": 0, "少し": 1, "ある程度": 2, "とても": 3, "極めて": 4},
    {"全くなかった": 0, "少し": 1, "ある程度": 2, "とても": 3, "極めて": 4},
]

ADCT_OPTIONS_EN = [
    {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3, "Very severe": 4},
    {"Not at all": 0, "1–2 days": 1, "3–4 days": 2, "5–6 days": 3, "Every day": 4},
    {"Not at all": 0, "A little": 1, "Moderately": 2, "Very much": 3, "Extremely": 4},
    {"Not at all": 0, "1–2 nights": 1, "3–4 nights": 2, "5–6 nights": 3, "Every night": 4},
    {"Not at all": 0, "A little": 1, "Moderately": 2, "Very much": 3, "Extremely": 4},
    {"Not at all": 0, "A little": 1, "Moderately": 2, "Very much": 3, "Extremely": 4},
]


def get_secret(name: str, default: str | None = None) -> str | None:
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.getenv(name, default)


def t(language: str, ja: str, en: str) -> str:
    return ja if language == "日本語" else en


def interpret_dlqi(score: int, language: str) -> tuple[str, str]:
    if score <= 1:
        return t(language, "影響なし", "No effect"), t(language, "生活への明らかな影響はほとんどありません。", "No measurable effect on the patient's life.")
    if score <= 5:
        return t(language, "軽度の影響", "Small effect"), t(language, "生活への影響は軽度です。", "Small effect on the patient's life.")
    if score <= 10:
        return t(language, "中等度の影響", "Moderate effect"), t(language, "生活への影響は中等度です。", "Moderate effect on the patient's life.")
    if score <= 20:
        return t(language, "非常に大きな影響", "Very large effect"), t(language, "生活への影響は非常に大きい状態です。", "Very large effect on the patient's life.")
    return t(language, "極めて大きな影響", "Extremely large effect"), t(language, "生活への影響は極めて大きい状態です。", "Extremely large effect on the patient's life.")


def interpret_adct(score: int, language: str) -> tuple[str, str]:
    if score >= 7:
        return (
            t(language, "コントロール不十分の可能性", "Possible uncontrolled atopic dermatitis"),
            t(language, "ADCTが7点以上です。症状、睡眠、日常生活への影響を確認してください。", "ADCT is 7 or higher. Review symptoms, sleep, and daily-life impact."),
        )
    return (
        t(language, "比較的コントロール良好", "Relatively controlled"),
        t(language, "ADCTは7点未満です。通常診療で確認を継続してください。", "ADCT is below 7. Continue routine clinical assessment."),
    )


def get_csv_path(instrument: str) -> Path:
    return CSV_PATH_ADCT if instrument == "ADCT" else CSV_PATH_DLQI


def save_result(row: dict):
    csv_path = get_csv_path(row.get("instrument", ""))
    df = pd.DataFrame([row])

    if csv_path.exists():
        df.to_csv(csv_path, mode="a", header=False, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")


def get_previous_adct(patient_code: str):
    if not patient_code or not CSV_PATH_ADCT.exists():
        return None

    try:
        df = pd.read_csv(CSV_PATH_ADCT, on_bad_lines="skip")
    except Exception:
        return None

    if "visit_code" not in df.columns or "total_score" not in df.columns:
        return None

    df_ad = df[df["visit_code"].astype(str) == str(patient_code)]

    if df_ad.empty:
        return None

    last_row = df_ad.sort_values("timestamp").iloc[-1]
    return int(last_row["total_score"])


def judge_maintenance(current, previous, scores):
    if current >= 7:
        return "非維持"

    if len(scores) >= 4 and scores[3] >= 1:
        return "非維持"

    for i, s in enumerate(scores):
        if i == 3:
            continue
        if s >= 2:
            return "非維持"

    if previous is not None and (current - previous) >= 5:
        return "非維持"

    return "維持"


def build_email_body(row: dict, result: dict) -> str:
    lines = [
        "New questionnaire submission",
        "",
        f"App: {APP_TITLE}",
        f"Timestamp: {row.get('timestamp', '')}",
        f"Language: {row.get('language', '')}",
        f"Disease: {row.get('disease', '')}",
        f"Instrument: {row.get('instrument', '')}",
        f"Anonymous visit code: {row.get('visit_code', '') or '(blank)'}",
        f"Total score: {row.get('total_score', '')} / {row.get('max_score', '')}",
        f"Severity / interpretation: {row.get('severity', '')}",
        f"Decision: {row.get('decision', '')}",
        f"Previous ADCT: {row.get('previous_adct', '')}",
        f"Delta ADCT: {row.get('delta_adct', '')}",
        "",
        "Item scores:",
    ]

    for i, score in enumerate(result["scores"], start=1):
        answer = result["answers"][i - 1]
        lines.append(f"Q{i}: {score} | {answer}")

    lines.extend([
        "",
        "Note:",
        "This message is intended for clinical support only.",
        "No direct personal identifiers should be entered into this app.",
    ])
    return "\n".join(lines)


def send_admin_email(row: dict, result: dict) -> tuple[bool, str]:
    smtp_host = get_secret("SMTP_HOST")
    smtp_port = int(get_secret("SMTP_PORT", "587"))
    smtp_user = get_secret("SMTP_USER")
    smtp_password = get_secret("SMTP_PASSWORD")
    smtp_from = get_secret("SMTP_FROM", smtp_user or ADMIN_EMAIL)

    missing = [
        name for name, value in {
            "SMTP_HOST": smtp_host,
            "SMTP_USER": smtp_user,
            "SMTP_PASSWORD": smtp_password,
            "SMTP_FROM": smtp_from,
        }.items() if not value
    ]

    if missing:
        return False, "Missing email settings: " + ", ".join(missing)

    subject = f"[Shirabeo Patient Insight] New {row['instrument']} Submission: {row['total_score']}/{row['max_score']}"
    body = build_email_body(row, result)

    msg = MIMEMultipart()
    msg["From"] = smtp_from
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_from, [ADMIN_EMAIL], msg.as_string())
        return True, "Email sent successfully."
    except Exception as e:
        print("EMAIL ERROR:", e)
        return False, f"Email sending failed: {e}"


def render_dlqi(language: str):
    questions = DLQI_QUESTIONS_JA if language == "日本語" else DLQI_QUESTIONS_EN
    options_common = DLQI_OPTIONS_JA if language == "日本語" else DLQI_OPTIONS_EN
    q7_options = DLQI_Q7_OPTIONS_JA if language == "日本語" else DLQI_Q7_OPTIONS_EN

    scores = []
    answers = []

    for i, q in enumerate(questions, start=1):
        st.markdown(f"**Q{i}. {q}**")
        opts = q7_options if i == 7 else options_common
        answer = st.radio(
            t(language, f"Q{i}の回答", f"Answer Q{i}"),
            list(opts.keys()),
            key=f"dlqi_{language}_{i}",
            label_visibility="collapsed",
        )
        scores.append(opts[answer])
        answers.append(answer)
        st.write("")

    total = int(sum(scores))
    severity, interpretation = interpret_dlqi(total, language)

    return {
        "instrument": "DLQI",
        "disease": "Psoriasis",
        "total_score": total,
        "max_score": 30,
        "severity": severity,
        "interpretation": interpretation,
        "scores": scores,
        "answers": answers,
    }


def render_adct(language: str):
    questions = ADCT_QUESTIONS_JA if language == "日本語" else ADCT_QUESTIONS_EN
    options_list = ADCT_OPTIONS_JA if language == "日本語" else ADCT_OPTIONS_EN

    scores = []
    answers = []

    for i, q in enumerate(questions, start=1):
        st.markdown(f"**Q{i}. {q}**")
        opts = options_list[i - 1]
        answer = st.radio(
            t(language, f"Q{i}の回答", f"Answer Q{i}"),
            list(opts.keys()),
            key=f"adct_{language}_{i}",
            label_visibility="collapsed",
        )
        scores.append(opts[answer])
        answers.append(answer)
        st.write("")

    total = int(sum(scores))
    severity, interpretation = interpret_adct(total, language)

    return {
        "instrument": "ADCT",
        "disease": "Atopic dermatitis",
        "total_score": total,
        "max_score": 24,
        "severity": severity,
        "interpretation": interpretation,
        "scores": scores,
        "answers": answers,
    }


def show_csv_tab(label: str, csv_path: Path, file_name: str):
    st.subheader(label)

    if not csv_path.exists():
        st.info(f"{label}データはまだありません。")
        return

    csv_bytes = csv_path.read_bytes()
    st.download_button(
        f"{label} CSVダウンロード",
        data=csv_bytes,
        file_name=file_name,
        mime="text/csv",
        use_container_width=True,
    )

    try:
        df = pd.read_csv(csv_path, on_bad_lines="skip")
        st.dataframe(df.tail(30), use_container_width=True)
    except Exception as e:
        st.warning(f"{label} CSVの読み込みに失敗しました。")
        st.caption(str(e))


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="📝", layout="centered")

    st.title(APP_TITLE)
    st.caption("DLQI for psoriasis / ADCT for atopic dermatitis")

    language = st.sidebar.radio("Language / 言語", ["日本語", "English"], index=0)

    disease_mode = st.sidebar.radio(
        t(language, "疾患・質問票", "Disease / questionnaire"),
        [
            t(language, "乾癬：DLQI", "Psoriasis: DLQI"),
            t(language, "アトピー性皮膚炎：ADCT", "Atopic dermatitis: ADCT"),
        ],
        index=1,
    )

    st.info(
        t(
            language,
            "過去1週間を振り返って回答してください。氏名・生年月日・住所・患者IDなどの直接個人情報は入力しないでください。",
            "Please answer based on the last 7 days. Do not enter direct personal identifiers such as name, date of birth, address, or patient ID.",
        )
    )

    with st.form("questionnaire_form", clear_on_submit=False):
        visit_code = st.text_input(
            t(language, "匿名コード", "Anonymous visit code"),
            placeholder=t(language, "例：AD001。空欄でも可。", "Example: AD001. Optional."),
            help=t(language, "匿名コードのみ使用してください。氏名や患者IDは入力しないでください。", "Use an anonymous code only. Do not enter name or patient ID."),
        )

        st.divider()

        if "DLQI" in disease_mode:
            result = render_dlqi(language)
        else:
            result = render_adct(language)

        submitted = st.form_submit_button(
            t(language, "送信", "Submit"),
            use_container_width=True
        )

    if submitted:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        previous_adct = None
        delta_adct = None
        decision = ""

        if result["instrument"] == "ADCT":
            previous_adct = get_previous_adct(visit_code)
            decision = judge_maintenance(
                result["total_score"],
                previous_adct,
                result["scores"]
            )
            if previous_adct is not None:
                delta_adct = result["total_score"] - previous_adct

        row = {
            "timestamp": now,
            "language": language,
            "disease": result["disease"],
            "instrument": result["instrument"],
            "visit_code": visit_code,
            "total_score": result["total_score"],
            "max_score": result["max_score"],
            "severity": result["severity"],
            "previous_adct": previous_adct,
            "delta_adct": delta_adct,
            "decision": decision,
        }

        for i, score in enumerate(result["scores"], start=1):
            row[f"q{i}_score"] = score
            row[f"q{i}_answer"] = result["answers"][i - 1]

        save_result(row)
        send_to_google_form(row)
      

        st.success(t(language, "送信されました。", "Submitted successfully."))

        st.metric(
            result["instrument"] + " " + t(language, "合計点", "total score"),
            f"{result['total_score']} / {result['max_score']}",
        )

        if result["instrument"] == "ADCT":
            st.markdown("---")

            if decision == "維持":
                st.markdown(
                    "<h1 style='text-align:center; color:green;'>🟢 維持</h1>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<p style='text-align:center; font-size:20px;'>現在の治療維持が妥当と考えられます</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<h1 style='text-align:center; color:red;'>🔴 非維持</h1>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<p style='text-align:center; font-size:20px;'>状態の再評価を推奨します</p>",
                    unsafe_allow_html=True,
                )

            if previous_adct is not None:
                st.markdown(
                    f"<p style='text-align:center;'>ADCT: {result['total_score']}（前回 {previous_adct}） / Δ {delta_adct}</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<p style='text-align:center;'>ADCT: {result['total_score']}（初回）</p>",
                    unsafe_allow_html=True,
                )
        else:
            st.subheader(result["severity"])
            st.write(result["interpretation"])

    st.divider()

    show_admin = st.checkbox(
        t(language, "医療者モードを表示", "Show clinician mode")
    )

    if show_admin:
        with st.expander(
            t(language, "医療者用：CSV確認・ダウンロード", "Clinician view: CSV review and download")
        ):
            admin_password = st.text_input(
                t(language, "管理者パスワード", "Admin password"),
                type="password",
                help=t(language, "RenderのEnvironmentに ADMIN_PASSWORD を設定してください。", "Set ADMIN_PASSWORD in Render Environment."),
            )

            configured_password = get_secret("ADMIN_PASSWORD")

            if not configured_password:
                st.caption(
                    t(language, "ADMIN_PASSWORD が未設定のため、CSV閲覧は無効です。", "CSV view is disabled because ADMIN_PASSWORD is not configured.")
                )
            elif admin_password == configured_password:
                tab_adct, tab_dlqi = st.tabs(["ADCT", "DLQI"])

                with tab_adct:
                    show_csv_tab("ADCT", CSV_PATH_ADCT, "adct_results.csv")

                with tab_dlqi:
                    show_csv_tab("DLQI", CSV_PATH_DLQI, "dlqi_results.csv")

            elif admin_password:
                st.error(t(language, "パスワードが違います。", "Incorrect password."))

    st.caption(
        t(
            language,
            "このアプリは診療補助目的です。最終的な診療判断は医療者が行ってください。",
            "For clinical support only. Final clinical decisions should be made by a qualified clinician.",
        )
    )


if __name__ == "__main__":
    main()
