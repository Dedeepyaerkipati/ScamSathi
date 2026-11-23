"""Static English/Telugu UI translations for ScamSathi explanations.

The translations are intentionally local and do not send user messages to a
translation service. Unknown future labels fall back to the English text.
"""

LABELS = {
    "Request for sensitive information": "సున్నితమైన సమాచారం అడగడం",
    "Bank or KYC impersonation pattern": "బ్యాంక్ లేదా KYC పేరుతో మోసం చేసే ప్రయత్నం",
    "UPI collect-request or QR-code pattern": "UPI కలెక్ట్ రిక్వెస్ట్ లేదా QR కోడ్ మోసం",
    "Remote-access or screen-sharing risk": "రిమోట్ యాక్సెస్ లేదా స్క్రీన్ షేరింగ్ ప్రమాదం",
    "Courier or parcel-fee pattern": "కొరియర్ లేదా పార్సెల్ ఫీజు మోసం",
    "Urgent electricity-disconnection threat": "విద్యుత్ కనెక్షన్ కట్ చేస్తామని అత్యవసర బెదిరింపు",
    "Electricity-disconnection claim": "విద్యుత్ కనెక్షన్ నిలిపివేస్తామని చెప్పడం",
    "Electricity bill payment pressure": "విద్యుత్ బిల్లు వెంటనే చెల్లించమని ఒత్తిడి",
    "Job or task scam with upfront payment": "ఉద్యోగం పేరుతో ముందుగా డబ్బు అడగడం",
    "Loan advance-fee pattern": "లోన్ పేరుతో ముందస్తు ఫీజు అడగడం",
    "Law-enforcement impersonation or digital-arrest threat": "పోలీసులు లేదా డిజిటల్ అరెస్ట్ పేరుతో బెదిరింపు",
    "Urgency or threat": "అత్యవసరంగా స్పందించమని ఒత్తిడి",
    "Prize or reward bait": "బహుమతి లేదా రివార్డ్ ఆశ చూపించడం",
    "Payment-related instruction": "డబ్బు చెల్లించమని సూచించడం",
    "Potentially deceptive link pattern": "అనుమానాస్పద లింక్ నమూనా",
}

EXPLANATIONS = {
    "Request for sensitive information": "ఈ సందేశం OTP, UPI PIN, పాస్‌వర్డ్ లేదా కార్డు వివరాలు ఇవ్వమని అడుగుతున్నట్లు ఉంది. ఈ వివరాలను ఎవరికీ చెప్పవద్దు.",
    "Bank or KYC impersonation pattern": "బ్యాంక్ లేదా KYC వివరాలతో పాటు ఖాతా నిలిపివేస్తామని లేదా వివరాలు ధృవీకరించమని ఒత్తిడి చేస్తోంది. అధికారిక బ్యాంక్ యాప్‌లో మాత్రమే తనిఖీ చేయండి.",
    "UPI collect-request or QR-code pattern": "డబ్బు అందుకోవడానికి QR స్కాన్ చేయమని లేదా UPI PIN నమోదు చేయమని చెబుతోంది. UPI PIN చెల్లింపును ఆమోదించడానికి ఉపయోగిస్తారు; డబ్బు స్వీకరించడానికి కాదు.",
    "Remote-access or screen-sharing risk": "బ్యాంకింగ్ లేదా రిఫండ్ సందర్భంలో రిమోట్ యాక్సెస్ యాప్ లేదా స్క్రీన్ షేరింగ్ అడుగుతున్నట్లు ఉంది. ఇది మీ ఖాతా సమాచారాన్ని ప్రమాదంలో పడేయవచ్చు.",
    "Courier or parcel-fee pattern": "పార్సెల్ సమస్య పేరుతో ఫీజు లేదా వెంటనే చెల్లింపు అడుగుతోంది. కొరియర్ అధికారిక యాప్‌లో ట్రాకింగ్ తనిఖీ చేయండి.",
    "Urgent electricity-disconnection threat": "విద్యుత్ కనెక్షన్ కట్ చేస్తామని గడువు పెట్టి భయపెడుతోంది. మీ విద్యుత్ సంస్థ అధికారిక యాప్ లేదా వెబ్‌సైట్‌లో బిల్లు తనిఖీ చేయండి.",
    "Electricity-disconnection claim": "విద్యుత్ కనెక్షన్ నిలిపివేస్తామని చెబుతోంది. సందేశంలోని నంబర్‌కు కాల్ చేయకుండా అధికారిక కస్టమర్ కేర్‌ను సంప్రదించండి.",
    "Electricity bill payment pressure": "పెండింగ్ బిల్లు పేరుతో త్వరగా చెల్లించమని ఒత్తిడి చేస్తోంది. నిజంగా బిల్లు పెండింగ్‌లో ఉందో అధికారిక మార్గంలో తనిఖీ చేయండి.",
    "Job or task scam with upfront payment": "ఉద్యోగం లేదా టాస్క్ ఇవ్వడానికి ముందుగా రిజిస్ట్రేషన్ ఫీజు లేదా డిపాజిట్ అడుగుతోంది. ఉద్యోగం కోసం ముందుగా డబ్బు చెల్లించవద్దు.",
    "Loan advance-fee pattern": "లోన్ విడుదలకు ముందుగా ఫీజు అడుగుతున్నట్లు ఉంది. రుణదాత నిజమైనదో స్వతంత్రంగా తనిఖీ చేయండి.",
    "Law-enforcement impersonation or digital-arrest threat": "పోలీసులు లేదా దర్యాప్తు సంస్థ పేరుతో అరెస్ట్/కేసు బెదిరింపు చేస్తోంది. భయంతో డబ్బు పంపవద్దు.",
    "Urgency or threat": "వెంటనే చర్య తీసుకోకపోతే నష్టం జరుగుతుందని ఒత్తిడి చేస్తోంది. తొందరపడకుండా అధికారిక మార్గంలో నిర్ధారించండి.",
    "Prize or reward bait": "బహుమతి లేదా క్యాష్‌బ్యాక్ ఆశ చూపించి వివరాలు లేదా డబ్బు పొందాలని ప్రయత్నించవచ్చు.",
    "Payment-related instruction": "సందేశం ద్వారా డబ్బు చెల్లించమని అడుగుతోంది. చెల్లించే ముందు గ్రహీత మరియు కారణాన్ని నిర్ధారించండి.",
    "Potentially deceptive link pattern": "లింక్‌లో అనుమానాస్పద నమూనా ఉంది. ఈ యాప్ ప్రత్యక్ష వెబ్‌సైట్ భద్రతను తనిఖీ చేయదు.",
}

CATEGORIES = {
    "Possible remote-access scam": "రిమోట్ యాక్సెస్ మోసం అయ్యే అవకాశం",
    "Possible UPI or QR-code payment scam": "UPI లేదా QR కోడ్ చెల్లింపు మోసం అయ్యే అవకాశం",
    "Possible bank or KYC phishing": "బ్యాంక్ లేదా KYC ఫిషింగ్ అయ్యే అవకాశం",
    "Possible credential or payment scam": "పాస్‌వర్డ్ లేదా చెల్లింపు మోసం అయ్యే అవకాశం",
    "Possible courier or parcel scam": "కొరియర్ లేదా పార్సెల్ మోసం అయ్యే అవకాశం",
    "Possible electricity-bill scam": "విద్యుత్ బిల్లు మోసం అయ్యే అవకాశం",
    "Possible job or task scam": "ఉద్యోగం లేదా టాస్క్ మోసం అయ్యే అవకాశం",
    "Possible loan advance-fee scam": "లోన్ ముందస్తు ఫీజు మోసం అయ్యే అవకాశం",
    "Possible authority impersonation scam": "అధికారుల పేరుతో మోసం అయ్యే అవకాశం",
    "Possible phishing or suspicious-link message": "ఫిషింగ్ లేదా అనుమానాస్పద లింక్ సందేశం అయ్యే అవకాశం",
    "Possible promotional or reward scam": "బహుమతి లేదా రివార్డ్ మోసం అయ్యే అవకాశం",
    "Message needs verification": "ఈ సందేశాన్ని నిర్ధారించాలి",
    "Message contains an unverified link": "ఈ సందేశంలో నిర్ధారించని లింక్ ఉంది",
    "No obvious warning pattern detected": "స్పష్టమైన హెచ్చరిక నమూనా కనిపించలేదు",
    "Potential spam message (ML model prediction)": "ML మోడల్ ప్రకారం స్పామ్ అయ్యే అవకాశం",
}

ADVICE = {
    "Never disclose an OTP, UPI PIN, password, CVV or full card details to a caller or message sender.": "OTP, UPI PIN, పాస్‌వర్డ్, CVV లేదా పూర్తి కార్డు వివరాలను ఎవరికీ చెప్పవద్దు.",
    "Do not use a link in the message. Check account or KYC status inside your bank's official app or by calling the number printed on your card.": "సందేశంలోని లింక్‌ను తెరవవద్దు. బ్యాంక్ అధికారిక యాప్‌లో లేదా కార్డుపై ఉన్న అధికారిక నంబర్ ద్వారా తనిఖీ చేయండి.",
    "Do not approve an unexpected collect request or enter your UPI PIN to receive a refund or payment. Check the request in your UPI app and decline anything you did not initiate.": "మీరు ప్రారంభించని UPI కలెక్ట్ రిక్వెస్ట్‌ను ఆమోదించవద్దు. రిఫండ్ పొందడానికి UPI PIN నమోదు చేయవద్దు.",
    "Do not call a number or pay through details in the message. Check your consumer number and bill in your electricity provider's official app, website or published customer-care channel.": "సందేశంలో ఇచ్చిన నంబర్‌కు కాల్ చేయవద్దు లేదా అక్కడి వివరాల ద్వారా చెల్లించవద్దు. విద్యుత్ సంస్థ అధికారిక యాప్/వెబ్‌సైట్‌లో బిల్లు తనిఖీ చేయండి.",
    "Open your electricity provider's official app or website yourself and check whether a bill is actually outstanding.": "మీ విద్యుత్ సంస్థ అధికారిక యాప్ లేదా వెబ్‌సైట్‌ను మీరే తెరిచి బిల్లు పెండింగ్‌లో ఉందో చూడండి.",
    "Do not install an APK or remote-access app at a stranger's request. End the call and contact the company through its official support channel.": "తెలియని వ్యక్తి చెప్పినందుకు APK లేదా రిమోట్ యాక్సెస్ యాప్ ఇన్‌స్టాల్ చేయవద్దు. అధికారిక సపోర్ట్‌ను సంప్రదించండి.",
    "Check tracking only through the courier's official website or app using a tracking number you already have. Do not pay through an unexpected message link.": "మీ దగ్గర ఉన్న ట్రాకింగ్ నంబర్‌తో కొరియర్ అధికారిక యాప్/వెబ్‌సైట్‌లో మాత్రమే తనిఖీ చేయండి.",
    "Do not pay a joining fee, deposit or task recharge to receive a job. Verify the employer independently and never share banking credentials.": "ఉద్యోగం కోసం జాయినింగ్ ఫీజు, డిపాజిట్ లేదా టాస్క్ రీచార్జ్ చెల్లించవద్దు. సంస్థను స్వతంత్రంగా నిర్ధారించండి.",
    "Do not transfer money or share documents because of a threatening call or message. End contact and verify through official government or police channels.": "బెదిరింపు కాల్ లేదా సందేశం కారణంగా డబ్బు పంపవద్దు, పత్రాలు ఇవ్వవద్దు. అధికారిక ప్రభుత్వ/పోలీస్ మార్గంలో నిర్ధారించండి.",
    "Do not reply, click links or follow payment instructions in this message.": "ఈ సందేశానికి సమాధానం ఇవ్వవద్దు, లింకులు తెరవవద్దు, చెల్లింపు సూచనలు పాటించవద్దు.",
    "Pause and verify the request using the organisation's official app, website or published phone number.": "ఆగి, సంస్థ అధికారిక యాప్, వెబ్‌సైట్ లేదా ప్రచురించిన ఫోన్ నంబర్ ద్వారా నిర్ధారించండి.",
    "Do not transfer money based only on a message or caller's instructions.": "సందేశం లేదా కాలర్ చెప్పినదాని ఆధారంగా మాత్రమే డబ్బు పంపవద్దు.",
    "A link is present, but this prototype has not checked its live reputation. Open it only after verifying the sender and destination.": "లింక్ ఉంది, కానీ దాని ప్రత్యక్ష భద్రతను ఈ ప్రోటోటైప్ తనిఖీ చేయలేదు. పంపిన వ్యక్తి మరియు గమ్యాన్ని నిర్ధారించిన తర్వాత మాత్రమే తెరవండి.",
    "Check the sender using a contact method you already trust.": "మీకు ఇప్పటికే తెలిసిన విశ్వసనీయ మార్గం ద్వారా పంపిన వ్యక్తిని నిర్ధారించండి.",
    "Do not share sensitive information or make payments based only on this message.": "ఈ సందేశం ఆధారంగా మాత్రమే వ్యక్తిగత వివరాలు పంచుకోవద్దు లేదా డబ్బు చెల్లించవద్దు.",
}

RISK = {
    "High risk": "అధిక ప్రమాదం",
    "Needs verification": "నిర్ధారించాలి",
    "No obvious warning detected": "స్పష్టమైన హెచ్చరిక కనిపించలేదు",
}

UI = {
    "en": {
        "title": "Pause. Check. Stay safe.",
        "subtitle": "Paste a suspicious SMS, email or chat message, or upload a screenshot. ScamSathi highlights warning signs and suggests safer next steps.",
        "input": "Message to inspect",
        "scan": "Scan message",
        "upload": "Upload message screenshot",
        "extract": "Extract text from screenshot",
        "use_text": "Use extracted text",
        "results": "Your message analysis",
        "why": "Why did ScamSathi flag this?",
        "advice": "What should you do next?",
        "category": "Suggested category",
        "ml": "Machine-learning assessment",
        "about": "About ScamSathi",
        "language": "Explanation language",
        "english": "English",
        "telugu": "Telugu",
        "privacy": "Your message is analyzed only when you submit it in this app. Avoid submitting personal or account details.",
        "no_ocr": "OCR is not ready. Install the Tesseract OCR application on Windows, then restart this app. See README.md for setup steps.",
        "empty_ocr": "No text was extracted. Try a clearer screenshot or type the message manually.",
    },
    "te": {
        "title": "ఆగండి. తనిఖీ చేయండి. సురక్షితంగా ఉండండి.",
        "subtitle": "అనుమానాస్పద SMS, ఈమెయిల్ లేదా చాట్ సందేశాన్ని పేస్ట్ చేయండి, లేదా స్క్రీన్‌షాట్ అప్‌లోడ్ చేయండి. ScamSathi హెచ్చరికలను చూపించి సురక్షితమైన తదుపరి చర్యలను సూచిస్తుంది.",
        "input": "తనిఖీ చేయాల్సిన సందేశం",
        "scan": "సందేశాన్ని తనిఖీ చేయండి",
        "upload": "సందేశం స్క్రీన్‌షాట్ అప్‌లోడ్ చేయండి",
        "extract": "స్క్రీన్‌షాట్ నుండి టెక్స్ట్ తీసుకోండి",
        "use_text": "తీసుకున్న టెక్స్ట్ ఉపయోగించండి",
        "results": "మీ సందేశ విశ్లేషణ",
        "why": "ScamSathi ఈ హెచ్చరిక ఎందుకు చూపించింది?",
        "advice": "ఇప్పుడు మీరు ఏమి చేయాలి?",
        "category": "సూచించిన వర్గం",
        "ml": "మెషిన్ లెర్నింగ్ విశ్లేషణ",
        "about": "ScamSathi గురించి",
        "language": "వివరణ భాష",
        "english": "ఇంగ్లీష్",
        "telugu": "తెలుగు",
        "privacy": "మీరు ఈ యాప్‌లో సమర్పించినప్పుడు మాత్రమే సందేశం విశ్లేషించబడుతుంది. వ్యక్తిగత లేదా ఖాతా వివరాలను ఇవ్వవద్దు.",
        "no_ocr": "OCR సిద్ధంగా లేదు. Windowsలో Tesseract OCR ఇన్‌స్టాల్ చేసి యాప్‌ను మళ్లీ ప్రారంభించండి. README.md చూడండి.",
        "empty_ocr": "స్క్రీన్‌షాట్ నుండి టెక్స్ట్ తీసుకోలేకపోయాం. స్పష్టమైన చిత్రం ఉపయోగించండి లేదా సందేశాన్ని టైప్ చేయండి.",
    },
}


def localized_indicator(item: dict, language: str) -> dict:
    if language != "te":
        return item
    label = item.get("label", "")
    return {
        **item,
        "label_display": LABELS.get(label, label),
        "explanation_display": EXPLANATIONS.get(label, item.get("explanation", "")),
    }


def localized_category(category: str, language: str) -> str:
    return CATEGORIES.get(category, category) if language == "te" else category


def localized_risk(risk: str, language: str) -> str:
    return RISK.get(risk, risk) if language == "te" else risk


def localized_advice(advice: str, language: str) -> str:
    return ADVICE.get(advice, advice) if language == "te" else advice


def ui(language: str) -> dict:
    return UI.get(language, UI["en"])
