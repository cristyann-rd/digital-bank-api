from abc import ABC, abstractmethod

from src.app.domain.repositories.account_repository import AccountRepository
from src.app.domain.repositories.deposit_repository import DepositTransactionRepository
from src.app.domain.repositories.withdraw_repository import WithdrawTransactionRepository


class UnitOfWork(ABC):
    accounts: AccountRepository
    deposit_transactions: DepositTransactionRepository
    withdraw_transactions: WithdrawTransactionRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass