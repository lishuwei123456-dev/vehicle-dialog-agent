from dataclasses import dataclass

from app.dialogue.pipeline import DialoguePipeline
from app.schemas.dialogue import DialogueRequest


@dataclass(frozen=True)
class EvalCase:
    query: str
    intent: str


def evaluate_cases(cases: list[EvalCase]) -> dict[str, float]:
    pipeline = DialoguePipeline()
    correct = 0
    for case in cases:
        response = pipeline.parse(DialogueRequest(query=case.query, session_id="eval"))
        correct += int(response.intent.value == case.intent)
    total = len(cases) or 1
    return {"accuracy": correct / total, "total": float(len(cases))}
