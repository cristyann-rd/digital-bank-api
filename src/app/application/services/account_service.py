import uuid
from uuid import UUID
from decimal import Decimal

from src.app.domain.repositories.account_repository import Account
from src.app.domain.unit_of_work import UnitOfWork


class AccountService:
    
    def __init__(self, uow: UnitOfWork):
        self.uow= uow
   
    
    async def create(self, user_id: UUID, name: str,  
                    currency: str, is_active:bool, balance: Decimal = Decimal("0.0")) -> Account:
        
        account = Account(
            account_number = str(uuid.uuid4()),
            account_id=uuid.uuid4(),
            user_id=user_id,
            name=name,
            balance=balance,
            currency=currency, 
            is_active=is_active
        )


        async with self.uow:
            return await self.uow.accounts.create(account)

    
    async def delete(self,user_id: UUID,account_number: str ):

       async with self.uow:
        return await self.uow.accounts.delete(account_number)
    
    async def find_by_account_number(self,user_id, account_number: str):
        return await self.uow.accounts.find_by_account_number(account_number)

    async def list_accounts(self):
        return await self.uow.accounts.list_accounts()
    