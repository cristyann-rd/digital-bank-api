from uuid import UUID

from app.application.ports.security import PasswordHasher, TokenManager
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_manager: TokenManager,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_manager = token_manager

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_repository.get_by_email(email.strip().lower())
        if not user:
            return None
        if not self.password_hasher.verify(password, user.password_hash):
            return None
        return user

    async def login(self, email: str, password: str) -> User | None:
        return await self.authenticate_user(email, password)

    def create_token(self, user_id: UUID) -> str:
        return self.token_manager.create_access_token(user_id)

    async def get_user_from_token(self, token: str) -> User | None:
        user_id = self.token_manager.decode_access_token(token)
        if user_id is None:
            return None
        return await self.user_repository.get_by_id(user_id)

    async def current_user(self, token: str) -> User | None:
        return await self.get_user_from_token(token)
