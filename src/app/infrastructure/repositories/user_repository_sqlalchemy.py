from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import (
    DuplicateEmailError,
    UserNotFoundError,
)
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.models.user import UserModel


class UserRepositorySQLAlchemy(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password_hash=db_user.password_hash,
        )

    async def create(self, user: User) -> User:
        db_user = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
        )
        self.session.add(db_user)

        try:
            await self.session.commit()
            await self.session.refresh(db_user)
        except IntegrityError as exc:
            await self.session.rollback()
            raise DuplicateEmailError("Email ja existe no sistema") from exc

        return self._to_domain(db_user)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_domain(db_user) if db_user else None

    async def get_by_id(self, user_id: UUID) -> User | None:
        db_user = await self.session.get(UserModel, user_id)
        return self._to_domain(db_user) if db_user else None

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(UserModel.id).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def update(self, user_id: UUID, user_data: dict) -> User:
        db_user = await self.session.get(UserModel, user_id)
        if db_user is None:
            raise UserNotFoundError("Usuario nao encontrado")

        for key, value in user_data.items():
            setattr(db_user, key, value)

        try:
            await self.session.commit()
            await self.session.refresh(db_user)
        except IntegrityError as exc:
            await self.session.rollback()
            raise DuplicateEmailError("Email ja existe no sistema") from exc

        return self._to_domain(db_user)

    async def get_users_after(
        self,
        last_id: UUID | None = None,
        limit: int = 100,
    ) -> list[User]:
        stmt = select(UserModel).order_by(UserModel.id).limit(limit)
        if last_id is not None:
            stmt = stmt.where(UserModel.id > last_id)

        result = await self.session.execute(stmt)
        return [self._to_domain(user) for user in result.scalars().all()]
