import uuid
from uuid import UUID

from src.app.domain.repositories.user_repository import UserRepository, User
from src.app.core.security import hash_password

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: UUID):
        return await self.user_repository.get_by_id(user_id)

    async def get_by_email(self, email: str):
        return await self.user_repository.get_by_email(email)

    async def create_user(self, name: str, email: str, password: str):
        hashed_password = hash_password(password)
        user = User(
            id= uuid.uuid4(),
            name=name,
            email=email,
            password_hash=hashed_password
        )
        return await self.user_repository.create(user)

    async def update_user(self, user_id: UUID, user_data: dict):
        return await self.user_repository.update(user_id, user_data)

    async def get_all_users(self):
        return await self.user_repository.get_users_after()

    async def email_exists(self, email: str) -> bool:
        return await self.user_repository.exists_by_email(email)