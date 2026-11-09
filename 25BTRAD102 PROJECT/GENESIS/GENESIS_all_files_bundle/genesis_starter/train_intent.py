
"""Train GENESIS's first intent-classification model."""

import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "genesis_intent_model.joblib"

# Each example maps a phrase to an intended action.
TRAINING_DATA = {
    "system_stats": [
        "show system stats",
        "give me hardware statistics",
        "check my computer performance",
        "show hardware telemetry",
        "how is my system doing",
        "show me my computer stats",
        "check system performance",
        "give me an overview of my hardware",
    ],
    "cpu_usage": [
        "what is my cpu usage",
        "how much processor power am I using",
        "check CPU percentage",
        "show processor utilization",
        "is my CPU overloaded",
        "how busy is my processor",
        "tell me my CPU load",
        "check processor usage",
    ],
    "ram_usage": [
        "how much RAM am I using",
        "show memory usage",
        "check my available RAM",
        "what percentage of memory is occupied",
        "how much computer memory is being used",
        "check RAM consumption",
        "show available memory",
        "tell me my memory utilization",
    ],
    "battery_status": [
        "what is my battery percentage",
        "check battery level",
        "how much battery is left",
        "is my laptop charging",
        "show battery status",
        "tell me my remaining battery",
        "check laptop battery",
        "how much charge do I have",
    ],
    "remember": [
        "remember that I prefer concise answers",
        "save this note for later",
        "remember this information",
        "store this fact in memory",
        "keep this in mind",
        "make a note of this",
        "save something to memory",
        "remember my preference",
    ],
    "show_memory": [
        "show my saved memories",
        "what do you remember",
        "list my memory notes",
        "show stored facts",
        "what have I asked you to remember",
        "display my saved notes",
        "read my memory",
        "show everything I saved",
    ],
    "time": [
        "what time is it",
        "show the current time",
        "tell me today's date and time",
        "what is the local time",
        "display the current date",
        "check the clock",
        "give me the current time",
        "what date is it today",
    ],
    "os_info": [
        "what operating system am I using",
        "show my system information",
        "tell me my Windows version",
        "which operating system is installed",
        "show computer platform details",
        "what kind of computer do I have",
        "check my OS",
        "display operating system information",
    ],
    "general_chat": [
        "explain how neural networks work",
        "help me understand physics",
        "write a Python program",
        "tell me something interesting",
        "help me plan my project",
        "what is machine learning",
        "explain this concept to me",
        "let us discuss artificial intelligence",
    ],
}


def main():
    texts = []
    labels = []

    for intent, examples in TRAINING_DATA.items():
        for example in examples:
            texts.append(example)
            labels.append(intent)

    # TF-IDF converts language into numeric features.
    # Logistic Regression learns to separate intent categories.
    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                strip_accents="unicode",
                ngram_range=(1, 2),
                sublinear_tf=True,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=42,
            ),
        ),
    ])

    pipeline.fit(texts, labels)

    # A rough cross-validation score helps assess the baseline.
    # This is not a substitute for testing on unseen real-world inputs.
    min_examples = min(
        sum(1 for label in labels if label == intent)
        for intent in set(labels)
    )

    folds = min(4, min_examples)
    if folds >= 2:
        scores = cross_val_score(
            pipeline,
            texts,
            labels,
            cv=folds,
            scoring="accuracy",
        )
        print(
            "Cross-validation accuracy: "
            f"{scores.mean():.1%} +/- {scores.std():.1%}"
        )

    artifact = {
        "pipeline": pipeline,
        "intents": sorted(set(labels)),
        "training_examples": len(texts),
        "version": 1,
    }

    joblib.dump(artifact, MODEL_PATH)

    print(f"Training examples: {len(texts)}")
    print(f"Intent classes: {len(set(labels))}")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
