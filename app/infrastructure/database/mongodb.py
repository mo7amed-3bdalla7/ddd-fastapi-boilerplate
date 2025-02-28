from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.config.settings import get_settings

settings = get_settings()


class MongoDB:
    client: AsyncIOMotorClient = None
    database_name: str = None

    async def connect_to_database(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.database_name = settings.DATABASE_NAME

    async def close_database_connection(self):
        if self.client:
            self.client.close()


db = MongoDB()
