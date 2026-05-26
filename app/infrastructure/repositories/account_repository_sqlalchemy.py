from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.account import AccountModel
from app.domain.entities.account import Account
from app.domain.repositories.account_repository import AccountRepository

class AccountRepositorySQLAlchemy(AccountRepository):
    

    def _to_domain(self, db_user: AccountModel) -> Account:
        return Account(
               account_id=db_user.account_id,
                user_id=db_user.user_id,
                name=db_user.name,
                email=db_user.email,
                password_hash=db_user.password_hash,
                balance=db_user.balance,
                currency=db_user.currency
        )

    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, account: Account) -> Account:
        async with AsyncSession() as session:
            new_account = AccountModel(
                user_id=account.user_id,
                account_id=account.account_id,
                balance=account.balance,
                currency=account.currency,
            )
            self.session.add(new_account)
            await session.commit()
            await session.refresh(new_account)
            return new_account   


    async def get_by_id(self, account_id: int) -> AccountModel | None:
        async with AsyncSession() as session:
            result = await session.execute(select(AccountModel).where(AccountModel.account_id == account_id))
            account = result.scalars().first()
            return account

    async def get_account_by_user_id(self, user_id: int) -> list[Account]:
        async with AsyncSession() as session:
            result = await session.execute(select(AccountModel).where(AccountModel.user_id == user_id))
            accounts = result.scalars().all()
            return [self._to_domain(account) for account in accounts]