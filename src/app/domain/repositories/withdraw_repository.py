from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.transaction import Transaction,TransactionType


class WithdrawTransactionRepository(ABC):


    @abstractmethod
    async def create(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    async def list_by_transactions_withdraw(
        self,
        account_number: str,
        transaction_type: TransactionType = TransactionType.WITHDRAW
    ) -> list[Transaction]:
        pass