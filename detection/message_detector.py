"""Hybrid rule-based and machine-learning message analysis for ScamSathi.

The rule layer highlights common social-engineering patterns seen in Indian
consumer messages. It is advisory: it does not verify senders, domains, or
transactions, and it is not a substitute for a bank or law-enforcement check.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

import joblib

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "spam_classifier.joblib"
_URL_PATTERN = re.compile(r"(?:https?://|www\.)[^\s<>()\[\]{}\"']+", re.IGNORECASE)
_MODEL = None
_MODEL_LOAD_ATTEMPTED = False


def _load_model():
    """Load the trained classifier once; return None if it is unavailable."""
    global _MODEL, _MODEL_LOAD_ATTEMPTED
    if _MODEL_LOAD_ATTEMPTED:
        return _MODEL
    _MODEL_LOAD_ATTEMPTED = True
    if MODEL_PATH.exists():
        try:
            _MODEL = joblib.load(MODEL_PATH)
        except Exception:
            _MODEL = None
    return _MODEL


def is_model_available() -> bool:
    """Return True when a trained classifier artifact is available and loadable."""
    return _load_model() is not None


def _extract_urls(message: str) -> list[str]:
    urls: list[str] = []
    for match in _URL_PATTERN.findall(message):
        url = match.rstrip(".,!?;:")
        if url and url not in urls:
            urls.append(url)
    return urls


def _has(text: str, phrases: tuple[str, ...] | list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def _has_request_for_sensitive_data(text: str) -> bool:
    """Detect a request for credentials, while avoiding common safety warnings."""
    sensitive = r"(?:otp|one[- ]time password|upi\s*pin|pin|password|cvv|card number|bank details)"
    action = r"(?:share|send|provide|enter|type|submit|confirm|verify|forward|give|reply with|tell me)"
    patterns = (
        re.compile(rf"\b{action}\b\s+(?:your\s+|the\s+)?{sensitive}\b"),
        re.compile(rf"\b{sensitive}\b\s+(?:immediately|right now|now|to verify|to unblock|for kyc)\b"),
    )
    for pattern in patterns:
        for match in pattern.finditer(text):
            prefix = text[max(0, match.start() - 24):match.start()]
            if re.search(r"\b(?:never|don't|dont|do not|avoid|should not|shouldn't)\s*$", prefix):
                continue
            return True
    return False


def _rule_analysis(message: str) -> tuple[int, list[dict], list[dict], str, list[str]]:
    text = re.sub(r"\s+", " ", message.lower()).strip()
    indicators: list[dict] = []
    urls = _extract_urls(message)
    advice: list[str] = []
    score = 0

    def add_indicator(label: str, explanation: str, points: int, next_step: str | None = None) -> None:
        nonlocal score
        # Prevent duplicate indicators when several related phrases match.
        if any(item["label"] == label for item in indicators):
            return
        indicators.append({"label": label, "explanation": explanation})
        score += points
        if next_step:
            advice.append(next_step)

    # 1. Credentials, OTPs and financial security information.
    if _has_request_for_sensitive_data(text):
        add_indicator(
            "Request for sensitive information",
            "The message appears to ask you to share or enter an OTP, UPI PIN, password, CVV or other financial details. A genuine bank or payment provider should not ask you to disclose your UPI PIN or OTP to a person.",
            38,
            "Never disclose an OTP, UPI PIN, password, CVV or full card details to a caller or message sender.",
        )

    # 2. Bank impersonation and KYC/account-blocking pressure.
    bank_terms = ("bank", "bank account", "debit card", "credit card", "account")
    kyc_terms = ("kyc", "re-kyc", "re kyc", "verify your account", "update your account", "account verification", "reactivate")
    account_threats = (
        "will be blocked", "will get blocked", "account blocked", "account suspended",
        "account will be suspended", "account deactivated", "services will stop",
        "card will be blocked", "kyc expired", "kyc will expire",
    )
    has_bank_context = _has(text, bank_terms)
    has_kyc_context = _has(text, kyc_terms)
    has_account_threat = _has(text, account_threats)
    if (has_bank_context and has_account_threat) or (
        has_kyc_context and (has_account_threat or _has_request_for_sensitive_data(text) or bool(urls))
    ):
        add_indicator(
            "Bank or KYC impersonation pattern",
            "The message combines account/KYC language with a threat, verification request or link. Scammers commonly imitate banks to make people act before checking the request.",
            25,
            "Do not use a link in the message. Check account or KYC status inside your bank's official app or by calling the number printed on your card.",
        )

    # 3. UPI collect requests, QR-code tricks and fake refund instructions.
    upi_brands = ("upi", "gpay", "google pay", "phonepe", "paytm", "bhim")
    upi_action_phrases = (
        "collect request", "payment request", "approve the request", "approve request",
        "accept the request", "accept payment", "scan qr to receive", "scan this qr to receive",
        "scan qr and enter", "enter upi pin to receive", "upi pin to receive",
        "enter your pin to receive", "receive money by scanning", "refund will be credited",
    )
    qr_receive = _has(text, ("scan qr to receive", "scan this qr to receive", "enter upi pin to receive", "upi pin to receive", "receive money by scanning"))
    # Do not flag educational or protective wording that warns users NOT to do this.
    qr_instruction_negated = bool(
        re.search(r"\b(?:never|don't|dont|do not|avoid|should not|shouldn't)\b.{0,45}\b(?:scan|enter|upi\s*pin)\b", text)
    )
    if qr_instruction_negated:
        qr_receive = False
    upi_brand_and_action = _has(text, upi_brands) and _has(text, upi_action_phrases) and not qr_instruction_negated
    if qr_receive or upi_brand_and_action:
        add_indicator(
            "UPI collect-request or QR-code pattern",
            "The message appears to tell you to approve a collect/payment request or scan a QR code to receive money. A UPI PIN is used to authorise a payment, not to receive money.",
            32,
            "Do not approve an unexpected collect request or enter your UPI PIN to receive a refund or payment. Check the request in your UPI app and decline anything you did not initiate.",
        )

    # 4. Remote-access apps, APK installs and screen-sharing requests.
    remote_tools = ("anydesk", "teamviewer", "quick support", "quicksupport", "rustdesk", "remote access", "screen sharing", "screen share")
    install_terms = ("install this app", "download this app", "install apk", "download apk", "install an apk", "share your screen", "give screen access", "allow remote")
    remote_context = _has(text, remote_tools) or _has(text, install_terms)
    financial_context = _has(text, ("bank", "upi", "payment", "refund", "kyc", "account", "card", "wallet"))
    if remote_context and (financial_context or _has_request_for_sensitive_data(text) or _has(text, ("customer care", "support agent", "refund team"))):
        add_indicator(
            "Remote-access or screen-sharing risk",
            "The message appears to involve remote-control software, an APK or screen sharing in a financial/customer-support context. This can expose messages, banking screens and payment activity to another person.",
            32,
            "Do not install an APK or remote-access app at a stranger's request. End the call and contact the company through its official support channel.",
        )

    # 5. Courier, parcel and customs-fee scams.
    courier_context = _has(text, ("parcel", "courier", "shipment", "package", "delivery"))
    courier_pressure = _has(text, ("held", "on hold", "delivery failed", "address issue", "customs fee", "customs charge", "pay delivery fee", "release your parcel", "clearance fee", "redelivery fee"))
    if courier_context and courier_pressure:
        add_indicator(
            "Courier or parcel-fee pattern",
            "The message combines a parcel/delivery issue with a fee, customs charge or urgent action. Unexpected small-fee messages can be used to collect card details or direct people to phishing pages.",
            24,
            "Check tracking only through the courier's official website or app using a tracking number you already have. Do not pay through an unexpected message link.",
        )

    # 6. Electricity disconnection and utility-bill threats.
    # Require a utility context plus a concrete disconnection claim. A routine
    # reminder that an electricity bill is due should not trigger this rule.
    utility_context = _has(
        text,
        ("electricity", "power supply", "electric bill", "electricity bill", "meter connection", "electricity connection"),
    )
    utility_disconnection = _has(
        text,
        (
            "will be disconnected", "will get disconnected", "connection will be cut",
            "power will be cut", "power supply will be cut", "disconnect tonight",
            "disconnect today", "electricity supply will be disconnected",
            "electricity connection will be disconnected", "meter will be disconnected",
        ),
    )
    utility_payment_pressure = _has(
        text,
        ("pay immediately", "pay now", "within 24 hours", "tonight", "today", "last warning", "final notice"),
    )
    utility_overdue_terms = _has(text, ("pending bill", "overdue bill", "unpaid bill", "bill payment pending"))

    if utility_context and utility_disconnection:
        # A disconnection threat combined with a deadline/payment demand is a
        # stronger signal than a generic bill reminder.
        points = 36 if utility_payment_pressure else 26
        add_indicator(
            "Urgent electricity-disconnection threat" if utility_payment_pressure else "Electricity-disconnection claim",
            "The message claims your electricity connection will be cut. A deadline or immediate-payment demand increases the pressure tactic. Verify the bill and notice directly with your actual electricity provider.",
            points,
            "Do not call a number or pay through details in the message. Check your consumer number and bill in your electricity provider's official app, website or published customer-care channel.",
        )
    elif utility_context and utility_overdue_terms and utility_payment_pressure:
        add_indicator(
            "Electricity bill payment pressure",
            "The message combines an overdue-bill claim with a demand to pay quickly. This may be a genuine reminder or an impersonation attempt, so verify it independently before paying.",
            20,
            "Open your electricity provider's official app or website yourself and check whether a bill is actually outstanding.",
        )

    # 7. Job/task scams asking for money upfront.
    # Include common wording variants such as "working from home" and
    # "earn 5,000 rupees daily". The fee must still appear with job context,
    # so an ordinary payment message is not flagged by this rule alone.
    job_context = _has(
        text,
        (
            "work from home", "working from home", "work-from-home",
            "part time job", "part-time job", "part time", "part-time",
            "online job", "remote job", "job offer", "daily earnings",
            "earn daily", "earn money", "earn rupees", "data entry job",
            "typing job", "task job", "telegram task", "whatsapp task",
        ),
    )
    upfront_fee = _has(
        text,
        (
            "registration fee", "registration fees", "joining fee", "joining fees",
            "security deposit", "pay to register", "pay registration",
            "pay a registration", "pay first", "recharge your wallet",
            "deposit money", "task recharge", "training fee", "activation fee",
            "account activation fee", "pay to activate", "pay a fee to activate",
            "fee to activate", "activate your account", "onboarding fee",
            "verification fee", "refundable deposit", "initial deposit",
        ),
    )
    if job_context and upfront_fee:
        add_indicator(
            "Job or task scam with upfront payment",
            "The message advertises a job, work-from-home role or task and asks for a registration fee, deposit, activation payment or wallet recharge. Paying money to unlock a job or task is a major warning sign.",
            32,
            "Do not pay a joining fee, deposit or task recharge to receive a job. Verify the employer independently and never share banking credentials.",
        )

    # 8. Loan scams that demand an advance payment.
    loan_context = _has(text, ("loan approved", "instant loan", "personal loan", "loan offer", "loan disbursal"))
    loan_fee = _has(text, ("processing fee", "advance fee", "pay fee first", "insurance fee", "release fee", "transfer fee"))
    if loan_context and loan_fee:
        add_indicator(
            "Loan advance-fee pattern",
            "The message offers or promises a loan but asks for an upfront fee before the money is released. Verify the lender and all charges independently before paying.",
            23,
            "Do not pay an unexpected advance fee to release a loan. Check that the lender is authorised and use its official contact details.",
        )

    # 9. Digital-arrest, law-enforcement and legal-threat impersonation.
    authority_context = _has(text, ("police", "cbi", "cyber crime", "customs officer", "court", "investigation agency"))
    authority_threat = _has(text, ("digital arrest", "you will be arrested", "arrest warrant", "legal case", "money laundering case", "settle this case", "pay to avoid arrest", "keep this call confidential"))
    if _has(text, ("digital arrest", "pay to avoid arrest", "keep this call confidential")) or (authority_context and authority_threat):
        add_indicator(
            "Law-enforcement impersonation or digital-arrest threat",
            "The message uses an arrest, investigation or legal threat to pressure you. Treat requests for money, secrecy or remote access from someone claiming to be an authority as highly suspicious.",
            32,
            "Do not transfer money or share documents because of a threatening call or message. End contact and verify through official government or police channels.",
        )

    # 10. Generic urgency, reward bait and payment pressure.
    urgency_terms = (
        "urgent", "immediately", "right now", "within 24 hours", "last warning",
        "act now", "final notice", "will be blocked", "account suspended",
    )
    if _has(text, urgency_terms):
        add_indicator(
            "Urgency or threat",
            "The message pressures you to act quickly or threatens a negative consequence. Scammers use urgency to discourage careful verification.",
            15,
            "Pause and verify the request using the organisation's official app, website or published phone number.",
        )

    reward_terms = ("congratulations", "you won", "winner", "claim your prize", "cashback", "reward", "lottery", "free gift", "prize")
    if _has(text, reward_terms):
        add_indicator(
            "Prize or reward bait",
            "The message uses a prize, cashback or reward to encourage a quick response. Unexpected rewards can be used to collect fees or personal information.",
            16,
            "Do not pay a fee or provide personal details to claim an unexpected prize or reward.",
        )

    payment_request_terms = (
        "transfer money", "send money", "pay now", "pay immediately", "processing fee",
        "refund fee", "send payment", "make a payment", "deposit money",
    )
    if _has(text, payment_request_terms):
        add_indicator(
            "Payment-related instruction",
            "The message asks for or directs a payment. Confirm the recipient and purpose through a trusted channel before transferring money.",
            18,
            "Do not transfer money based only on a message or caller's instructions.",
        )

    # 11. Link pattern checks. These are heuristics, not live reputation checks.
    url_details: list[dict] = []
    suspicious_link_found = False
    if urls:
        for url in urls:
            candidate = url if url.lower().startswith(("http://", "https://")) else "https://" + url
            parsed = urlparse(candidate)
            host = (parsed.hostname or "").lower()
            path_and_query = (parsed.path + "?" + parsed.query).lower()
            notes: list[str] = []
            if any(shortener in host for shortener in ("bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy")):
                notes.append("URL shortener hides the final destination")
            if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
                notes.append("Link uses an IP address instead of a familiar domain")
            if "xn--" in host:
                notes.append("Domain contains punycode, which can be used for look-alike names")
            if any(word in path_and_query for word in ("login", "verify", "kyc", "update", "claim", "password", "otp", "payment")):
                notes.append("URL path contains a sensitive-action term")
            if not notes:
                notes.append("Link found; its destination and reputation have not been verified")
            url_details.append({"url": url, "note": "; ".join(notes)})
            if any(term in note for note in notes for term in ("hides the final", "IP address", "punycode")):
                suspicious_link_found = True

        if suspicious_link_found:
            add_indicator(
                "Potentially deceptive link pattern",
                "At least one link uses a pattern that deserves extra checking. This prototype does not perform live domain-reputation or safety checks.",
                22,
                "Avoid opening unexpected links. If needed, visit the service through its official app or by typing its known website address.",
            )
        elif not any("link" in item["label"].lower() for item in indicators):
            advice.append("A link is present, but this prototype has not checked its live reputation. Open it only after verifying the sender and destination.")

    score = min(score, 100)

    labels = {item["label"] for item in indicators}
    if "Remote-access or screen-sharing risk" in labels:
        category = "Possible remote-access scam"
    elif "UPI collect-request or QR-code pattern" in labels:
        category = "Possible UPI or QR-code payment scam"
    elif "Bank or KYC impersonation pattern" in labels:
        category = "Possible bank or KYC phishing"
    elif "Request for sensitive information" in labels:
        category = "Possible credential or payment scam"
    elif "Courier or parcel-fee pattern" in labels:
        category = "Possible courier or parcel scam"
    elif any("electricity" in label.lower() or "utility-disconnection" in label.lower() for label in labels):
        category = "Possible electricity-bill scam"
    elif "Job or task scam with upfront payment" in labels:
        category = "Possible job or task scam"
    elif "Loan advance-fee pattern" in labels:
        category = "Possible loan advance-fee scam"
    elif "Law-enforcement impersonation or digital-arrest threat" in labels:
        category = "Possible authority impersonation scam"
    elif "Potentially deceptive link pattern" in labels:
        category = "Possible phishing or suspicious-link message"
    elif "Prize or reward bait" in labels:
        category = "Possible promotional or reward scam"
    elif indicators:
        category = "Message needs verification"
    elif urls:
        category = "Message contains an unverified link"
    else:
        category = "No obvious warning pattern detected"

    # Keep the advice list readable if multiple patterns matched.
    advice = list(dict.fromkeys(advice))
    if not advice:
        advice = [
            "Check the sender using a contact method you already trust.",
            "Do not share sensitive information or make payments based only on this message.",
        ]

    return score, indicators, url_details, category, advice


def analyze_message(message: str) -> dict:
    """Analyze a message using transparent rules and, when trained, an ML model."""
    if not isinstance(message, str):
        raise TypeError("message must be a string")

    rule_score, indicators, urls, category, advice = _rule_analysis(message)
    model = _load_model()
    ml_available = model is not None
    ml_label = None
    spam_probability = None

    if ml_available and message.strip():
        try:
            ml_label = str(model.predict([message])[0]).lower()
            probabilities = model.predict_proba([message])[0]
            classes = list(model.named_steps["classifier"].classes_)
            if "spam" not in classes:
                raise ValueError("The trained model does not contain a 'spam' class")
            spam_probability = float(probabilities[classes.index("spam")])
            if ml_label == "spam" and category == "No obvious warning pattern detected":
                if spam_probability < 0.55:
                    category = "Message needs verification (borderline ML signal)"
                else:
                    category = "Potential spam message (ML model prediction)"
        except Exception:
            # Keep the rule-based analysis working even if an artifact is incompatible.
            ml_available = False
            ml_label = None
            spam_probability = None

    if ml_available and spam_probability is not None:
        # This is a combined product score, not a calibrated probability.
        combined_score = round(0.60 * rule_score + 0.40 * (spam_probability * 100))
        if rule_score >= 60 or (spam_probability >= 0.90 and rule_score >= 20):
            risk_level = "High risk"
        elif rule_score >= 20 or spam_probability >= 0.55 or (ml_label == "spam" and spam_probability >= 0.50):
            # A weak spam prediction is not enough for "High risk", but it
            # should not be presented as completely clear either.
            risk_level = "Needs verification"
        else:
            risk_level = "No obvious warning detected"
        if ml_label == "spam" and spam_probability < 0.55 and not indicators:
            summary = (
                "No configured rule-based warning pattern was detected. The ML model gave a "
                f"borderline SPAM prediction ({spam_probability:.1%} estimated spam likelihood). "
                "This is weak evidence, not a confirmed scam. Verify the sender independently."
            )
            advice.insert(0, "The model result is borderline. Verify the sender through an official channel before taking action.")
        else:
            summary = (
                f"The rule checker found {len(indicators)} warning indicator(s). "
                f"The trained SMS model classified this text as {ml_label.upper()} with "
                f"{spam_probability:.0%} estimated spam likelihood. Use both signals as guidance, not proof."
            )
    else:
        combined_score = rule_score
        if rule_score >= 55:
            risk_level = "High risk"
        elif rule_score >= 18 or urls:
            risk_level = "Needs verification"
        else:
            risk_level = "No obvious warning detected"
        summary = (
            f"The rule checker found {len(indicators)} warning indicator(s). "
            "The trained ML model is not available; this result uses rule-based checks only."
        )

    if risk_level == "High risk" and not any("Do not reply" in item for item in advice):
        advice.insert(0, "Do not reply, click links or follow payment instructions in this message.")

    return {
        "risk_level": risk_level,
        "category": category,
        "summary": summary,
        "score": int(max(0, min(100, combined_score))),
        "rule_score": int(rule_score),
        "indicators": indicators,
        "urls": urls,
        "advice": advice,
        "ml_available": ml_available,
        "ml_label": ml_label,
        "ml_spam_probability": spam_probability,
    }
