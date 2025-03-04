import uuid
from contextlib import asynccontextmanager

import tomllib
from fastapi import FastAPI, Request
from loguru import logger

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


app.include_router(user_routes.router)
app.include_router(ping_pong.router)
