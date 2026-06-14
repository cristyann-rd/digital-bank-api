from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.domain.services.account_number_generator import AccountNumberGenerator
from app.application.use_cases.account_usecase  import AccountUseCase
from app.domain.repositories.account_repository import AccountRepository
from app.domain.unit_of_work import UnitOfWork
from app.infrastructure.database.connection import get_db
from app.infrastructure.generators.sequential_account_generator import SequentialAccountGenerator
from app.infrastructure.repositories.account_repository_sqlalchemy import AccountRepositorySQLAlchemy

from app.infrastructure.uow import SqlAlchemyUnitOfWork


_account_number_generator = SequentialAccountGenerator(start=10_000_000)


async def get_uow(session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)


def get_account_repository(db: AsyncSession = Depends(get_db)) -> AccountRepository:
    return AccountRepositorySQLAlchemy(db)


def get_account_number_generator():
    return _account_number_generator


def get_account_use_case(
    uow: UnitOfWork = Depends(get_uow),
    account_number_generator: AccountNumberGenerator = Depends(get_account_number_generator),
):
    return AccountUseCase(
        uow,
        account_number_generator
    )

