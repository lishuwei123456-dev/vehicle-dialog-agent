from dataclasses import dataclass

from app.dialogue.intents import Intent


@dataclass(frozen=True)
class IntentPrediction:
    intent: Intent
    confidence: float
    matched_keyword: str = ""


class IntentClassifier:
    """Keyword baseline with the same interface as a trainable classifier."""

    def __init__(self) -> None:
        self._rules: list[tuple[Intent, tuple[str, ...], float]] = [
            (Intent.NAVIGATE, ("导航", "带我去", "去", "路线", "怎么走", "目的地"), 0.86),
            (Intent.PLAY_MUSIC, ("播放", "放一首", "听歌", "音乐", "歌曲", "歌手"), 0.84),
            (Intent.WEATHER_QUERY, ("天气", "下雨", "温度", "气温", "空气质量", "会不会冷"), 0.82),
            (Intent.VEHICLE_CONTROL, ("打开", "关闭", "空调", "车窗", "座椅", "音量", "调高", "调低"), 0.80),
        ]

    def predict(self, query: str) -> IntentPrediction:
        for intent, keywords, confidence in self._rules:
            for keyword in keywords:
                if keyword in query:
                    return IntentPrediction(intent=intent, confidence=confidence, matched_keyword=keyword)
        return IntentPrediction(intent=Intent.UNKNOWN, confidence=0.35)

    def topk(self, query: str, k: int = 3) -> list[IntentPrediction]:
        scored = [self.predict(query)]
        for intent, keywords, confidence in self._rules:
            if all(item.intent != intent for item in scored):
                overlap = sum(1 for keyword in keywords if keyword in query)
                score = min(0.74, 0.42 + overlap * 0.16)
                scored.append(IntentPrediction(intent=intent, confidence=score))
        return sorted(scored, key=lambda item: item.confidence, reverse=True)[:k]
