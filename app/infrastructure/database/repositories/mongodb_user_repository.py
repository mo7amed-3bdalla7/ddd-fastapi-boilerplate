from typing import List
from datetime import datetime
from uuid import UUID, uuid4
from bson import ObjectId

from app.application.interfaces.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.database.mongodb import db

class MongoDBUserRepository(UserRepository):
    def __init__(self):
        self.collection = db.client[db.database_name]["users"]

    async def create_user(self, user: User) -> User:
        user_dict = {
            "_id": str(uuid4()),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        
        await self.collection.insert_one(user_dict)
        user.id = UUID(user_dict["_id"])
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        user_dict = await self.collection.find_one({"email": email})
        if not user_dict:
            return None
            
        return User(
            id=UUID(str(user_dict["_id"])),
            username=user_dict["username"],
            email=user_dict["email"],
            full_name=user_dict["full_name"],
            created_at=user_dict["created_at"],
            updated_at=user_dict.get("updated_at")
        )

    async def list_users(self) -> List[User]:
        users = []
        async for user_dict in self.collection.find():
            user = User(
                id=UUID(str(user_dict["_id"])),
                username=user_dict["username"],
                email=user_dict["email"],
                full_name=user_dict["full_name"],
                created_at=user_dict["created_at"],
                updated_at=user_dict.get("updated_at")
            )
            users.append(user)
        return users 