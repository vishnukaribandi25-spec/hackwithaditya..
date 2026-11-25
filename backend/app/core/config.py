import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    frontend_origins: tuple[str, ...]
    gemini_api_key: str | None
    gemini_model: str


def get_settings() -> Settings:
    origins_value = os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    frontend_origins = tuple(
        origin.strip() for origin in origins_value.split(",") if origin.strip()
    )
    if not frontend_origins:
        raise ValueError("FRONTEND_ORIGINS must contain at least one origin")

    return Settings(
        app_name=os.getenv("APP_NAME", "SchemeSathi API"),
        app_version=os.getenv("APP_VERSION", "1.0.0"),
        frontend_origins=frontend_origins,
        gemini_api_key=os.getenv("GEMINI_API_KEY", "").strip() or None,
        gemini_model=os.getenv("GEMINI_MODEL", "").strip() or "gemini-flash-latest",
    )
