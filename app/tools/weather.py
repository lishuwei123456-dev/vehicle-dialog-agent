def query_weather(city: str) -> dict[str, str]:
    return {
        "city": city,
        "condition": "晴",
        "temperature": "26",
        "wind": "微风",
        "suggestion": "适合通勤和短途出行",
    }
