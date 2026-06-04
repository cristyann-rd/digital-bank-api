from typing import cast
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.entities.account import Account
from src.app.domain.repositories.account_repository import AccountRepository
from src.app.infrastructure.models.account import AccountModel


class AccountRepositorySQLAlchemy(AccountRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, db_account: AccountModel) -> Account:
        return Account(
            account_number=db_account.account_number,
            account_id=db_account.account_id,
            user_id=db_account.user_id,
            name=db_account.name,
            is_active=db_account.is_active,
            balance=db_account.balance,
            currency=db_account.currency,
        )

    async def create(self, account: Account) -> Account:
        new_account = AccountModel(
            account_id=account.account_id,
            user_id=account.user_id,
            account_number=account.account_number,
            name=account.name,
            balance=account.balance,
            currency=account.currency,
            is_active=account.is_active,
        )

        self.session.add(new_account)

        await self.session.flush()
        await self.session.refresh(new_account)

        return self._to_domain(new_account)

    async def find_by_account_number(
        self,
        user_id: UUID,
        account_number: str,
    ) -> Account | None:
        stmt = select(AccountModel).where(
            AccountModel.account_number == account_number,
            AccountModel.user_id == user_id
        )

        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()

        if account is None:
            return None

        return self._to_domain(account)

    async def get_by_account_for_update(
        self,
        user_id: UUID,
        account_number: str,
    ) -> Account | None:
        stmt = (
            select(AccountModel)
            .where(
                AccountModel.account_number == account_number,
                AccountModel.user_id == user_id
            )
            .with_for_update()
        )

        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()

        if account is None:
            return None

        return self._to_domain(account)

    async def save(self, account: Account) -> None:
        stmt = select(AccountModel).where(
            AccountModel.account_id == account.account_id
        )

        result = await self.session.execute(stmt)
        db_account = result.scalar_one_or_none()

        if db_account is None:
            raise ValueError("Conta não encontrada para atualização.")

        db_account.name = account.name
        db_account.balance = account.balance
        db_account.currency = account.currency
        db_account.is_active = account.is_active

        await self.session.flush()

    async def delete(self, user_id: UUID, account_number: str) -> bool:
        stmt = delete(AccountModel).where(
            AccountModel.account_number == account_number,
            AccountModel.user_id == user_id
        )

        result = await self.session.execute(stmt)
        cursor_result = cast(CursorResult, result)

        await self.session.flush()

        return cursor_result.rowcount > 0

    async def list_accounts(self, user_id: UUID) -> list[Account]:
        stmt = select(AccountModel).where(
            AccountModel.user_id == user_id
        ).order_by(
            AccountModel.account_number
        )

        result = await self.session.execute(stmt)
        accounts = result.scalars().all()

        return [self._to_domain(account) for account in accounts]

    async def update_account_status(self, user_id: UUID, account_number: str, is_active: bool) -> Account | None:
        stmt = select(AccountModel).where(
            AccountModel.account_number == account_number,
            AccountModel.user_id == user_id
        ).with_for_update()

        result = await self.session.execute(stmt)
        db_account = result.scalar_one_or_none()

        if db_account is None:
            return None

        db_account.is_active = is_active

        await self.session.flush()

        return self._to_domain(db_account)