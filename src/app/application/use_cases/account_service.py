import uuid
from uuid import UUID
from decimal import Decimal

from src.app.domain.entities.account import Account
from src.app.domain.unit_of_work import UnitOfWork


class AccountService:
    
    def __init__(self, uow: UnitOfWork):
        self.uow= uow
   
    
    async def create(self, user_id: UUID, name: str,  
                    currency: str, is_active:bool, balance: Decimal = Decimal("0.00")) -> Account:
        
        account = Account(
            account_number = str(uuid.uuid4()),
            account_id=generator(),
            user_id=user_id,
            name=name,
            balance=balance,
            currency=currency, 
            is_active=is_active
        )


        async with self.uow:
            return await self.uow.accounts.create(account)


    async def find_by_account_number(self,user_id: UUID, account_number: str):
        return await self.uow.accounts.find_by_account_number(user_id=user_id, account_number=account_number)

    async def list_accounts(self, user_id: UUID) -> list[Account]:
        return await self.uow.accounts.list_accounts(user_id)

    async def get_by_account_for_update(self, user_id: UUID, account_number: str):
        return await self.uow.accounts.get_by_account_for_update(user_id=user_id, account_number=account_number)
    