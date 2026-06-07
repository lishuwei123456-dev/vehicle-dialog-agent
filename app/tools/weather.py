from app.core.config import get_settings


CITY_COORDINATES = {
    "当前城市": (39.9042, 116.4074),
    "北京": (39.9042, 116.4074),
    "上海": (31.2304, 121.4737),
    "广州": (23.1291, 113.2644),
    "深圳": (22.5431, 114.0579),
    "杭州": (30.2741, 120.1551),
    "成都": (30.5728, 104.0668),
    "重庆": (29.5630, 106.5516),
    "武汉": (30.5928, 114.3055),
    "南京": (32.0603, 118.7969),
}


def query_weather(city: str) -> dict[str, str]:
    settings = get_settings()
    if settings.weather_provider == "open-meteo":
        return query_open_meteo(city)
    return query_demo_weather(city)


def query_demo_weather(city: str) -> dict[str, str]:
    return {
        "city": city,
        "condition": "晴",
        "temperature": "26",
        "wind": "微风",
        "suggestion": "适合通勤和短途出行",
    }


def query_open_meteo(city: str) -> dict[str, str]:
    import httpx

    lat, lon = CITY_COORDINATES.get(city, CITY_COORDINATES["当前城市"])
    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "timezone": "Asia/Shanghai",
        },
        timeout=5,
    )
    response.raise_for_status()
    current = response.json()["current"]
    return {
        "city": city,
        "condition": weather_code_to_text(int(current.get("weather_code", 0))),
        "temperature": str(current.get("temperature_2m", "--")),
        "wind": f"{current.get('wind_speed_10m', '--')} km/h",
        "suggestion": "实时天气来自 Open-Meteo",
    }


def weather_code_to_text(code: int) -> str:
    if code == 0:
        return "晴"
    if code in {1, 2, 3}:
        return "多云"
    if code in {45, 48}:
        return "有雾"
    if code in {51, 53, 55, 61, 63, 65, 80, 81, 82}:
        return "有雨"
    if code in {71, 73, 75, 85, 86}:
        return "有雪"
    if code in {95, 96, 99}:
        return "雷雨"
    return "天气变化"
