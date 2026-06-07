from app.dialogue.intents import Intent
from app.schemas.dialogue import (
    CockpitApplyResponse,
    CockpitState,
    DialogueRequest,
    DialogueResponse,
    ModuleTrace,
)


class CockpitSimulator:
    """In-memory cockpit state for local demonstrations."""

    def __init__(self) -> None:
        self._states: dict[str, CockpitState] = {}

    def apply(
        self,
        request: DialogueRequest,
        dialogue: DialogueResponse,
    ) -> CockpitApplyResponse:
        state = self._get_state(request.session_id)
        modules = self._build_trace(dialogue)

        if not dialogue.accepted:
            state.last_action = dialogue.reply
            modules.append(ModuleTrace(name="Cockpit Simulator", status="skipped", detail="No state change"))
            return CockpitApplyResponse(dialogue=dialogue, state=state, modules=modules)

        query = request.query
        if dialogue.intent == Intent.NAVIGATE:
            destination = dialogue.slots.get("destination", "未识别目的地")
            state.navigation_destination = destination
            state.last_action = f"Route preview prepared for {destination}"
        elif dialogue.intent == Intent.PLAY_MUSIC:
            keyword = dialogue.slots.get("keyword", "推荐音乐")
            state.media_title = keyword
            state.media_status = "playing"
            state.last_action = f"Searching media for {keyword}"
        elif dialogue.intent == Intent.WEATHER_QUERY:
            city = dialogue.slots.get("city", "当前城市")
            state.weather_city = city
            state.weather_summary = f"{city} 晴，26 度，适合出行"
            state.last_action = f"Weather card refreshed for {city}"
        elif dialogue.intent == Intent.VEHICLE_CONTROL:
            self._apply_vehicle_control(state, dialogue.slots, query)
        else:
            state.last_action = "No cockpit module matched"

        modules.append(ModuleTrace(name="Cockpit Simulator", status="updated", detail=state.last_action))
        self._states[request.session_id] = state
        return CockpitApplyResponse(dialogue=dialogue, state=state, modules=modules)

    def _get_state(self, session_id: str) -> CockpitState:
        if session_id not in self._states:
            self._states[session_id] = CockpitState(session_id=session_id)
        return self._states[session_id].model_copy(deep=True)

    def _apply_vehicle_control(
        self,
        state: CockpitState,
        slots: dict[str, str],
        query: str,
    ) -> None:
        target = slots.get("target", "vehicle_device")
        action = slots.get("action", "adjust")

        if target == "air_conditioner":
            if action == "close":
                state.climate_on = False
                state.last_action = "Climate switched off"
            else:
                state.climate_on = True
                state.last_action = "Climate switched on"
        elif target == "window":
            state.window_position = 0 if action == "close" else 60
            state.last_action = f"Window position set to {state.window_position}%"
        elif target == "seat":
            state.seat_heat = action != "close"
            state.last_action = "Seat comfort setting updated"
        elif target == "volume":
            delta = -8 if action in {"close", "decrease"} or "小" in query else 8
            state.volume = min(100, max(0, state.volume + delta))
            state.last_action = f"Volume adjusted to {state.volume}"
        else:
            state.last_action = "Vehicle control command parsed"

    def _build_trace(self, dialogue: DialogueResponse) -> list[ModuleTrace]:
        reject_status = "passed" if dialogue.accepted else "blocked"
        return [
            ModuleTrace(name="Reject Detector", status=reject_status, detail=dialogue.reply),
            ModuleTrace(
                name="Intent Classifier",
                status=dialogue.intent.value,
                detail=f"confidence={dialogue.confidence:.2f}",
            ),
            ModuleTrace(name="Slot Extractor", status="ready", detail=str(dialogue.slots or {})),
        ]
