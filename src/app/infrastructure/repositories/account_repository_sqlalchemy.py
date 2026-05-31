
from typing import cast


from sqlalchemy import delete, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.entities.account import Account
from src.app.domain.repositories.account_repository import (
    AccountRepository,
)
from src.app.infrastructure.models.account import AccountModel


class AccountRepositorySQLAlchemy(AccountRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, db_account: AccountModel) -> Account:
        return Account(
            account_number=db_account.account_number,
            user_id=db_account.user_id,
            name=db_account.name,
            is_active=db_account.is_active,
            balance=db_account.balance,
            currency=db_account.currency,
        )

    async def create(self, account: Account) -> Account:

        new_account = AccountModel(
            user_id=account.user_id,
            account_number=account.account_number,
            balance=account.balance,
            currency=account.currency,
        )

        self.session.add(new_account)

        await self.session.commit()
        await self.session.refresh(new_account)

        return self._to_domain(new_account)

    async def find_by_account_number(
        self,
        account_number: str,
    ) -> Account | None:

        stmt = select(AccountModel).where(
            AccountModel.account_number == account_number
        )

        result = await self.session.execute(stmt)

        account = result.scalars().first()

        if account is None:
            return None

        return self._to_domain(account)

    async def delete(self, account_number: str) -> bool:

        stmt = delete(AccountModel).where(
            AccountModel.account_number == account_number
        )

        result = await self.session.execute(stmt)

        cursor_result = cast(CursorResult, result)

        await self.session.commit()

        return cursor_result.rowcount > 0

    async def list_accounts(self) -> list[Account]:

        stmt = select(AccountModel).order_by(
            AccountModel.account_number
        )

        result = await self.session.execute(stmt)

        accounts = result.scalars().all()

        return [
            self._to_domain(account)
            for account in accounts
        ]