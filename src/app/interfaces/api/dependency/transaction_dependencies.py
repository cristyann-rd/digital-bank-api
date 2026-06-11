from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.entities.transaction import TransactionType
from src.app.application.use_cases.deposit_service import DepositMoneyUseCase
from src.app.application.use_cases.withdraw_service import WithdrawMoneyUseCase
from src.app.domain.repositories.deposit_repository import DepositTransactionRepository
from src.app.domain.repositories.withdraw_repository import WithdrawTransactionRepository
from src.app.domain.unit_of_work import UnitOfWork
from src.app.infrastructure.database.connection import get_db
from src.app.infrastructure.repositories.deposit_repository_sqlalchemy import DepositRepositorySQLAlchemy
from src.app.infrastructure.repositories.withdraw_repository_sqlalchemy import WithdrawRepositorySQLAlchemy

from src.app.infrastructure.uow import SqlAlchemyUnitOfWork

async def get_uow(session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)

def get_deposit_repository(db: AsyncSession = Depends(get_db)) -> DepositTransactionRepository:
    return DepositRepositorySQLAlchemy(db)

def get_withdraw_repository(db: AsyncSession = Depends(get_db)) -> WithdrawTransactionRepository:
    return WithdrawRepositorySQLAlchemy(db)

def get_deposit_service(
    uow: UnitOfWork = Depends(get_uow),
) -> DepositMoneyUseCase:
    return DepositMoneyUseCase(
        uow,
    )

def get_withdraw_service(
    uow: UnitOfWork = Depends(get_uow),
) -> WithdrawMoneyUseCase:
    return WithdrawMoneyUseCase(
        uow
    )
        