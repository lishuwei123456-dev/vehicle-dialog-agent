"""Train a BERT/RoBERTa text classifier on AutoDL.

This script is intentionally generic. It expects JSONL rows:
{"text": "...", "label": "NAVIGATE"}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("training/data/intent_sample.jsonl"))
    parser.add_argument("--model", default="hfl/chinese-roberta-wwm-ext")
    parser.add_argument("--output", type=Path, default=Path("outputs/intent-roberta"))
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()

    try:
        from datasets import Dataset
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            DataCollatorWithPadding,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise SystemExit("Install training dependencies with: pip install -r requirements-train.txt") from exc

    rows = load_jsonl(args.data)
    labels = sorted({row["label"] for row in rows})
    label2id = {label: index for index, label in enumerate(labels)}
    id2label = {index: label for label, index in label2id.items()}
    dataset = Dataset.from_list([{"text": row["text"], "label": label2id[row["label"]]} for row in rows])
    split = dataset.train_test_split(test_size=0.2, seed=42)

    tokenizer = AutoTokenizer.from_pretrained(args.model)

    def tokenize(batch: dict[str, list[str]]) -> dict[str, list[list[int]]]:
        return tokenizer(batch["text"], truncation=True, max_length=64)

    encoded = split.map(tokenize, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model,
        num_labels=len(labels),
        id2label=id2label,
        label2id=label2id,
    )
    training_args = TrainingArguments(
        output_dir=str(args.output),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_steps=10,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encoded["train"],
        eval_dataset=encoded["test"],
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
    )
    trainer.train()
    trainer.save_model(str(args.output))
    tokenizer.save_pretrained(str(args.output))


if __name__ == "__main__":
    main()
