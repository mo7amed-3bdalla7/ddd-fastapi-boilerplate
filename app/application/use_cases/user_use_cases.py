import datetime
from typing import List

from app.application.interfaces.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.value_objects.email import Email


class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def list_users(self) -> List[User]:
        return await self._user_repository.list_users()

    async def create_user(self, username: str, email: str, full_name: str) -> User:
        # Validate email using value object
        validated_email = Email(email)

        # Check if user already exists
        existing_user = await self._user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Create new user
        user = User(
            username=username,
            email=validated_email.value,
            full_name=full_name,
            created_at=datetime.datetime.now(datetime.UTC),
        )

        # Save and return user
        return await self._user_repository.create_user(user)
