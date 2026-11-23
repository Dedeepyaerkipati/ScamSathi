# ScamSathi — Complete Prototype v1.0

ScamSathi is an educational digital-safety prototype. It combines transparent rule-based checks for common Indian scam patterns with a TF-IDF + Logistic Regression SMS spam classifier. It also provides a Telugu/English explanation interface and optional local screenshot OCR.

## Features included

- Hybrid analysis: Indian-focused rules + trained ML model when available.
- Warning patterns: OTP/credential requests, bank/KYC impersonation, UPI collect/QR refund tricks, remote-access requests, courier fees, electricity disconnection threats, job/task fees, loan advance fees, digital-arrest threats, urgency/reward bait, and suspicious URL patterns.
- Explainable indicators with recommended safety actions.
- English and Telugu explanations (static local translations; no translation API).
- Screenshot upload and OCR using local Tesseract (optional external executable installation).
- Training script for the public UCI SMS Spam Collection.
- Unit tests for scam and non-scam examples.

## 1. Requirements

- Windows 10/11
- Python 3.10–3.13 (Python 3.13 is suitable with current package versions)
- Internet connection for the first dataset download, unless you already have `data/SMSSpamCollection` or your trained model file.
- Tesseract OCR is optional and only needed for screenshot scanning.

## 2. Setup on Windows / VS Code

Open this extracted `ScamSathi_Complete` folder in VS Code. In the PowerShell terminal:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Add or train the model

**Important:** The trained `spam_classifier.joblib` file is created on your own computer and is not embedded in this source ZIP.

You already trained the model in your earlier ScamSathi folder. To keep using that exact trained model, copy this file from your old project:

`old ScamSathi\models\spam_classifier.joblib`

to:

`ScamSathi_Complete\models\spam_classifier.joblib`

You may also copy `training_metrics.json` into the new `models` folder.

If you do not have the model file, train again (requires internet to download the UCI dataset):

```powershell
python train_model.py
```

The script creates `models/spam_classifier.joblib` and `models/training_metrics.json`.

## 4. Run the application

```powershell
python -m streamlit run app.py
```

## 5. Run tests

```powershell
python -m unittest discover -s tests -v
```

The detector tests run without the trained model. With no model artifact, the app falls back to rule-based analysis and shows that the ML model is unavailable.

## 6. Optional screenshot OCR setup (Windows)

The screenshot feature uses Tesseract locally. The Python package `pytesseract` is installed by `requirements.txt`, but the Tesseract OCR program itself must be installed separately.

1. Install the Tesseract OCR Windows application using a trusted distribution.
2. During installation, include English language data.
3. Add the Tesseract installation folder to Windows PATH (commonly `C:\Program Files\Tesseract-OCR`).
4. Close and reopen VS Code so the updated PATH is loaded.
5. Run the app and upload a PNG/JPG screenshot, then choose **Extract text from screenshot**.

If Tesseract is not detected, the main message scanner still works. You can paste the message manually.

## 7. Example messages for testing

**UPI QR refund scam example**

`Your refund is ready. Scan this QR to receive money and enter UPI PIN to receive the amount.`

**Electricity disconnection threat example**

`Your electricity connection will be disconnected tonight due to pending bill. Pay immediately.`

**Normal message**

`Hi! Our project meeting is tomorrow at 10 AM. Please bring your laptop.`

**Normal UPI mention**

`I paid the shop 500 rupees through UPI. Thank you.`

## 8. Important limitations and honest claims

- The ML model is trained on the English UCI SMS Spam Collection. It is not an India-specific banking, UPI, Telugu or electricity-fraud model.
- Indian-specific detections currently come from transparent phrase/pattern rules, not from the UCI model learning these categories.
- The displayed combined score is a heuristic indicator, not a calibrated probability.
- A low score does not prove a message is genuine.
- URL checks identify a few suspicious URL patterns; they do not query live domain reputation, DNS, or threat-intelligence services.
- OCR can make mistakes. Review extracted text before scanning.
- The app does not connect to WhatsApp, SMS inboxes, UPI apps or bank accounts. It only analyzes content that the user submits.

## Dataset reference

Almeida, T. A., & Hidalgo, J. M. G. (2011). SMS Spam Collection. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/228/sms

## Project structure

```text
ScamSathi_Complete/
├── app.py
├── train_model.py
├── requirements.txt
├── detection/
│   ├── __init__.py
│   ├── message_detector.py
│   ├── translations.py
│   └── ocr.py
├── tests/
│   └── test_detector.py
├── data/
├── models/
└── README.md
```
