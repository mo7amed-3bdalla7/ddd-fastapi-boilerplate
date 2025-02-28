from app.application.use_cases.user_use_cases import UserUseCases
from app.infrastructure.database.repositories.mongodb_user_repository import MongoDBUserRepository

def get_user_use_cases() -> UserUseCases:
    user_repository = MongoDBUserRepository()
    return UserUseCases(user_repository) 