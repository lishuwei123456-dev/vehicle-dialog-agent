from dataclasses import dataclass
from typing import Any

from app.dialogue.intents import Intent


@dataclass(frozen=True)
class FunctionSchema:
    name: str
    description: str
    parameters: dict[str, Any]


FUNCTION_SCHEMAS: dict[Intent, FunctionSchema] = {
    Intent.NAVIGATE: FunctionSchema(
        name="start_navigation",
        description="Create a route plan to a destination.",
        parameters={"destination": {"type": "string", "required": True}},
    ),
    Intent.PLAY_MUSIC: FunctionSchema(
        name="search_music",
        description="Search and play music by song, artist, album, or keyword.",
        parameters={"keyword": {"type": "string", "required": True}},
    ),
    Intent.WEATHER_QUERY: FunctionSchema(
        name="query_weather",
        description="Query weather by city and date.",
        parameters={"city": {"type": "string", "required": False}},
    ),
    Intent.VEHICLE_CONTROL: FunctionSchema(
        name="control_vehicle_device",
        description="Control vehicle devices such as climate, windows, seats, and volume.",
        parameters={
            "target": {"type": "string", "required": True},
            "action": {"type": "string", "required": True},
        },
    ),
}


class FunctionCallingPlanner:
    """Builds a function-call-like plan without requiring a paid LLM service."""

    def plan(self, intent: Intent, slots: dict[str, str]) -> dict[str, Any]:
        schema = FUNCTION_SCHEMAS.get(intent)
        if schema is None:
            return {"name": "fallback", "arguments": {}}
        return {"name": schema.name, "arguments": slots, "schema": schema.parameters}
