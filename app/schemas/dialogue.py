from typing import Any

from pydantic import BaseModel, Field

from app.dialogue.intents import Intent


class HealthResponse(BaseModel):
    status: str


class DialogueRequest(BaseModel):
    query: str = Field(..., min_length=0, description="User utterance.")
    session_id: str = Field(default="demo", description="Conversation session id.")


class DialogueResponse(BaseModel):
    query: str
    accepted: bool
    intent: Intent
    confidence: float = Field(..., ge=0.0, le=1.0)
    slots: dict[str, str]
    function_call: dict[str, Any] = Field(default_factory=dict)
    tool_result: dict[str, Any] = Field(default_factory=dict)
    reply: str


class CockpitState(BaseModel):
    session_id: str
    climate_on: bool = False
    cabin_temperature: int = Field(default=24, ge=16, le=32)
    window_position: int = Field(default=0, ge=0, le=100)
    seat_heat: bool = False
    volume: int = Field(default=42, ge=0, le=100)
    media_title: str = "未播放"
    media_status: str = "idle"
    navigation_destination: str = "未设置"
    weather_city: str = "当前城市"
    weather_summary: str = "暂无天气"
    last_action: str = "Ready"


class ModuleTrace(BaseModel):
    name: str
    status: str
    detail: str


class CockpitApplyResponse(BaseModel):
    dialogue: DialogueResponse
    state: CockpitState
    modules: list[ModuleTrace]
