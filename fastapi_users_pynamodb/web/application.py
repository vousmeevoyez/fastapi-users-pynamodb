from fastapi import FastAPI
from fastapi.responses import UJSONResponse
import logging
from fastapi_users_pynamodb.web.api.router import api_router
from fastapi_users_pynamodb.settings import settings
from fastapi_users_pynamodb.web.lifetime import register_startup_event, register_shutdown_event
from importlib import metadata


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="fastapi_users_pynamodb",
        version=metadata.version("fastapi_users_pynamodb"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
