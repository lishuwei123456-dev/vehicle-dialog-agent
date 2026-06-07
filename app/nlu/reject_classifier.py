from dataclasses import dataclass


@dataclass(frozen=True)
class RejectPrediction:
    accepted: bool
    confidence: float
    reason: str


class RejectClassifier:
    """Rule-based reject detector for invalid or non-actionable input."""

    def predict(self, query: str) -> RejectPrediction:
        text = query.strip()
        if not text:
            return RejectPrediction(False, 0.99, "未收到有效输入。")
        if len(text) == 1 and text not in {"去", "听", "开"}:
            return RejectPrediction(False, 0.92, "输入过短，暂时无法理解。")
        if text in {"啊啊啊", "哈哈哈", "嗯嗯嗯", "。。。", "..."}:
            return RejectPrediction(False, 0.94, "输入缺少明确意图。")
        if len(set(text)) <= 2 and len(text) >= 4:
            return RejectPrediction(False, 0.88, "输入重复度过高，缺少明确语义。")
        return RejectPrediction(True, 0.86, "通过拒识检测。")
