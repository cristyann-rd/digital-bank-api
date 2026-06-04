from uuid import UUID


from src.app.domain.entities.account import Account
from src.app.domain.unit_of_work import UnitOfWork
from src.app.domain.services.account_number_generator import AccountNumberGenerator



class AccountUseCase:
    
    def __init__(self, uow: UnitOfWork, account_number_generator: AccountNumberGenerator):
        self.uow = uow
        self.account_number_generator = account_number_generator
   
    
    async def create(self, user_id: UUID, name: str,  
                    currency: str) -> Account:
        
        account_number = self.account_number_generator.next()

        account = Account.open(
        user_id=user_id,
        name=name,
        currency=currency,
        account_number=account_number
        )
   
        

        async with self.uow:
            created_account = await self.uow.accounts.create(account)
            await self.uow.commit()
            return created_account


    async def find_by_account_number(self,user_id: UUID, account_number: str):
        return await self.uow.accounts.find_by_account_number(user_id=user_id, account_number=account_number)

    async def list_accounts(self, user_id: UUID) -> list[Account]:
        return await self.uow.accounts.list_accounts(user_id)

    async def get_by_account_for_update(self, user_id: UUID, account_number: str):
        return await self.uow.accounts.get_by_account_for_update(user_id=user_id, account_number=account_number)
    