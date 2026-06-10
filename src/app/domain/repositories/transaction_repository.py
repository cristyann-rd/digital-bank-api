from abc import ABC, abstractmethod
from uuid import UUID

from src.app.domain.entities.transaction import Transaction


class AccountTransactionRepository(ABC):

    @abstractmethod
    async def get_by_id(self, transaction_id: UUID) -> Transaction | None:
        pass

    @abstractmethod
    async def list_by_account_id(
        self,
        account_id: UUID,
    ) -> list[Transaction]:
        pass

    @abstractmethod
    async def create(self, transaction: Transaction) -> None:
        pass