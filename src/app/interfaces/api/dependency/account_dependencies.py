from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from src.app.domain.services.account_number_generator import AccountNumberGenerator
from src.app.application.use_cases.account_usecase  import AccountUseCase
from src.app.domain.repositories.account_repository import AccountRepository
from src.app.domain.unit_of_work import UnitOfWork
from src.app.infrastructure.database.connection import get_db
from src.app.infrastructure.generators.sequential_account_generator import SequentialAccountGenerator
from src.app.infrastructure.repositories.account_repository_sqlalchemy import AccountRepositorySQLAlchemy

from src.app.infrastructure.uow import SqlAlchemyUnitOfWork


async def get_uow(session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)


def get_account_repository(db: AsyncSession = Depends(get_db)) -> AccountRepository:
    return AccountRepositorySQLAlchemy(db)


def get_account_number_generator():
    return SequentialAccountGenerator()


def get_account_use_case(
    uow: UnitOfWork = Depends(get_uow),
    account_number_generator: AccountNumberGenerator = Depends(get_account_number_generator),
):
    return AccountUseCase(
        uow,
        account_number_generator
    )

