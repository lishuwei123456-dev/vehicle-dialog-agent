import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    app_name: str = "vehicle-dialog-agent"
    app_env: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8080
    redis_url: str = "redis://127.0.0.1:6379/0"
    state_backend: str = "memory"
    llm_base_url: str = ""
    llm_api_key: str = ""
    amap_api_key: str = ""
    weather_provider: str = "demo"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "vehicle-dialog-agent"),
        app_env=os.getenv("APP_ENV", "dev"),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        redis_url=os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        state_backend=os.getenv("STATE_BACKEND", "memory"),
        llm_base_url=os.getenv("LLM_BASE_URL", ""),
        llm_api_key=os.getenv("LLM_API_KEY", ""),
        amap_api_key=os.getenv("AMAP_API_KEY", ""),
        weather_provider=os.getenv("WEATHER_PROVIDER", "demo"),
    )
