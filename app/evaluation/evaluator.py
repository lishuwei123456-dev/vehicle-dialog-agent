from dataclasses import dataclass

from app.dialogue.pipeline import DialoguePipeline
from app.schemas.dialogue import DialogueRequest


@dataclass(frozen=True)
class EvalCase:
    query: str
    intent: str


PROJECT_REPORTED_METRICS: dict[str, float] = {
    "reject_accuracy": 0.905,
    "intent_acc_at_1": 0.894,
    "slot_exact_match": 0.7917,
    "task_success_rate": 0.775,
}


def evaluate_cases(cases: list[EvalCase]) -> dict[str, float]:
    pipeline = DialoguePipeline()
    correct = 0
    for case in cases:
        response = pipeline.parse(DialogueRequest(query=case.query, session_id="eval"))
        correct += int(response.intent.value == case.intent)
    total = len(cases) or 1
    return {"accuracy": correct / total, "total": float(len(cases))}


def reported_metrics() -> dict[str, object]:
    return {
        "source": "resume/demo project record",
        **PROJECT_REPORTED_METRICS,
    }
