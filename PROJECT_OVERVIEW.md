# Hackathon Project Overview

**Problem:** People receive suspicious SMS/chat messages that use urgency, reward bait, account threats, QR/UPI instructions and fake fees. They may not know which signals to check.

**Solution:** ScamSathi lets a user paste a message or extract text from a screenshot, then displays a risk indicator, ML spam estimate when available, matched rule explanations and safer next steps.

**Technical design:** Streamlit UI; TF-IDF + Logistic Regression text classifier trained on UCI SMS Spam Collection; transparent Python rules for India-focused patterns; local Tesseract OCR; local static English/Telugu explanation strings.

**User flow:** Paste/upload → optional OCR → analyze → view ML and rule outputs separately → understand warning signs → verify through official channels.

**Honest limitation:** ML scores are not proof and the UCI model is general English SMS spam data, not a dedicated Indian fraud dataset. Rules cover Indian examples but require broad test/evaluation data. URL checks are heuristic only.
