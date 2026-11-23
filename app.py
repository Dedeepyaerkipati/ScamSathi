from __future__ import annotations

import html
import streamlit as st

from detection.message_detector import analyze_message, is_model_available
from detection.ocr import extract_text_from_image
from detection.translations import (
    localized_advice, localized_category, localized_indicator,
    localized_risk, ui,
)

st.set_page_config(
    page_title="ScamSathi | Digital Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root{
  --navy:#101d32;--navy2:#172944;--teal:#19b6a0;
  --app-bg:var(--background-color,#f3f6fa);
  --card-bg:var(--secondary-background-color,#ffffff);
  --app-text:var(--text-color,#17263c);
  --app-muted:color-mix(in srgb,var(--app-text) 62%,transparent);
  --app-line:color-mix(in srgb,var(--app-text) 16%,transparent);
}
.stApp{background:var(--app-bg)!important;color:var(--app-text)!important;overflow-x:hidden}
[data-testid="stAppViewContainer"],.main{background:var(--app-bg)!important;color:var(--app-text)!important}
[data-testid="stHeader"]{background:var(--app-bg)!important}
.block-container{width:100%!important;max-width:100%!important;min-width:0!important;margin:0!important;padding:1.5rem clamp(.8rem,2.6vw,2.2rem) 3rem!important;box-sizing:border-box!important}
div[data-testid="column"],div[data-testid="stHorizontalBlock"]{min-width:0!important;max-width:100%;box-sizing:border-box}
/* Keep the branded sidebar intentionally dark in both app themes. */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#101d32 0%,#172944 100%)!important;border-right:1px solid rgba(255,255,255,.10)}
section[data-testid="stSidebar"] *{color:#e9f1fa}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{color:#a9b9cc!important}
section[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.14)}
.hero{width:100%;box-sizing:border-box;background:linear-gradient(115deg,#101d32 0%,#1a3654 70%,#126d70 125%);border-radius:22px;padding:30px 34px;color:#fff;box-shadow:0 14px 35px rgba(16,29,50,.13);margin-bottom:24px;overflow:hidden}
.hero-kicker{color:#76e5d2;text-transform:uppercase;letter-spacing:2px;font-size:.72rem;font-weight:800;margin-bottom:8px}
.hero-title{color:#fff!important;font-size:clamp(1.8rem,4vw,2.65rem);line-height:1.12;font-weight:800;margin:0 0 9px}
.hero-subtitle{color:#d0dceb!important;font-size:1rem;max-width:850px;margin:0;overflow-wrap:anywhere}
.hero-pill{display:inline-block;margin-top:17px;background:rgba(25,182,160,.14);border:1px solid rgba(118,229,210,.3);color:#9af0e1!important;padding:6px 11px;border-radius:30px;font-size:.76rem;font-weight:700}
.section-heading{color:var(--app-text)!important;font-size:1.18rem;font-weight:800;margin:5px 0 3px}
.section-subheading{color:var(--app-muted)!important;font-size:.88rem;margin-bottom:13px;overflow-wrap:anywhere}
.feature-card{height:100%;width:100%;box-sizing:border-box;background:var(--card-bg);color:var(--app-text);border:1px solid var(--app-line);border-radius:15px;padding:16px 17px;box-shadow:0 4px 13px rgba(25,42,70,.035)}
.feature-icon{font-size:1.25rem;margin-bottom:7px}.feature-title{color:var(--app-text)!important;font-weight:800;font-size:.91rem;margin-bottom:4px}.feature-copy{color:var(--app-muted)!important;font-size:.79rem;line-height:1.45}
/* Labels and form controls follow the selected Streamlit theme. */
.stApp label,.stApp [data-testid="stWidgetLabel"] p{color:var(--app-text)!important;font-weight:650!important}
.stTextArea textarea,.stTextInput input,.stNumberInput input{background:var(--secondary-background-color)!important;color:var(--text-color)!important;border:1px solid var(--app-line)!important;border-radius:13px!important;padding:15px!important;line-height:1.55!important;width:100%!important;max-width:100%!important;box-sizing:border-box!important}
.stTextArea textarea::placeholder,.stTextInput input::placeholder{color:var(--app-muted)!important;opacity:1}
.stTextArea textarea:focus,.stTextInput input:focus,.stNumberInput input:focus{border-color:#19b6a0!important;box-shadow:0 0 0 3px rgba(25,182,160,.16)!important}
/* Make primary, secondary, upload and form buttons readable in both themes. */
div.stButton>button[kind="primary"],.stFormSubmitButton>button{background:linear-gradient(90deg,#087f78,#119b8b)!important;color:#fff!important;border:1px solid #087f78!important;border-radius:12px!important;min-height:46px;font-weight:800!important;box-shadow:0 7px 16px rgba(8,127,120,.18)}
div.stButton>button[kind="primary"]:hover,.stFormSubmitButton>button:hover{background:linear-gradient(90deg,#066b66,#0b8276)!important;border-color:#066b66!important;color:#fff!important}
div.stButton>button:not([kind="primary"]){background:var(--secondary-background-color)!important;color:var(--text-color)!important;border-radius:10px!important;border:1px solid var(--app-line)!important;min-height:42px}
div.stButton>button:not([kind="primary"]):hover{border-color:#19b6a0!important;color:var(--text-color)!important;background:color-mix(in srgb,var(--secondary-background-color) 88%,#19b6a0 12%)!important}
div.stButton>button:disabled{opacity:.48!important;color:var(--app-muted)!important;cursor:not-allowed!important}
[data-testid="stFileUploader"] section{background:var(--secondary-background-color)!important;border:1px solid var(--app-line)!important}
[data-testid="stFileUploader"] button{background:var(--secondary-background-color)!important;color:var(--text-color)!important;border:1px solid var(--app-line)!important}
[data-testid="stSelectbox"] div[data-baseweb="select"]>div{background:var(--secondary-background-color)!important;color:var(--text-color)!important;border-color:var(--app-line)!important}
[data-testid="stRadio"] label{color:var(--app-text)!important}
.risk-banner{width:100%;box-sizing:border-box;border-radius:15px;padding:17px 20px;border:1px solid;margin:8px 0 16px}
.risk-high{background:color-mix(in srgb,#ef4444 11%,var(--card-bg));border-color:color-mix(in srgb,#ef4444 35%,var(--app-line))}.risk-medium{background:color-mix(in srgb,#f59e0b 12%,var(--card-bg));border-color:color-mix(in srgb,#f59e0b 38%,var(--app-line))}.risk-low{background:color-mix(in srgb,#10b981 11%,var(--card-bg));border-color:color-mix(in srgb,#10b981 35%,var(--app-line))}
.risk-label{font-size:1.25rem;font-weight:850;margin-bottom:3px;color:var(--app-text)!important}.risk-detail{font-size:.88rem;color:var(--app-muted)!important;line-height:1.45}
.metric-card{width:100%;max-width:100%;min-width:0;box-sizing:border-box;overflow-wrap:anywhere;background:var(--card-bg);color:var(--app-text);border:1px solid var(--app-line);border-radius:14px;padding:14px 12px;min-height:88px}
.metric-label{color:var(--app-muted)!important;font-size:.72rem;font-weight:700}.metric-value{color:var(--app-text)!important;font-size:1.55rem;font-weight:850;margin-top:2px}.metric-note{color:var(--app-muted)!important;font-size:.72rem}
.indicator-card,.url-card{width:100%;box-sizing:border-box;background:var(--card-bg);color:var(--app-text);border:1px solid var(--app-line);border-left:4px solid #e6a23c;border-radius:11px;padding:12px 14px;margin:8px 0;overflow-wrap:anywhere}
.indicator-title{font-weight:800;color:var(--app-text)!important;margin-bottom:3px}.indicator-copy{color:var(--app-muted)!important;font-size:.84rem;line-height:1.45}
.url-card{background:var(--secondary-background-color);border-left:1px solid var(--app-line)}.url-text{color:#16a895!important;font-weight:750;font-family:monospace;font-size:.87rem;overflow-wrap:anywhere}.url-note{color:var(--app-muted)!important;font-size:.8rem;margin-top:4px}
.footer-note{color:var(--app-muted)!important;font-size:.75rem;line-height:1.5;margin-top:14px}
/* Streamlit messages and captions should not fade into either background. */
.stCaption,.stMarkdown p,.stMarkdown li{overflow-wrap:anywhere}
[data-testid="stAlert"]{color:var(--app-text)!important}
@media(max-width:700px){.block-container{padding:1rem .7rem 2rem!important}.hero{padding:23px 20px}}
</style>
""", unsafe_allow_html=True)


def metric_card(label: str, value: str, note: str) -> str:
    return (
        '<div class="metric-card">'
        f'<div class="metric-label">{html.escape(label)}</div>'
        f'<div class="metric-value">{html.escape(value)}</div>'
        f'<div class="metric-note">{html.escape(note)}</div>'
        '</div>'
    )


def render_result(result: dict, message: str, language: str) -> None:
    strings = ui(language)
    risk_styles = {
        "High risk": ("risk-high", "🔴", "Treat this message as dangerous until independently verified." if language == "en" else "ఈ సందేశాన్ని స్వతంత్రంగా నిర్ధారించే వరకు ప్రమాదకరంగా పరిగణించండి."),
        "Needs verification": ("risk-medium", "🟠", "Pause and verify the sender before clicking or replying." if language == "en" else "లింక్ తెరవడానికి లేదా సమాధానం ఇవ్వడానికి ముందు పంపిన వ్యక్తిని నిర్ధారించండి."),
        "No obvious warning detected": ("risk-low", "🟢", "No configured warning pattern was found; this is not a safety guarantee." if language == "en" else "సెట్ చేసిన హెచ్చరిక నమూనా కనిపించలేదు; అయినా ఇది భద్రతకు హామీ కాదు."),
    }
    risk_class, symbol, guidance = risk_styles.get(result["risk_level"], risk_styles["Needs verification"])
    st.markdown(f'<div class="section-heading">{html.escape(strings["results"])}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="risk-banner {risk_class}"><div class="risk-label">{symbol} {html.escape(localized_risk(result["risk_level"], language))}</div>'
        f'<div class="risk-detail">{html.escape(guidance)}</div></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="medium")
    cols[0].markdown(metric_card("RISK INDICATOR SCORE" if language == "en" else "ప్రమాద సూచిక స్కోరు", f'{result["score"]}/100', "Combined indicator score; not a probability" if language == "en" else "ఇది కలిపిన సూచిక స్కోరు; సంభావ్యత కాదు"), unsafe_allow_html=True)
    cols[1].markdown(metric_card("WARNING SIGNS" if language == "en" else "హెచ్చరికలు", str(len(result["indicators"])), "Patterns matched" if language == "en" else "గుర్తించిన నమూనాలు"), unsafe_allow_html=True)
    cols[2].markdown(metric_card("LINKS FOUND" if language == "en" else "లింకులు", str(len(result["urls"])), "Not reputation-checked" if language == "en" else "లింక్ భద్రత ప్రత్యక్షంగా తనిఖీ కాలేదు"), unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f'**🤖 {strings["ml"]}**')
        if result.get("ml_available") and result.get("ml_spam_probability") is not None:
            spam_pct = float(result["ml_spam_probability"]) * 100
            prediction = ("Likely spam" if result.get("ml_label") == "spam" else "Likely legitimate (ham)") if language == "en" else ("స్పామ్ అయ్యే అవకాశం" if result.get("ml_label") == "spam" else "సాధారణ సందేశం (హామ్) అయ్యే అవకాశం")
            st.write(f'**{"Model prediction" if language == "en" else "మోడల్ అంచనా"}:** {prediction}')
            st.progress(max(0.0, min(1.0, float(result["ml_spam_probability"]))))
            note = (f"Estimated spam likelihood: {spam_pct:.1f}%. This is a model estimate, not a guarantee. The model was trained on an English SMS dataset." if language == "en" else f"స్పామ్ అయ్యే మోడల్ అంచనా: {spam_pct:.1f}%. ఇది అంచనా మాత్రమే, హామీ కాదు. మోడల్ ఇంగ్లీష్ SMS డేటాపై శిక్షణ పొందింది.")
            st.caption(note)
        else:
            st.info("ML model not found. Run `python train_model.py`." if language == "en" else "ML మోడల్ కనిపించలేదు. `python train_model.py` అమలు చేయండి.")

    with st.container(border=True):
        st.markdown(f'**{strings["category"]}**')
        st.write(localized_category(result["category"], language))
        if language == "en":
            st.write(result["summary"])
        else:
            ml_sentence = "ML మోడల్ ఈ సందేశాన్ని స్పామ్‌గా గుర్తించింది." if result.get("ml_label") == "spam" else "ML మోడల్ ఈ సందేశాన్ని సాధారణ సందేశంగా గుర్తించింది." if result.get("ml_label") == "ham" else "ML మోడల్ అందుబాటులో లేదు."
            st.write(f'రూల్ తనిఖీలో {len(result["indicators"])} హెచ్చరిక(లు) కనిపించాయి. {ml_sentence} ఈ ఫలితం మార్గదర్శకం మాత్రమే; ఖచ్చితమైన నిర్ధారణ కాదు.')

    st.markdown(f'### 🔎 {strings["why"]}')
    if result["indicators"]:
        for item in result["indicators"]:
            item_display = localized_indicator(item, language)
            title = html.escape(str(item_display.get("label_display", item["label"])))
            explanation = html.escape(str(item_display.get("explanation_display", item["explanation"])))
            st.markdown(f'<div class="indicator-card"><div class="indicator-title">{title}</div><div class="indicator-copy">{explanation}</div></div>', unsafe_allow_html=True)
    else:
        st.info("No configured warning patterns were detected. This does not prove the message is genuine." if language == "en" else "సెట్ చేసిన హెచ్చరిక నమూనాలు కనిపించలేదు. దీనివల్ల సందేశం నిజమైనదని నిర్ధారణ కాదు.")

    if result["urls"]:
        st.markdown("### 🔗 Links found" if language == "en" else "### 🔗 గుర్తించిన లింకులు")
        for item in result["urls"]:
            st.markdown(f'<div class="url-card"><div class="url-text">{html.escape(str(item["url"]))}</div><div class="url-note">{html.escape(str(item["note"]))}</div></div>', unsafe_allow_html=True)

    st.markdown(f'### 🧭 {strings["advice"]}')
    for advice in result["advice"]:
        st.markdown(f'- {localized_advice(advice, language)}')

    with st.expander("View submitted message" if language == "en" else "మీరు సమర్పించిన సందేశం చూడండి"):
        st.code(message, language=None)
    st.caption("ScamSathi is advisory. It does not access SMS, WhatsApp or bank accounts, and it does not verify live website reputation. Never share OTPs, UPI PINs or passwords." if language == "en" else "ScamSathi సూచనలు మాత్రమే ఇస్తుంది. ఇది SMS, WhatsApp లేదా బ్యాంక్ ఖాతాలను యాక్సెస్ చేయదు; వెబ్‌సైట్ భద్రతను ప్రత్యక్షంగా నిర్ధారించదు. OTP, UPI PIN లేదా పాస్‌వర్డ్ పంచుకోవద్దు.")


# Sidebar
with st.sidebar:
    st.markdown("<div style='font-size:2rem;margin:8px 0 2px'>🛡️</div><div style='font-size:1.4rem;font-weight:850'>ScamSathi</div><div style='color:#a9b9cc;font-size:.82rem;margin:4px 0 18px'>Your digital safety companion</div>", unsafe_allow_html=True)
    language_choice = st.selectbox("Explanation language / వివరణ భాష", ["English", "తెలుగు (Telugu)"])
    language = "te" if language_choice.startswith("తెలుగు") else "en"
    strings = ui(language)
    st.divider()
    page = st.radio("WORKSPACE", ["Message Scanner", "About ScamSathi"])
    st.divider()
    if is_model_available():
        st.success("ML model: trained and loaded")
    else:
        st.warning("ML model: training required")
    st.caption("PROTOTYPE v1.0 • Advisory only")
    st.caption("Your message is analyzed only when you submit it.")

if page == "Message Scanner":
    st.markdown(
        f"<div class='hero'><div class='hero-kicker'>AI-assisted digital protection</div>"
        f"<div class='hero-title'>{html.escape(strings['title'])}</div>"
        f"<p class='hero-subtitle'>{html.escape(strings['subtitle'])}</p>"
        f"<span class='hero-pill'>🛡️ Check before you trust</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="section-heading">{html.escape(strings["input"])}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subheading">{html.escape(strings["privacy"])}</div>', unsafe_allow_html=True)

    # OCR controls appear before the text area so extracted text can be placed in widget state safely.
    with st.container(border=True):
        uploaded = st.file_uploader(strings["upload"], type=["png", "jpg", "jpeg", "webp"], help="OCR is performed locally with Tesseract; images are not uploaded to an external OCR service.")
        ocr_col, use_col = st.columns([1, 1])
        with ocr_col:
            extract_clicked = st.button(strings["extract"], disabled=uploaded is None, use_container_width=True)
        with use_col:
            use_clicked = st.button(strings["use_text"], disabled=not bool(st.session_state.get("ocr_text")), use_container_width=True)
        if extract_clicked and uploaded is not None:
            try:
                extracted = extract_text_from_image(uploaded.getvalue())
                st.session_state["ocr_text"] = extracted
                if extracted:
                    st.success("Text extracted. Review it before scanning." if language == "en" else "టెక్స్ట్ తీసుకున్నాం. స్కాన్ చేయడానికి ముందు పరిశీలించండి.")
                    st.text_area("OCR preview", value=extracted, height=110, disabled=True)
                else:
                    st.warning(strings["empty_ocr"])
            except RuntimeError as exc:
                st.error(str(exc))
            except ValueError as exc:
                st.error(str(exc))
        if use_clicked:
            st.session_state["message_input"] = st.session_state.get("ocr_text", "")
            st.session_state.pop("last_result", None)
            st.session_state.pop("last_message", None)
            st.rerun()

        message = st.text_area(
            strings["input"],
            height=175,
            placeholder="Paste the SMS, WhatsApp message or email text here..." if language == "en" else "SMS, WhatsApp లేదా ఈమెయిల్ సందేశాన్ని ఇక్కడ పేస్ట్ చేయండి...",
            key="message_input",
            label_visibility="collapsed",
        )
        scan = st.button(strings["scan"] + "  🔍", type="primary", use_container_width=True)
        st.caption("You choose what to submit. ScamSathi does not connect to your messaging or banking apps.")

    if scan:
        if not message.strip():
            st.warning("Please paste or extract a message before scanning." if language == "en" else "స్కాన్ చేయడానికి ముందు సందేశాన్ని పేస్ట్ చేయండి లేదా OCR ద్వారా తీసుకోండి.")
            st.session_state.pop("last_result", None)
            st.session_state.pop("last_message", None)
        else:
            with st.spinner("Analyzing warning patterns and ML signals..." if language == "en" else "హెచ్చరిక నమూనాలు మరియు ML సంకేతాలను పరిశీలిస్తున్నాం..."):
                st.session_state["last_result"] = analyze_message(message.strip())
                st.session_state["last_message"] = message.strip()

    if "last_result" in st.session_state and "last_message" in st.session_state:
        st.divider()
        render_result(st.session_state["last_result"], st.session_state["last_message"], language)

    st.divider()
    st.markdown("### What does ScamSathi check?" if language == "en" else "### ScamSathi ఏమి తనిఖీ చేస్తుంది?")
    feature_cols = st.columns(3, gap="medium")
    features = [
        ("🚨", "Indian scam patterns" if language == "en" else "భారతీయ మోసం నమూనాలు", "UPI, KYC, electricity, courier, job and loan warning signs." if language == "en" else "UPI, KYC, విద్యుత్, కొరియర్, ఉద్యోగం మరియు లోన్ హెచ్చరికలు."),
        ("🤖", "ML text classification" if language == "en" else "ML సందేశ వర్గీకరణ", "TF-IDF + Logistic Regression trained on public English SMS data." if language == "en" else "పబ్లిక్ ఇంగ్లీష్ SMS డేటాపై శిక్షణ పొందిన TF-IDF + Logistic Regression."),
        ("📷", "Screenshot OCR" if language == "en" else "స్క్రీన్‌షాట్ OCR", "Extract text locally from message screenshots with Tesseract." if language == "en" else "Tesseract ద్వారా స్క్రీన్‌షాట్ నుండి స్థానికంగా టెక్స్ట్ తీసుకోవడం."),
    ]
    for col, (icon, title, copy) in zip(feature_cols, features):
        with col:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><div class="feature-title">{html.escape(title)}</div><div class="feature-copy">{html.escape(copy)}</div></div>', unsafe_allow_html=True)
else:
    st.markdown("<div class='hero'><div class='hero-kicker'>About the project</div><div class='hero-title'>Scam awareness, made easier.</div><p class='hero-subtitle'>ScamSathi combines transparent scam-pattern checks with a machine-learning SMS classifier and local screenshot text extraction.</p></div>", unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### Current features")
            for point in ["Hybrid rule-based + ML text analysis", "Indian-specific patterns: UPI, KYC, electricity, courier, job, loan and digital-arrest threats", "English and Telugu explanation interface", "Optional screenshot OCR using local Tesseract", "URL pattern checks without live reputation claims"]:
                st.markdown(f"- {point}")
    with right:
        with st.container(border=True):
            st.markdown("### Known limitations")
            for point in ["The initial ML dataset is general English SMS spam, not an India-specific fraud dataset", "OCR requires Tesseract to be installed separately on Windows", "URLs are not checked against a live threat-intelligence service", "No connection to SMS, WhatsApp, UPI or bank accounts", "A low score does not prove a message is safe"]:
                st.markdown(f"- {point}")
    st.info("This is a prototype for awareness and education. Verify financial or account requests through official channels.")
