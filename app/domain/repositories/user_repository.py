from abc import ABC, abstractmethod
from app.domain.entities.user import User


class UserRepository(ABC):
    
    @abstractmethod
    async def create(self, user) -> User:
        pass
   
    @abstractmethod
    async def get_by_email(self, email) -> User | None:
        pass
 
    @abstractmethod
    async def get_by_id(self, user_id) -> User | None:
        pass
 
    @abstractmethod
    async def exists_by_email(self, email) -> bool:
        pass

    @abstractmethod
    async def update(self, user_id: int, user_data: dict) -> User:
        pass

    @abstractmethod
    async def get_users_after(self, last_id: int | None = None, limit: int = 100) -> list[User]:
        pass