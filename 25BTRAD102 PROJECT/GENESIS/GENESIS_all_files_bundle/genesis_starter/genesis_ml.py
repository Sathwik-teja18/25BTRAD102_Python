
"""
GENESIS ML - Transformer Cortex
Version: 1.0.0

Purpose:
- Classify requests using a locally trained Transformer encoder.
- Distinguish normal conversation from capability development.
- Recognize skill creation, code debugging, and code improvement.
- Provide predictions to cortex.py.

This model classifies intent; Ollama remains responsible for generating
natural-language answers and proposed code.
"""

from __future__ import annotations

import argparse
import random
import re
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
import warnings

warnings.filterwarnings(
    "ignore",
    message="The PyTorch API of nested tensors is in prototype stage.*",
    category=UserWarning,
)


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "genesis_transformer.pt"

SEED = 42
MAX_LENGTH = 40
EMBEDDING_SIZE = 96
ATTENTION_HEADS = 4
TRANSFORMER_LAYERS = 2
FEED_FORWARD_SIZE = 192
DROPOUT = 0.1
BATCH_SIZE = 16
EPOCHS = 60
LEARNING_RATE = 0.001
CONFIDENCE_THRESHOLD = 0.45

PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"

LABELS = [
    "chat",
    "create_skill",
    "debug_code",
    "improve_code",
]

LABEL_TO_ID = {label: i for i, label in enumerate(LABELS)}
ID_TO_LABEL = {i: label for label, i in LABEL_TO_ID.items()}

random.seed(SEED)
torch.manual_seed(SEED)


# ---------------------------------------------------------
# TRAINING EXAMPLES
# Expand this dataset as GENESIS learns new request types.
# ---------------------------------------------------------

TRAINING_DATA = {
    "chat": [
        "hello genesis",
        "good morning",
        "how are you today",
        "explain quantum physics",
        "what is a transformer neural network",
        "tell me about black holes",
        "help me understand calculus",
        "what is the difference between ram and storage",
        "write a short poem about space",
        "summarize the theory of relativity",
        "what can you tell me about machine learning",
        "answer my question about chemistry",
        "explain this concept in simple terms",
        "give me ideas for a science project",
        "what is the weathering process in geology",
        "help me study for an examination",
        "tell me something interesting",
        "explain how computers work",
        "what does this mathematical formula mean",
        "give me a general explanation of neural networks",
        "what is the capital of japan",
        "compare two scientific theories",
        "help me understand this topic",
        "answer normally without changing your code",
        "I have a question about astronomy",
        "explain the difference between a cpu and gpu",
        "what are the applications of artificial intelligence",
        "give me a summary of this subject",
    ],

    "create_skill": [
        "create a new skill for GENESIS",
        "teach GENESIS how to calculate derivatives",
        "add a new capability to the assistant",
        "build a Python skill for file analysis",
        "make GENESIS able to process csv files",
        "develop a new tool for GENESIS",
        "implement a calculator capability",
        "add support for summarizing local documents",
        "create a module that reads spreadsheet files",
        "make the assistant capable of solving equations",
        "generate a new Python module for this task",
        "help GENESIS learn a new function",
        "design a plugin for the assistant",
        "extend the assistant with image processing",
        "add a capability to search through project files",
        "create a reusable automation skill",
        "make a new module that analyzes datasets",
        "build a capability that extracts text from pdf files",
        "add a new feature to the GENESIS project",
        "develop a tool that converts units",
        "create a new Python utility for GENESIS",
        "implement a feature the assistant does not have",
        "teach the assistant a new programming capability",
        "build a module that checks code quality",
    ],

    "debug_code": [
        "debug this Python code",
        "fix this traceback",
        "why is my Python script crashing",
        "find the bug in this function",
        "diagnose this exception",
        "fix the syntax error in my program",
        "help me troubleshoot this runtime error",
        "investigate why this function returns the wrong result",
        "find and fix the problem in this module",
        "my application crashes when I start it",
        "explain and fix this error message",
        "repair the broken code in this file",
        "identify the cause of this stack trace",
        "fix this import error",
        "resolve this Python dependency problem",
        "debug my transformer training loop",
        "find the cause of this failed test",
        "my code produces an unexpected output",
        "help me repair this broken function",
        "troubleshoot the GENESIS startup failure",
        "correct this failing unit test",
        "diagnose the error without deleting existing features",
        "find why the application exits immediately",
        "help me fix a model loading error",
    ],

    "improve_code": [
        "improve the GENESIS source code",
        "refactor this Python module",
        "make this code more efficient",
        "review the assistant architecture",
        "improve the existing implementation",
        "rewrite this function while preserving its behavior",
        "optimize the performance of this script",
        "clean up the code without removing features",
        "improve the error handling in GENESIS",
        "make this module easier to maintain",
        "upgrade this implementation safely",
        "review the project for design problems",
        "improve the structure of the application",
        "reduce repeated code in this project",
        "add tests to protect existing functionality",
        "improve the reliability of this module",
        "suggest a safer implementation",
        "rewrite this class with better organization",
        "preserve existing features while improving the code",
        "make the assistant architecture more modular",
        "improve the transformer classifier",
        "review this code and propose improvements",
        "help me evolve the GENESIS codebase",
        "make the project more robust without overwriting files",
    ],
}


# ---------------------------------------------------------
# TOKENIZER
# A simple word tokenizer; no external model download.
# ---------------------------------------------------------

def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+|[^\w\s]", text.lower())


def build_vocabulary() -> dict[str, int]:
    vocabulary = {
        PAD_TOKEN: 0,
        UNK_TOKEN: 1,
    }

    for examples in TRAINING_DATA.values():
        for sentence in examples:
            for token in tokenize(sentence):
                if token not in vocabulary:
                    vocabulary[token] = len(vocabulary)

    return vocabulary


def encode_text(
    text: str,
    vocabulary: dict[str, int],
    max_length: int = MAX_LENGTH,
) -> list[int]:
    tokens = tokenize(text)
    ids = [vocabulary.get(token, vocabulary[UNK_TOKEN])
           for token in tokens[:max_length]]

    ids += [vocabulary[PAD_TOKEN]] * (max_length - len(ids))
    return ids


# ---------------------------------------------------------
# DATASET
# ---------------------------------------------------------

class IntentDataset(Dataset):
    def __init__(self, vocabulary: dict[str, int]):
        self.samples = []

        for label, sentences in TRAINING_DATA.items():
            label_id = LABEL_TO_ID[label]

            for sentence in sentences:
                encoded = encode_text(sentence, vocabulary)
                self.samples.append((encoded, label_id))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        encoded, label = self.samples[index]
        return (
            torch.tensor(encoded, dtype=torch.long),
            torch.tensor(label, dtype=torch.long),
        )


# ---------------------------------------------------------
# TRANSFORMER ENCODER CLASSIFIER
# ---------------------------------------------------------

class GenesisTransformer(nn.Module):
    def __init__(
        self,
        vocabulary_size: int,
        number_of_labels: int,
        max_length: int = MAX_LENGTH,
    ):
        super().__init__()

        self.token_embedding = nn.Embedding(
            vocabulary_size,
            EMBEDDING_SIZE,
            padding_idx=0,
        )

        self.position_embedding = nn.Embedding(
            max_length,
            EMBEDDING_SIZE,
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=EMBEDDING_SIZE,
            nhead=ATTENTION_HEADS,
            dim_feedforward=FEED_FORWARD_SIZE,
            dropout=DROPOUT,
            batch_first=True,
            activation="gelu",
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=TRANSFORMER_LAYERS,
        )

        self.normalization = nn.LayerNorm(EMBEDDING_SIZE)

        self.classifier = nn.Sequential(
            nn.Linear(EMBEDDING_SIZE, EMBEDDING_SIZE),
            nn.GELU(),
            nn.Dropout(DROPOUT),
            nn.Linear(EMBEDDING_SIZE, number_of_labels),
        )

    def forward(self, input_ids):
        batch_size, sequence_length = input_ids.shape

        positions = torch.arange(
            sequence_length,
            device=input_ids.device,
        ).unsqueeze(0).expand(batch_size, -1)

        padding_mask = input_ids.eq(0)

        embeddings = (
            self.token_embedding(input_ids)
            + self.position_embedding(positions)
        )

        encoded = self.transformer(
            embeddings,
            src_key_padding_mask=padding_mask,
        )

        # Mean-pool only real tokens, ignoring padding.
        valid_tokens = (~padding_mask).unsqueeze(-1).float()
        summed = (encoded * valid_tokens).sum(dim=1)
        counts = valid_tokens.sum(dim=1).clamp(min=1.0)
        pooled = self.normalization(summed / counts)

        return self.classifier(pooled)


# ---------------------------------------------------------
# TRAINING
# ---------------------------------------------------------

def train_model() -> None:
    vocabulary = build_vocabulary()
    dataset = IntentDataset(vocabulary)

    generator = torch.Generator().manual_seed(SEED)

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        generator=generator,
    )

    model = GenesisTransformer(
        vocabulary_size=len(vocabulary),
        number_of_labels=len(LABELS),
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=0.01,
    )

    loss_function = nn.CrossEntropyLoss()

    print(f"Training GENESIS Transformer on {len(dataset)} examples.")
    print(f"Vocabulary size: {len(vocabulary)}")
    print(f"Intent classes: {', '.join(LABELS)}")

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for inputs, targets in loader:
            optimizer.zero_grad()

            logits = model(inputs)
            loss = loss_function(logits, targets)

            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=1.0,
            )
            optimizer.step()

            total_loss += loss.item()
            predictions = logits.argmax(dim=1)
            correct += (predictions == targets).sum().item()
            total += targets.size(0)

        if (epoch + 1) % 10 == 0 or epoch == 0:
            average_loss = total_loss / max(len(loader), 1)
            accuracy = correct / max(total, 1)

            print(
                f"Epoch {epoch + 1:02d}/{EPOCHS} | "
                f"Loss: {average_loss:.4f} | "
                f"Training accuracy: {accuracy:.1%}"
            )

    checkpoint = {
        "state_dict": model.state_dict(),
        "vocabulary": vocabulary,
        "labels": LABELS,
        "max_length": MAX_LENGTH,
        "embedding_size": EMBEDDING_SIZE,
        "attention_heads": ATTENTION_HEADS,
        "transformer_layers": TRANSFORMER_LAYERS,
        "feed_forward_size": FEED_FORWARD_SIZE,
        "dropout": DROPOUT,
    }

    torch.save(checkpoint, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")
    print("Training complete. Run the prediction tests next.")
    print(
        "Note: training accuracy is measured on the training examples, "
        "not on unseen requests."
    )


# ---------------------------------------------------------
# MODEL LOADING AND PREDICTION
# ---------------------------------------------------------

_loaded_model = None
_loaded_vocabulary = None


def load_model():
    global _loaded_model, _loaded_vocabulary

    if _loaded_model is not None:
        return _loaded_model, _loaded_vocabulary

    if not MODEL_PATH.exists():
        return None, None

    try:
        checkpoint = torch.load(
            MODEL_PATH,
            map_location="cpu",
            weights_only=True,
        )
    except TypeError:
        # Compatibility with older PyTorch versions.
        checkpoint = torch.load(
            MODEL_PATH,
            map_location="cpu",
        )

    vocabulary = checkpoint["vocabulary"]
    labels = checkpoint["labels"]

    if labels != LABELS:
        raise ValueError(
            "Saved model labels do not match this source file. "
            "Retrain with: python genesis_ml.py train"
        )

    model = GenesisTransformer(
        vocabulary_size=len(vocabulary),
        number_of_labels=len(labels),
        max_length=checkpoint["max_length"],
    )

    model.load_state_dict(checkpoint["state_dict"])
    model.eval()

    _loaded_model = model
    _loaded_vocabulary = vocabulary

    return model, vocabulary


def keyword_fallback(text: str) -> str:
    """
    Conservative fallback for when no trained model is available.
    Ambiguous requests default to normal conversation.
    """
    lowered = text.lower()

    debug_terms = (
        "traceback", "stack trace", "syntax error", "crash",
        "debug", "debugging", "exception", "failing test",
        "import error", "runtime error",
    )

    skill_terms = (
        "create a skill", "new skill", "new capability",
        "add a capability", "new feature", "build a module",
        "teach genesis", "teach the assistant", "new tool",
    )

    improve_terms = (
        "refactor", "improve the code", "optimize the code",
        "rewrite this function", "evolve the code",
        "preserve existing features", "improve the architecture",
    )

    if any(term in lowered for term in debug_terms):
        return "debug_code"

    if any(term in lowered for term in skill_terms):
        return "create_skill"

    if any(term in lowered for term in improve_terms):
        return "improve_code"

    return "chat"


def classify_request(text: str) -> dict:
    """
    Returns:
        {
            "intent": "chat" | "create_skill" |
                      "debug_code" | "improve_code",
            "confidence": float,
            "source": "transformer" | "fallback"
        }
    """
    model, vocabulary = load_model()

    if model is None:
        return {
            "intent": keyword_fallback(text),
            "confidence": 0.0,
            "source": "fallback",
        }

    encoded = encode_text(text, vocabulary)

    input_ids = torch.tensor([encoded], dtype=torch.long)

    with torch.no_grad():
        logits = model(input_ids)
        probabilities = torch.softmax(logits, dim=1)[0]

    predicted_id = int(probabilities.argmax().item())
    confidence = float(probabilities[predicted_id].item())
    predicted_label = ID_TO_LABEL[predicted_id]

    # Avoid trusting low-confidence predictions.
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "intent": keyword_fallback(text),
            "confidence": confidence,
            "source": "fallback",
        }

    return {
        "intent": predicted_label,
        "confidence": confidence,
        "source": "transformer",
    }


# ---------------------------------------------------------
# COMMAND-LINE INTERFACE
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="GENESIS Transformer intent classifier"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "train",
        help="Train and save the Transformer classifier",
    )

    predict_parser = subparsers.add_parser(
        "predict",
        help="Classify a request",
    )

    predict_parser.add_argument(
        "text",
        nargs="+",
        help="Request text to classify",
    )

    test_parser = subparsers.add_parser(
        "test",
        help="Run basic routing checks",
    )

    args = parser.parse_args()

    if args.command == "train":
        train_model()

    elif args.command == "predict":
        text = " ".join(args.text)
        result = classify_request(text)

        print(f"Request: {text}")
        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Source: {result['source']}")

    elif args.command == "test":
        test_cases = [
            ("Explain black holes to me", "chat"),
            ("Create a new Python skill for GENESIS", "create_skill"),
            ("Fix this traceback in my Python program", "debug_code"),
            ("Refactor the code without removing features", "improve_code"),
        ]

        failures = 0

        for request, expected in test_cases:
            result = classify_request(request)
            passed = result["intent"] == expected

            print(
                f"[{'PASS' if passed else 'FAIL'}] "
                f"{request}\n"
                f"  Expected: {expected}\n"
                f"  Actual:   {result['intent']}\n"
                f"  Source:   {result['source']}\n"
            )

            if not passed:
                failures += 1

        print(f"Test result: {len(test_cases) - failures}/"
              f"{len(test_cases)} passed.")

        if failures:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
