
import os
import html
import re
import requests
import streamlit as st
import joblib
from dotenv import load_dotenv

load_dotenv()

MODEL = "models/spam_classifier.joblib"

st.set_page_config(
    page_title="MailGuard AI | Email Security",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Theme selection
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "Dark"

st.session_state.app_theme = st.radio(
    "🎨 Interface theme",
    ["Dark", "Light"],
    horizontal=True,
    key="theme_selector",
    label_visibility="collapsed",
)

# -------------------- DESIGN --------------------

css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b1020;
    --panel: #111a2e;
    --border: #27334b;
    --text: #f3f6ff;
    --muted: #9aa8c2;
    --purple: #9b87ff;
    --blue: #60a5fa;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, #25204b 0%, transparent 35%),
        radial-gradient(ellipse at 95% 15%, #102c4b 0%, transparent 30%),
        #0b1020;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, p, label {
    font-family: 'Inter', sans-serif !important;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 32px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 15px;
    background: linear-gradient(135deg, #8b5cf6, #3b82f6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    box-shadow: 0 8px 28px #5b4ad044;
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
    color: #f5f7ff;
    letter-spacing: -0.7px;
}

.brand-sub {
    color: #9aa8c2;
    font-size: 12px;
    margin-top: 2px;
}

.top-pill {
    display: inline-block;
    color: #c4b5fd;
    background: #8b5cf620;
    border: 1px solid #8b5cf655;
    border-radius: 30px;
    padding: 7px 13px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 15px;
}

.hero-title {
    font-size: clamp(34px, 5vw, 52px);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -1.8px;
    color: #f7f8ff;
    margin: 0 0 14px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    font-size: 15px;
    line-height: 1.8;
    color: #a5b2ca;
    max-width: 690px;
    margin-bottom: 25px;
}

.feature-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 18px 0 30px 0;
}

.feature {
    color: #cbd5e1;
    font-size: 12px;
    padding: 9px 13px;
    border-radius: 9px;
    background: #ffffff08;
    border: 1px solid #ffffff12;
}

.panel {
    background: linear-gradient(145deg, #141e34, #101729);
    border: 1px solid #293650;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 12px 35px #00000012;
}

.panel-title {
    font-size: 19px;
    font-weight: 700;
    color: #f1f5ff;
    margin-bottom: 5px;
}

.panel-subtitle {
    color: #98a7c1;
    font-size: 12px;
    line-height: 1.6;
    margin-bottom: 20px;
}

.section-label {
    color: #a5b4fc;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #0b1222 !important;
    color: #f3f6ff !important;
    border: 1px solid #2b3955 !important;
    border-radius: 10px !important;
    font-size: 14px !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 1px #8b5cf6 !important;
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label {
    color: #dbe4f5 !important;
    font-weight: 600 !important;
}

.stButton > button {
    border-radius: 10px;
    min-height: 48px;
    font-weight: 700;
    border: 1px solid #9b87ff;
    background: linear-gradient(100deg, #7c3aed, #4f7df3);
    color: white;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: #c4b5fd;
    box-shadow: 0 5px 25px #8b5cf640;
    color: white;
    transform: translateY(-1px);
}

div[data-testid="stCheckbox"] label {
    color: #cbd5e1 !important;
    font-size: 13px;
}

.result-card {
    border-radius: 16px;
    padding: 23px;
    margin: 12px 0 18px 0;
    border: 1px solid;
}

.result-spam {
    background: linear-gradient(120deg, #451a2a66, #211526);
    border-color: #fb718555;
}

.result-safe {
    background: linear-gradient(120deg, #064e3b66, #10251f);
    border-color: #34d39955;
}

.result-heading {
    font-size: 23px;
    font-weight: 800;
    margin: 8px 0;
}

.result-caption {
    color: #bdc9dc;
    font-size: 13px;
    line-height: 1.7;
}

.result-icon {
    font-size: 27px;
}

.metric-card {
    background: #0b1222;
    border: 1px solid #293650;
    border-radius: 13px;
    padding: 17px;
    min-height: 95px;
}

.metric-label {
    color: #98a7c1;
    font-size: 12px;
    margin-bottom: 10px;
}

.metric-value {
    color: #f3f6ff;
    font-size: 25px;
    font-weight: 800;
}

.explanation-card {
    background: #111b30;
    border: 1px solid #30405f;
    border-left: 4px solid #9b87ff;
    border-radius: 12px;
    padding: 20px;
    color: #d9e2f3;
    font-size: 14px;
    line-height: 1.9;
    margin: 12px 0;
}

.ai-badge {
    display: inline-block;
    background: #8b5cf620;
    border: 1px solid #8b5cf655;
    border-radius: 20px;
    color: #c4b5fd;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 10px;
}

.tip-card {
    background: #172033;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 17px;
    color: #cbd5e1;
    font-size: 12px;
    line-height: 1.8;
    margin-top: 15px;
}

.footer {
    border-top: 1px solid #26334b;
    padding-top: 20px;
    margin-top: 35px;
    color: #8290aa;
    font-size: 11px;
    line-height: 1.9;
    text-align: center;
}

div[data-testid="stAlert"] {
    border-radius: 10px;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .panel {
        padding: 17px;
    }
}
</style>
"""

# Light-mode overrides: replace the fixed dark colors used by the original design.
if st.session_state.app_theme == "Light":
    css = css.replace(
        """background:
        radial-gradient(ellipse at 15% 0%, #25204b 0%, transparent 35%),
        radial-gradient(ellipse at 95% 15%, #102c4b 0%, transparent 30%),
        #0b1020;""",
        """background:
        radial-gradient(ellipse at 15% 0%, #eee9ff 0%, transparent 35%),
        radial-gradient(ellipse at 95% 15%, #e5f1ff 0%, transparent 30%),
        #f4f7fc;"""
    )
    css += """
<style>
.stApp { color: #172033 !important; }
.brand-name, .hero-title, .panel-title, .metric-value,
.result-heading { color: #172033 !important; }
.brand-sub, .hero-description, .panel-subtitle,
.result-caption, .metric-label, .footer { color: #526078 !important; }
.feature {
    color: #344054 !important;
    background: #ffffff !important;
    border-color: #dbe3ef !important;
}
.panel {
    background: #ffffff !important;
    border-color: #d5deeb !important;
    box-shadow: 0 12px 35px #1d35570d !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    color: #172033 !important;
    border-color: #cbd5e1 !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stCheckbox"] label {
    color: #344054 !important;
}
.metric-card {
    background: #f8faff !important;
    border-color: #d5deeb !important;
}
.metric-value { color: #172033 !important; }
.explanation-card {
    background: #f8faff !important;
    border-color: #d5deeb !important;
    border-left-color: #8b5cf6 !important;
    color: #344054 !important;
}
.tip-card {
    background: #f8faff !important;
    border-color: #d5deeb !important;
    color: #344054 !important;
}
.result-spam {
    background: linear-gradient(120deg, #fff1f2, #fff7f7) !important;
    border-color: #fda4af !important;
}
.result-safe {
    background: linear-gradient(120deg, #ecfdf5, #f4fff9) !important;
    border-color: #6ee7b7 !important;
}
.result-caption { color: #475569 !important; }
.footer { border-top-color: #d5deeb !important; }\n.stApp { --empty-heading: #172033; --empty-muted: #526078; }
.top-pill {
    color: #6d28d9 !important;
    background: #f3e8ff !important;
    border-color: #d8b4fe !important;
}
.section-label { color: #6d28d9 !important; }
div[data-testid="stRadio"] label { color: #344054 !important; }
</style>
"""
else:
    css += """
<style>
div[data-testid="stRadio"] label { color: #dbe4f5 !important; }
</style>
"""

st.markdown(css, unsafe_allow_html=True)


# -------------------- MODEL --------------------

@st.cache_resource
def load_model():
    return joblib.load(MODEL) if os.path.exists(MODEL) else None


def local_explanation(text, prediction, confidence):
    low = text.lower()

    signs = {
        "urgent or time-pressure language": [
            "urgent", "immediately", "act now", "expires today"
        ],
        "prize or money claims": [
            "winner", "won", "prize", "cash", "lottery", "claim your"
        ],
        "sensitive information requests": [
            "password", "otp", "bank details", "credit card",
            "verify your account"
        ],
        "suspicious link wording": [
            "click here", "http://", "bit.ly", "tinyurl"
        ],
        "unsolicited offers": [
            "free", "discount", "earn money", "work from home"
        ],
    }

    found = [
        name for name, words in signs.items()
        if any(word in low for word in words)
    ]

    if prediction == "Spam":
        result = "The machine-learning model classified this email as likely spam."
        if found:
            result += " Potential warning signs include: " + ", ".join(found) + "."
        result += (
            " Avoid clicking unknown links or sharing passwords, OTPs, "
            "or banking details."
        )
    else:
        result = (
            "The machine-learning model classified this email as likely not spam. "
            "This prediction does not guarantee that the email is safe."
        )
        if found:
            result += (
                " Please review these possible warning signs: "
                + ", ".join(found) + "."
            )

    if confidence is not None:
        result += f" Model confidence for this prediction: {confidence:.1%}."

    return result


def clean_ai_explanation(text):
    """Remove escaped Markdown markers that sometimes appear in Gemini output."""
    text = text.replace("\\\\", "")
    text = re.sub(r"^\s*#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"^\s*[-*]\s+", "• ", text, flags=re.MULTILINE)
    return text.strip()


# -------------------- GEMINI AI --------------------

def ask_gemini(text, prediction, confidence):
    key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv(
        "GEMINI_MODEL", "gemini-3.1-flash-lite"
    ).strip()

    if not key:
        return None, "No Gemini API key configured. Showing the built-in explanation."

    conf = f"{confidence:.1%}" if confidence is not None else "not available"

    prompt = f"""
You are an email safety assistant helping a non-technical user.

A machine-learning model predicted: {prediction}.
Model confidence for this prediction: {conf}.

Explain the email in simple, clear language:
1. Briefly summarize what the email appears to be about.
2. Point out suspicious wording or explain why it appears ordinary.
3. Give practical safety advice if needed.

Do not claim a link is malicious without evidence.
Do not treat the machine-learning prediction as proof.
Mention that automated predictions can be wrong.
Keep the response concise and easy to understand.

Email:
{text[:5000]}
"""

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            params={"key": key},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 450,
                },
            },
            timeout=90,
        )

        if response.status_code != 200:
            return None, (
                f"Gemini API returned HTTP {response.status_code}. "
                "Showing the built-in explanation instead."
            )

        data = response.json()
        candidates = data.get("candidates", [])

        if not candidates:
            return None, "Gemini did not return an explanation. Using the built-in version."

        parts = candidates[0].get("content", {}).get("parts", [])
        explanation = " ".join(
            part.get("text", "") for part in parts if part.get("text")
        ).strip()

        if not explanation:
            return None, "Gemini returned an empty response. Using the built-in version."

        return explanation, None

    except Exception as error:
        return None, (
            f"Gemini is temporarily unavailable ({type(error).__name__}). "
            "Showing the built-in explanation instead."
        )


# -------------------- HEADER --------------------

st.markdown("""
<div class="brand">
    <div class="brand-icon">📧</div>
    <div>
        <div class="brand-name">MailGuard <span class="gradient-text">AI</span></div>
        <div class="brand-sub">INTELLIGENT EMAIL SECURITY</div>
    </div>
</div>

<div class="top-pill">✦ MACHINE LEARNING + GENERATIVE AI</div>

<div class="hero-title">
    Your inbox,<br>
    <span class="gradient-text">protected by intelligence.</span>
</div>

<div class="hero-description">
    Analyze suspicious emails in seconds. Our machine-learning model
    detects potential spam, while Generative AI explains the result
    in language that's easy to understand.
</div>

<div class="feature-row">
    <div class="feature">🧠 ML-powered detection</div>
    <div class="feature">✨ AI explanations</div>
    <div class="feature">🛡️ Security awareness</div>
    <div class="feature">⚡ Instant analysis</div>
</div>
""", unsafe_allow_html=True)


# -------------------- CHECK MODEL --------------------

clf = load_model()

if clf is None:
    st.error("Trained model not found.")
    st.markdown(
        "Run the training script from your project directory, then restart this app."
    )
    st.code("py train_model.py\npy -m streamlit run app.py")
    st.stop()


# -------------------- MAIN INPUT --------------------

left, right = st.columns([1.08, 0.92], gap="large")

with left:
    st.markdown("""
    <div class="panel">
        <div class="section-label">01 / EMAIL ANALYZER</div>
        <div class="panel-title">Inspect an email</div>
        <div class="panel-subtitle">
            Paste the subject and message below to check for potential spam.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        subject = st.text_input(
            "Email subject",
            placeholder="e.g. Congratulations! Claim your reward",
        )

        body = st.text_area(
            "Email message",
            placeholder="Paste the complete email content here...",
            height=235,
        )

        use_ai = st.checkbox(
            "Generate an AI explanation using Gemini",
            value=True,
        )

        analyze = st.button(
            "🔍  Analyze Email",
            type="primary",
            use_container_width=True,
        )

    st.markdown("""
    <div class="tip-card">
        <b>🔒 Privacy reminder</b><br>
        Avoid pasting real passwords, OTPs, bank details, or other
        sensitive personal information into the analyzer.
    </div>
    """, unsafe_allow_html=True)


with right:
    st.markdown("""
    <div class="panel">
        <div class="section-label">02 / ANALYSIS RESULTS</div>
        <div class="panel-title">Your security report</div>
        <div class="panel-subtitle">
            Your prediction and explanation will appear here after analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if analyze:
        email = (subject.strip() + "\n" + body.strip()).strip()

        if not email:
            st.warning("Please enter an email subject or message.")
        else:
            with st.spinner("Analyzing email content..."):
                prediction = clf.predict([email])[0]

                confidence = None
                if hasattr(clf, "predict_proba"):
                    probabilities = clf.predict_proba([email])[0]
                    confidence = float(
                        probabilities[list(clf.classes_).index(prediction)]
                    )

                explanation = None
                note = None
                explanation_source = "Built-in explanation"

                if use_ai:
                    with st.spinner("Preparing your AI explanation..."):
                        explanation, note = ask_gemini(
                            email, prediction, confidence
                        )

                    if explanation:
                        explanation_source = "Gemini AI explanation"

                if not explanation:
                    explanation = local_explanation(
                        email, prediction, confidence
                    )

            if prediction == "Spam":
                st.markdown("""
                <div class="result-card result-spam">
                    <div class="result-icon">🚨</div>
                    <div class="result-heading">Potential Spam Detected</div>
                    <div class="result-caption">
                        This email has been classified as spam by the
                        machine-learning model. Be careful before interacting
                        with its links or attachments.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-card result-safe">
                    <div class="result-icon">🛡️</div>
                    <div class="result-heading">Likely Not Spam</div>
                    <div class="result-caption">
                        The model classified this email as not spam.
                        This does not guarantee that the sender or email is safe.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            metric_col1, metric_col2 = st.columns(2)

            with metric_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">MODEL PREDICTION</div>
                    <div class="metric-value">{html.escape(str(prediction))}</div>
                </div>
                """, unsafe_allow_html=True)

            with metric_col2:
                confidence_text = (
                    f"{confidence:.1%}" if confidence is not None else "N/A"
                )
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">CLASS CONFIDENCE</div>
                    <div class="metric-value">{confidence_text}</div>
                </div>
                """, unsafe_allow_html=True)

            if confidence is not None:
                st.progress(max(0.0, min(1.0, confidence)))
                st.caption(
                    "Confidence is the model's estimated support for its "
                    "selected class, not a guarantee of correctness."
                )

            st.markdown("""
            <div style="margin-top:25px;">
                <div class="section-label">03 / INTELLIGENT INSIGHTS</div>
                <div class="panel-title">Why this result?</div>
            </div>
            """, unsafe_allow_html=True)

            safe_explanation = html.escape(
                clean_ai_explanation(explanation)
            ).replace("\\n", "<br>")

            st.markdown(
                f"""
                <div class="explanation-card">
                    <div class="ai-badge">✦ {html.escape(explanation_source)}</div>
                    <div>{safe_explanation}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if note:
                st.info(note)

            st.warning(
                "Safety first: never share passwords, OTPs, or banking "
                "details based only on an email. Verify important requests "
                "through an official website or known contact."
            )

    else:
        st.markdown("""
        <div class="panel" style="text-align:center; padding:35px 20px;">
            <div style="font-size:48px; margin:12px 0 20px 0;">🔎</div>
            <div style="font-size:18px; font-weight:700; color:var(--empty-heading, #e7ecf8);">
                Ready to analyze
            </div>
            <div style="font-size:13px; line-height:1.8; color:var(--empty-muted, #9aa8c2);
                        margin-top:10px;">
                Your spam prediction, confidence score and intelligent
                explanation will appear here.
            </div>
            <div style="margin-top:24px; color:#a5b4fc; font-size:12px;">
                Paste an email and click Analyze Email to get started.
            </div>
        </div>
        """, unsafe_allow_html=True)


# -------------------- HOW IT WORKS --------------------

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("⚙️  How MailGuard AI works"):
    st.markdown("""
    **Step 1 — Text processing:** The trained TF-IDF pipeline converts email
    text into numerical features.

    **Step 2 — Spam classification:** The saved machine-learning model predicts
    whether the email is Spam or Not Spam.

    **Step 3 — Confidence score:** If supported by the model, the app displays
    its estimated confidence for the selected class.

    **Step 4 — Intelligent explanation:** Gemini explains possible warning signs
    in simple language. If Gemini is unavailable, a built-in explanation is used.

    **Important:** This is an academic prototype. Model predictions can be wrong,
    and confidence scores do not prove that an email is safe.
    """)

st.markdown("""
<div class="footer">
    <b>MailGuard AI</b> · Academic MCA Project<br>
    Machine Learning + Generative AI · Built with Python and Streamlit<br>
    For educational demonstration only — not a replacement for professional email security.
</div>
""", unsafe_allow_html=True)
