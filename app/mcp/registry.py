from app.tools.map import start_navigation
from app.tools.music import search_music
from app.tools.weather import query_weather


TOOL_REGISTRY = {
    "start_navigation": start_navigation,
    "search_music": search_music,
    "query_weather": query_weather,
}


def call_tool(name: str, arguments: dict[str, str]) -> dict[str, str]:
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        return {"error": f"unknown tool: {name}"}
    return tool(**arguments)
