from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.infrastructure.models.user import UserModel
from app.domain.repositories.user_repository import UserRepository, User

class UserRepositorySQLAlchemy(UserRepository):
    
    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password_hash=db_user.password_hash,
        )
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        db_user = UserModel(
            name=user.name,
            email=user.email,
            password_hash=user.password_hash
        )

        self.session.add(db_user)

        await self.session.flush()  
        await self.session.commit()
        await self.session.refresh(db_user)

        return self._to_domain(db_user)
    
    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return self._to_domain(db_user) if db_user else None
    
    async def get_by_id(self, user_id: int) -> User | None:
        db_user = await self.session.get(UserModel, user_id)
        return self._to_domain(db_user) if db_user else None
    
    async def exists_by_email(self, email: str) -> bool:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        return db_user is not None

    async def update(self, user_id: int, user_data: dict) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise HTTPException(status_code=404, 
                                detail="Usuário não encontrado")

        for key, value in user_data.items():
            setattr(db_user, key, value)

            await self.session.commit()
            await self.session.refresh(db_user)

        return self._to_domain(db_user)
    
    async def get_users_after(
        self,
        last_id: int | None = None,
        limit: int = 100,
    ) -> list[User]:
        
        stmt = select(UserModel).order_by(UserModel.id).limit(limit)

        if last_id is not None:
            
            stmt = stmt.where(UserModel.id > last_id)

        result = await self.session.execute(stmt)

        users = result.scalars().all()

        return [self._to_domain(user) for user in users]