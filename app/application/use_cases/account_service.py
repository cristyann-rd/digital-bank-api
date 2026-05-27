import uuid

from app.domain.repositories.account_repository import AccountRepository, Account



class AccountService:
    
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository
   
    
    async def create(self, user_id: int, name: str, 
                             email: str,  
                             balance: float, currency: str):
        account = Account(
            account_number = str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            email=email,
            balance=balance,
            currency=currency
        )
        return await self.account_repository.create(account)
    
    async def delete(self,account_number: str ):
        return await self.account_repository.delete(account_number)
    
    async def find_by_account_number(self, account_number: str) -> Account | None:
        return await self.account_repository.find_by_account_number(account_number)
    
    async def list_accounts(self):
        return await self.account_repository.list_accounts()

    