from abc import ABC, abstractmethod
from uuid import UUID

from src.app.domain.entities.transaction import Transaction,TransactionType


class DepositTransactionRepository(ABC):

    @abstractmethod
    async def list_by_transactions_deposit(
        self,
        account_number: str,
        transaction_type: TransactionType = TransactionType.DEPOSIT
    ) -> list[Transaction]:
        pass

    @abstractmethod
    async def create(self, transaction: Transaction) -> None:
        pass
