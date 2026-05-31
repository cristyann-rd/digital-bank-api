from abc import ABC, abstractmethod
from uuid import UUID

from src.app.domain.entities.transaction import AccountTransaction

class AccountTransactionRepository(ABC):


    @abstractmethod
    async def create(self,transaction:AccountTransaction,) -> AccountTransaction:
        pass

    @abstractmethod
    async def get_by_id(self, transaction_id: UUID,) -> AccountTransaction | None:
        pass

    @abstractmethod
    async def list_by_account_id(self, account_id: UUID,) -> list[AccountTransaction]:
        pass

    @abstractmethod
    async def list_by_account_id_paginated(self, account_id: UUID, 
                                           limit: int, offset: int,) -> list[AccountTransaction]:
        pass

    @abstractmethod
    async def  list_by_account_id_paginated_type(self,account_id:UUID, transaction_type: AccountTransaction, limit: int, offset: int,) -> AccountTransaction:
        pass
