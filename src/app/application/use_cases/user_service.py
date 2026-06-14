import uuid
from uuid import UUID

from app.application.ports.security import PasswordHasher
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import (
    DuplicateEmailError,
    UserNotFoundError,
)
from app.domain.repositories.user_repository import UserRepository
from app.domain.validators.password_validator import PasswordValidator


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_validator: PasswordValidator,
        password_hasher: PasswordHasher,
    ):
        self.user_repository = user_repository
        self.password_validator = password_validator
        self.password_hasher = password_hasher

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email.strip().lower())

    async def create_user(self, name: str, email: str, password: str) -> User:
        normalized_email = email.strip().lower()
        if await self.user_repository.exists_by_email(normalized_email):
            raise DuplicateEmailError("Email ja existe no sistema")

        self.password_validator.validate(password)

        user = User(
            id=uuid.uuid4(),
            name=name.strip(),
            email=normalized_email,
            password_hash=self.password_hasher.hash(password),
        )
        return await self.user_repository.create(user)

    async def update_user(self, user_id: UUID, user_data: dict) -> User:
        current_user = await self.user_repository.get_by_id(user_id)
        if current_user is None:
            raise UserNotFoundError("Usuario nao encontrado")

        data = dict(user_data)
        if "email" in data:
            normalized_email = str(data["email"]).strip().lower()
            existing_user = await self.user_repository.get_by_email(normalized_email)
            if existing_user is not None and existing_user.id != user_id:
                raise DuplicateEmailError("Email ja existe no sistema")
            data["email"] = normalized_email

        if "password" in data:
            password = data.pop("password")
            self.password_validator.validate(password)
            data["password_hash"] = self.password_hasher.hash(password)

        if "name" in data:
            data["name"] = str(data["name"]).strip()

        if not data:
            return current_user

        return await self.user_repository.update(user_id, data)

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_users_after()

    async def email_exists(self, email: str) -> bool:
        return await self.user_repository.exists_by_email(email.strip().lower())
