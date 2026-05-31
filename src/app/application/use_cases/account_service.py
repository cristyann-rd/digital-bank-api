import uuid
from uuid import UUID
from decimal import Decimal

from src.app.domain.repositories.account_repository import AccountRepository, Account



class AccountService:
    
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository
   
    
    async def create(self, user_id: UUID, name: str,  
                             balance: Decimal, currency: str, is_active:bool):
        account = Account(
            account_number = str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            balance=balance,
            currency=currency, 
            is_active=is_active
        )
        return await self.account_repository.create(account)
    
    async def delete(self,user_id: UUID,account_number: str ):
        return await self.account_repository.delete(account_number)
    
    async def find_by_account_number(self, user_id: UUID, account_number: str) -> Account | None:
        return await self.account_repository.find_by_account_number(account_number)
    
    async def list_accounts(self):
        return await self.account_repository.list_accounts()

    