import os
from collections.abc import AsyncIterator
from uuid import UUID

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient


os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "bank_dio_test")
os.environ.setdefault(
    "SECRET_KEY",
    "test-secret-key-with-at-least-32-characters",
)
os.environ.setdefault("TOKEN_EXPIRE_MINUTES", "30")


from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import (
    DuplicateEmailError,
    UserNotFoundError,
)
from app.domain.repositories.user_repository import UserRepository
from app.interfaces.api.dependency.user_dependencies import get_user_repository
from app.main import create_app


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: dict[UUID, User] = {}

    async def create(self, user: User) -> User:
        if await self.exists_by_email(user.email):
            raise DuplicateEmailError("Email ja existe no sistema")
        self.users[user.id] = user
        return user

    async def get_by_email(self, email: str) -> User | None:
        return next(
            (user for user in self.users.values() if user.email == email),
            None,
        )

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self.users.get(user_id)

    async def exists_by_email(self, email: str) -> bool:
        return await self.get_by_email(email) is not None

    async def update(self, user_id: UUID, user_data: dict) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise UserNotFoundError("Usuario nao encontrado")
        for key, value in user_data.items():
            setattr(user, key, value)
        return user

    async def get_users_after(
        self,
        last_id: UUID | None = None,
        limit: int = 100,
    ) -> list[User]:
        users = sorted(self.users.values(), key=lambda user: user.id)
        if last_id is not None:
            users = [user for user in users if user.id > last_id]
        return users[:limit]


@pytest.fixture
def user_repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def app(user_repository: InMemoryUserRepository):
    application = create_app()
    application.dependency_overrides[get_user_repository] = lambda: user_repository
    yield application
    application.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture
async def registered_user(client: AsyncClient) -> dict:
    payload = {
        "name": "Maria Silva",
        "email": "maria@example.com",
        "password": "SenhaForte1!",
    }
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 201
    return payload | {"id": response.json()["id"]}


@pytest_asyncio.fixture
async def access_token(
    client: AsyncClient,
    registered_user: dict,
) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]
