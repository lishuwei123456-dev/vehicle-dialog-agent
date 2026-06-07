from typing import Any

from app.dialogue.intents import Intent
from app.dialogue.state_store import create_state_store
from app.llm.function_calling import FunctionCallingPlanner
from app.mcp.registry import call_tool
from app.nlu.intent_classifier import IntentClassifier
from app.nlu.reject_classifier import RejectClassifier
from app.nlu.slot_extractor import SlotExtractor
from app.schemas.dialogue import DialogueRequest, DialogueResponse


class DialoguePipeline:
    """Dialogue orchestration: reject detection, intent, slots, tools, and state."""

    def __init__(self) -> None:
        self.rejector = RejectClassifier()
        self.intent_classifier = IntentClassifier()
        self.slot_extractor = SlotExtractor()
        self.function_planner = FunctionCallingPlanner()
        self.state_store = create_state_store()

    def parse(self, request: DialogueRequest) -> DialogueResponse:
        query = request.query.strip()
        reject = self.rejector.predict(query)
        if not reject.accepted:
            return DialogueResponse(
                query=request.query,
                accepted=False,
                intent=Intent.UNKNOWN,
                confidence=0.0,
                slots={},
                function_call={},
                tool_result={},
                reply=reject.reason,
            )

        prediction = self.intent_classifier.predict(query)
        slots = self.slot_extractor.extract(query, prediction.intent)
        function_call = self.function_planner.plan(prediction.intent, slots)
        tool_result = self._execute_tool(function_call)
        reply = self._build_reply(prediction.intent, slots, tool_result)
        response = DialogueResponse(
            query=request.query,
            accepted=prediction.intent != Intent.UNKNOWN,
            intent=prediction.intent,
            confidence=prediction.confidence,
            slots=slots,
            function_call=function_call,
            tool_result=tool_result,
            reply=reply,
        )
        self.state_store.append(request.session_id, query, response.intent.value, response.reply)
        return response

    def _execute_tool(self, function_call: dict[str, Any]) -> dict[str, Any]:
        name = function_call.get("name", "")
        arguments = function_call.get("arguments", {})
        if name in {"start_navigation", "search_music", "query_weather"}:
            return call_tool(name, arguments)
        return {}

    def _build_reply(self, intent: Intent, slots: dict[str, str], tool_result: dict[str, Any]) -> str:
        if intent == Intent.NAVIGATE:
            destination = tool_result.get("destination") or slots.get("destination", "目标地点")
            eta = tool_result.get("eta", "待计算")
            return f"已规划前往{destination}的路线，预计{eta}。"
        if intent == Intent.PLAY_MUSIC:
            title = tool_result.get("title") or slots.get("keyword", "音乐")
            return f"已为你准备播放：{title}。"
        if intent == Intent.WEATHER_QUERY:
            city = tool_result.get("city") or slots.get("city", "当前城市")
            condition = tool_result.get("condition", "未知")
            temperature = tool_result.get("temperature", "--")
            return f"{city}当前{condition}，{temperature}度。"
        if intent == Intent.VEHICLE_CONTROL:
            target = slots.get("target", "vehicle_device")
            action = slots.get("action", "adjust")
            return f"车辆控制指令已解析：{target} -> {action}。"
        return "暂时没有识别到明确任务。"
