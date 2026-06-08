from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

from app.cockpit.simulator import CockpitSimulator
from app.dialogue.pipeline import DialoguePipeline
from app.evaluation.evaluator import EvalCase, evaluate_cases, reported_metrics
from app.llm.function_calling import FUNCTION_SCHEMAS
from app.mcp.registry import TOOL_REGISTRY
from app.schemas.dialogue import (
    CockpitApplyResponse,
    DialogueRequest,
    DialogueResponse,
    HealthResponse,
)

router = APIRouter()
pipeline = DialoguePipeline()
cockpit = CockpitSimulator()
static_dir = Path(__file__).resolve().parents[1] / "static"


@router.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/v1/dialogue/parse", response_model=DialogueResponse)
def parse_dialogue(request: DialogueRequest) -> DialogueResponse:
    return pipeline.parse(request)


@router.post("/v1/cockpit/apply", response_model=CockpitApplyResponse)
def apply_cockpit(request: DialogueRequest) -> CockpitApplyResponse:
    dialogue = pipeline.parse(request)
    return cockpit.apply(request, dialogue)


@router.get("/v1/mcp/tools")
def list_tools() -> dict[str, list[str]]:
    return {"tools": sorted(TOOL_REGISTRY.keys())}


@router.get("/v1/function-schemas")
def list_function_schemas() -> dict[str, dict[str, object]]:
    return {
        intent.value: {
            "name": schema.name,
            "description": schema.description,
            "parameters": schema.parameters,
        }
        for intent, schema in FUNCTION_SCHEMAS.items()
    }


@router.get("/v1/evaluation/sample")
def sample_evaluation() -> dict[str, float]:
    cases = [
        EvalCase("导航去北京南站", "NAVIGATE"),
        EvalCase("播放周杰伦的歌", "PLAY_MUSIC"),
        EvalCase("查询北京天气", "WEATHER_QUERY"),
        EvalCase("打开空调", "VEHICLE_CONTROL"),
    ]
    return evaluate_cases(cases)


@router.get("/v1/evaluation/reported-metrics")
def evaluation_reported_metrics() -> dict[str, object]:
    return reported_metrics()
