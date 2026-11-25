import logging

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router
from app.api.routes.eligibility import router as eligibility_router
from app.api.routes.eligibility import router as eligibility_router
from app.api.routes.profile import router as profile_router
from app.api.routes.schemes import router as schemes_router
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.frontend_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(eligibility_router, prefix="/api")
app.include_router(eligibility_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(schemes_router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = []
    for error in exc.errors():
        if "social_category" in error.get("loc", ()):
            errors.append(
                {
                    "loc": error["loc"],
                    "msg": "Select one of the supported social-category options.",
                    "type": "value_error",
                }
            )
        else:
            errors.append(error)
    return JSONResponse(status_code=422, content={"detail": jsonable_encoder(errors)})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled error while processing %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
