from fastapi import FastAPI
from app.infrastructure.database.mongodb import db
from app.infrastructure.api.routes import user_routes, ping_pong

app = FastAPI(title="DDD FastAPI Boilerplate")

@app.on_event("startup")
async def startup():
    await db.connect_to_database()

@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()

app.include_router(user_routes.router) 
app.include_router(ping_pong.router)