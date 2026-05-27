from abc import ABC, abstractmethod

from app.domain.entities.account import Account


class AccountRepository(ABC):

    @abstractmethod
    async def create(self, account: Account) -> Account:
        pass

    @abstractmethod
    async def find_by_account_number(self, account_number: str,) -> Account | None:
        pass

    @abstractmethod
    async def delete(self, account_number: str) -> bool:
        pass

    @abstractmethod
    async def list_accounts(self) -> list[Account]:
        pass