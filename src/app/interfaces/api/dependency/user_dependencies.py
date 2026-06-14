from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.security import PasswordHasher, TokenManager
from app.application.use_cases.auth_service import AuthService
from app.application.use_cases.user_service import UserService
from app.core.security import password_hasher, token_manager
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.validators.password_validator import PasswordValidator
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.user_repository_sqlalchemy import (
    UserRepositorySQLAlchemy,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepositorySQLAlchemy(db)


def get_password_validator() -> PasswordValidator:
    return PasswordValidator()


def get_password_hasher() -> PasswordHasher:
    return password_hasher


def get_token_manager() -> TokenManager:
    return token_manager


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    password_validator: PasswordValidator = Depends(get_password_validator),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> UserService:
    return UserService(user_repository, password_validator, hasher)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    access_token_manager: TokenManager = Depends(get_token_manager),
) -> AuthService:
    return AuthService(user_repository, hasher, access_token_manager)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    user = await auth_service.get_user_from_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
