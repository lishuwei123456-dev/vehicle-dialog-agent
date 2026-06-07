from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes import router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    static_dir = Path(__file__).resolve().parent / "static"
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Vehicle task-oriented dialogue system for course and graduation design.",
    )
    application.mount("/static", StaticFiles(directory=static_dir), name="static")
    application.include_router(router)
    return application


app = create_app()
