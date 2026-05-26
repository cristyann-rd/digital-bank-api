from abc import ABC, abstractmethod
from app.domain.entities.account import Account

class AccountRepository(ABC):
    
    @abstractmethod
    async def create(self, account) -> Account:
        pass

    @abstractmethod
    async def get_by_id(self, account_id) -> Account | None:
        pass

    @abstractmethod
    async def get_account_by_user_id(self, user_id: int) -> list[Account]:
        pass

    @abstractmethod
    async def account_number(self, account_number: int) -> str:
        pass