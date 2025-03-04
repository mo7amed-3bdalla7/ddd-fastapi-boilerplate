import traceback
import uuid
from contextlib import asynccontextmanager

import tomllib
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import JSONResponse

from app.infrastructure.api.routes import ping_pong, user_routes
from app.infrastructure.database.mongodb import db

# Load logging config from pyproject.toml
with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)["tool"]["loguru"]

# Remove default handlers to prevent duplicate logs
logger.remove()

# Add console logger using settings from pyproject.toml
logger.add(
    sink=lambda msg: print(msg, end=""),
    format=config["format"],
    level=config["level"],
    serialize=config["serialize"],
)


@asynccontextmanager
async def lifespan(the_app: FastAPI):
    the_app.title = "DDD FastAPI Boilerplate"

    # Startup: Connect to the database
    await db.connect_to_database()

    yield  # This is where the FastAPI application runs

    # Shutdown: Close the database connection
    await db.close_database_connection()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log incoming requests."""
    response = await call_next(request)

    logger.info(
        {
            "event": "request_handled",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "request_id": str(uuid.uuid4()),
        }
    )
    return response


# Generic Exception Handler (500 Internal Server Error)
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handles unexpected errors and returns traceback as a list of lines."""
    error_trace = traceback.format_exc().splitlines()
    logger.error(f"Unhandled exception: {exc}\n" + "\n".join(error_trace))

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "error": str(exc),
            "traceback": error_trace,
        },
    )


# HTTPException Handler (400, 404, etc.)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles HTTP exceptions and logs them."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


# Validation Error Handler (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles validation errors and returns traceback in JSON list format."""
    error_trace = traceback.format_exc().splitlines()
    logger.error(f"Validation error: {exc.errors()}\n" + "\n".join(error_trace))

    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation Error",
            "details": exc.errors(),
            "traceback": error_trace,
        },
    )


app.include_router(user_routes.router)
app.include_router(ping_pong.router)
