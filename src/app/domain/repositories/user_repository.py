from uuid import UUID

from abc import ABC, abstractmethod
from app.domain.entities.user import User


class UserRepository(ABC):
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
   
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass
 
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        pass
 
    @abstractmethod
    async def exists_by_email(self, email) -> bool:
        pass

    @abstractmethod
    async def update(self, user_id: UUID, user_data: dict) -> User:
        pass

    @abstractmethod
    async def get_users_after(self, last_id: UUID | None = None, limit: int = 100) -> list[User]:
        pass
