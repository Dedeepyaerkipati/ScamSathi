"""Train ScamSathi's SMS spam classifier using the public UCI SMS Spam Collection.

Dataset source: Almeida & Hidalgo (2011), UCI Machine Learning Repository,
https://archive.ics.uci.edu/dataset/228/sms
License listed by UCI: CC BY 4.0.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
DATA_FILE = DATA_DIR / "SMSSpamCollection"
MODEL_FILE = MODEL_DIR / "spam_classifier.joblib"
METRICS_FILE = MODEL_DIR / "training_metrics.json"
DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"


def download_dataset() -> Path:
    """Download and extract the UCI dataset if it is not already present."""
    if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
        print(f"Using existing dataset: {DATA_FILE}")
        return DATA_FILE

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading the UCI SMS Spam Collection dataset...")
    request = urllib.request.Request(
        DATA_URL,
        headers={"User-Agent": "ScamSathi-educational-project/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            archive_bytes = response.read()
    except Exception as exc:
        raise RuntimeError(
            "Could not download the dataset. Check your internet connection and try again."
        ) from exc

    try:
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            member = next(
                (name for name in archive.namelist() if name.endswith("SMSSpamCollection")),
                None,
            )
            if member is None:
                raise RuntimeError("The downloaded ZIP did not contain SMSSpamCollection.")
            DATA_FILE.write_bytes(archive.read(member))
    except zipfile.BadZipFile as exc:
        raise RuntimeError("The downloaded dataset file was not a valid ZIP archive.") from exc

    print(f"Dataset saved to: {DATA_FILE}")
    return DATA_FILE


def load_dataset(path: Path) -> tuple[list[str], list[str]]:
    texts: list[str] = []
    labels: list[str] = []
    with path.open("r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            row = line.rstrip("\r\n").split("\t", 1)
            if len(row) != 2:
                continue
            label, message = row
            label = label.strip().lower()
            message = message.strip()
            if label in {"ham", "spam"} and message:
                labels.append(label)
                texts.append(message)

    if len(texts) < 100:
        raise RuntimeError(
            f"Only {len(texts)} usable messages were loaded. The dataset may be incomplete."
        )
    if len(set(labels)) != 2:
        raise RuntimeError("The dataset must contain both ham and spam labels.")
    return texts, labels


def main() -> int:
    try:
        data_path = download_dataset()
        texts, labels = load_dataset(data_path)

        X_train, X_test, y_train, y_test = train_test_split(
            texts,
            labels,
            test_size=0.20,
            random_state=42,
            stratify=labels,
        )

        # TF-IDF turns words and two-word phrases into numeric features.
        # Logistic Regression learns which patterns are associated with spam.
        model = Pipeline(
            steps=[
                (
                    "tfidf",
                    TfidfVectorizer(
                        lowercase=True,
                        strip_accents="unicode",
                        ngram_range=(1, 2),
                        min_df=2,
                        sublinear_tf=True,
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=1200,
                        class_weight="balanced",
                        random_state=42,
                    ),
                ),
            ]
        )

        print(f"Training on {len(X_train):,} messages; testing on {len(X_test):,} messages...")
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, pos_label="spam", zero_division=0)
        recall = recall_score(y_test, predictions, pos_label="spam", zero_division=0)
        f1 = f1_score(y_test, predictions, pos_label="spam", zero_division=0)
        matrix = confusion_matrix(y_test, predictions, labels=["ham", "spam"]).tolist()

        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, MODEL_FILE)
        metrics = {
            "dataset": "UCI SMS Spam Collection (2011)",
            "dataset_url": "https://archive.ics.uci.edu/dataset/228/sms",
            "total_messages": len(texts),
            "training_messages": len(X_train),
            "test_messages": len(X_test),
            "random_state": 42,
            "test_size": 0.20,
            "accuracy": round(float(accuracy), 4),
            "spam_precision": round(float(precision), 4),
            "spam_recall": round(float(recall), 4),
            "spam_f1": round(float(f1), 4),
            "confusion_matrix_labels": ["ham", "spam"],
            "confusion_matrix": matrix,
        }
        METRICS_FILE.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        print("\nMODEL EVALUATION (held-out test set)")
        print(f"Accuracy:        {accuracy:.3f}")
        print(f"Spam precision:  {precision:.3f}")
        print(f"Spam recall:     {recall:.3f}")
        print(f"Spam F1-score:   {f1:.3f}")
        print("\nConfusion matrix (rows=true, columns=predicted; order: ham, spam):")
        print(matrix)
        print("\nClassification report:")
        print(classification_report(y_test, predictions, labels=["ham", "spam"], zero_division=0))
        print(f"Saved trained model: {MODEL_FILE}")
        print(f"Saved evaluation metrics: {METRICS_FILE}")
        print("\nTraining completed successfully.")
        return 0

    except Exception as exc:
        print(f"\nTRAINING FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
