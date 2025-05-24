from fastapi import FastAPI

from routes import api_routes, model_routes


def register_routes(app: FastAPI):
    """
    Register all routes for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    """
    app.include_router(
        router=api_routes.router,
        prefix="/api",
        responses={"404": {"description": "Not Found"}},
    )

    app.include_router(
        router=model_routes.router,
        prefix="/model",
        responses={"404": {"description": "Not Found"}},
    )
