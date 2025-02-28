from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    async def list_users(self) -> List[User]:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        pass 