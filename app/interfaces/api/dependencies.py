from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import get_db
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.repositories.user_repository_sqlalchemy import UserRepositorySQLAlchemy
from src.app.application.use_cases.user_service import UserService
from src.app.application.use_cases.auth_service import AuthService
"""from app.services.exceptions import (
    InvalidTokenError,
    ExpiredTokenError,
    InactiveUserError,
)"""

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_user_repostitory(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepositorySQLAlchemy(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repostitory)) -> UserService:
    return UserService(user_repository)

def get_auth_service(user_repository: UserRepository = Depends(get_user_repostitory)) -> AuthService:
    return AuthService(user_repository)

async def get_current_user(
    token: str = Depends(OAuth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    user = await auth_service.get_user_from_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user