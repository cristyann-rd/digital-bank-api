from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.infrastructure.database.connection import get_db
from src.app.domain.repositories.account_repository import AccountRepository
from src.app.infrastructure.repositories.account_repository_sqlalchemy import AccountRepositorySQLAlchemy
from src.app.application.services.account_service  import AccountService
from src.app.domain.unit_of_work import UnitOfWork
from src.app.infrastructure.uow import SqlAlchemyUnitOfWork


async def get_uow(session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)


def get_account_repository(db: AsyncSession = Depends(get_db)) -> AccountRepository:
    return AccountRepositorySQLAlchemy(db)

def get_account_service(
    uow: UnitOfWork = Depends(get_uow)
):
    return AccountService(uow)

