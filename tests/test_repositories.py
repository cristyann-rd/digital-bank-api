from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.domain.entities.user import User
from app.infrastructure.models.user import UserModel
from app.infrastructure.repositories.user_repository_sqlalchemy import (
    UserRepositorySQLAlchemy,
)


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
    )
    async with engine.begin() as connection:
        await connection.run_sync(UserModel.__table__.create)

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with session_factory() as session:
        yield session

    await engine.dispose()


async def test_async_repository_saves_and_fetches_user(
    db_session: AsyncSession,
) -> None:
    repository = UserRepositorySQLAlchemy(db_session)
    user = User(
        id=uuid4(),
        name="Repositorio Async",
        email="repository@example.com",
        password_hash="not-a-plain-password",
    )

    created_user = await repository.create(user)
    fetched_user = await repository.get_by_email(user.email)

    assert created_user == user
    assert fetched_user == user


async def test_database_constraint_blocks_duplicate_email(
    db_session: AsyncSession,
) -> None:
    db_session.add_all(
        [
            UserModel(
                id=uuid4(),
                name="Primeiro",
                email="duplicate@example.com",
                password_hash="hash-1",
            ),
            UserModel(
                id=uuid4(),
                name="Segundo",
                email="duplicate@example.com",
                password_hash="hash-2",
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        await db_session.commit()

    await db_session.rollback()
