import uuid
from uuid import UUID
from decimal import Decimal

from src.app.domain.repositories.transaction_repository import AccountTransactionRepository, AccountTransaction
from src.app.domain.repositories.account_repository import AccountRepository, Account

class DepositService:

    def __init__(self, deposit_repository: AccountTransactionRepository,
                       account_repository: AccountRepository):
        
        self.deposit_repository = deposit_repository
        self.account_repository = account_repository


    async def deposit(self, user_id, data):
        account = await self.account_repository.find_by_account_number(user_id)
