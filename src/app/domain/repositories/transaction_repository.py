from abc import ABC, abstractmethod

from src.app.domain.entities.transaction import MoneyOperationRequest, TransactionType

class AccountTransactionRepository(ABC):


    @abstractmethod
    async def create():
        pass

    @abstractmethod
    async def loockup_transaction_id():
        pass

    @abstractmethod
    async def account_transacion_list():
        pass

    @abstractmethod
    async def account_transaction_pagination():
        pass

    @abstractmethod
    async def account_transaction_type():
        pass
