from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.api.routes import ping_pong, user_routes
from app.infrastructure.database.mongodb import db


@asynccontextmanager
async def lifespan(the_app: FastAPI):
    the_app.title = "DDD FastAPI Boilerplate"

    # Startup: Connect to the database
    await db.connect_to_database()

    yield  # This is where the FastAPI application runs

    # Shutdown: Close the database connection
    await db.close_database_connection()


app = FastAPI(lifespan=lifespan)

app.include_router(user_routes.router)
app.include_router(ping_pong.router)
