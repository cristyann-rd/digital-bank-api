from abc import ABC, abstractmethod
from uuid import UUID

from src.app.domain.entities.account import Account


class AccountRepository(ABC):

    @abstractmethod
    async def create(self, account: Account) -> Account:
        pass

    @abstractmethod
    async def find_by_account_number(
        self,
        user_id: UUID,
        account_number: str,
    ) -> Account | None:
        pass

    @abstractmethod
    async def get_by_account_for_update(
        self,
        user_id: UUID,
        account_number: str,
    ) -> Account | None:
        pass

    @abstractmethod
    async def save(self, account: Account) -> None:
        pass

    @abstractmethod
    async def delete(self, user_id: UUID, account_number: str) -> bool:
        pass

    @abstractmethod
    async def list_accounts(self, user_id: UUID) -> list[Account]:
        pass

    @abstractmethod
    async def update_account_status(self, user_id: UUID, account_number: str, is_active: bool) -> Account | None:
        pass