from uuid import UUID
from src.app.domain.repositories.user_repository import UserRepository
from src.app.core.security import verify_password, create_access_token, decode_access_token

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    async def login(self, email: str, password: str):
        user = await self.authenticate_user(email, password)
        if not user:
            return None
        return user

    def create_token(self, user_id: UUID):
        return create_access_token(user_id)

    async def get_user_from_token(self, token: str):
        user_id = decode_access_token(token)
        if user_id is None:
            return None
        return await self.user_repository.get_by_id(user_id)
    
    async def current_user(self, token: str):
        return await self.get_user_from_token(token)