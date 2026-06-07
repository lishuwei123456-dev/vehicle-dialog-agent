from app.dialogue.intents import Intent


class SlotExtractor:
    """Deterministic slot extractor that mirrors function-calling output."""

    def extract(self, query: str, intent: Intent) -> dict[str, str]:
        if intent == Intent.NAVIGATE:
            return self._navigation(query)
        if intent == Intent.PLAY_MUSIC:
            return self._music(query)
        if intent == Intent.WEATHER_QUERY:
            return self._weather(query)
        if intent == Intent.VEHICLE_CONTROL:
            return self._vehicle_control(query)
        return {}

    def _navigation(self, query: str) -> dict[str, str]:
        for prefix in ("导航去", "带我去", "去"):
            if prefix in query:
                destination = query.split(prefix, 1)[1].strip()
                if destination:
                    return {"destination": destination}
        return {}

    def _music(self, query: str) -> dict[str, str]:
        for prefix in ("播放", "放一首", "听"):
            if prefix in query:
                keyword = query.split(prefix, 1)[1].strip()
                if keyword:
                    return {"keyword": keyword}
        return {}

    def _weather(self, query: str) -> dict[str, str]:
        for city in ("北京", "上海", "广州", "深圳", "杭州", "成都", "重庆", "武汉", "南京"):
            if city in query:
                return {"city": city}
        return {"city": "当前城市"}

    def _vehicle_control(self, query: str) -> dict[str, str]:
        target_map = {
            "空调": "air_conditioner",
            "车窗": "window",
            "座椅": "seat",
            "音量": "volume",
        }
        if "打开" in query:
            action = "open"
        elif "关闭" in query:
            action = "close"
        elif any(word in query for word in ("调高", "增大", "大一点", "升高")):
            action = "increase"
        elif any(word in query for word in ("调低", "降低", "小一点")):
            action = "decrease"
        else:
            action = "adjust"
        for keyword, target in target_map.items():
            if keyword in query:
                return {"target": target, "action": action}
        return {"target": "vehicle_device", "action": action}
