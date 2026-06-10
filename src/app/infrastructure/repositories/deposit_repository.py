from typing import cast
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.entities.transaction import Transaction, TransactionType
from src.app.domain.repositories.transaction_repository import AccountTransactionRepository
from src.app.infrastructure.models.transaction import TransactionModel


class DepositRepositorySQLAlchemy(AccountTransactionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, db_transaction: TransactionModel) -> Transaction:
        return Transaction(
            transaction_id=db_transaction.transaction_id,
            account_number=db_transaction.account_number,
            account_id=db_transaction.account_id,
            amount=db_transaction.amount,
            balance_after=db_transaction.balance_after,
            transaction_type=db_transaction.transaction_type,
            description=db_transaction.description,
            created_at=db_transaction.created_at,
            is_active=db_transaction.is_active,
        )
    async def create(self, transaction: Transaction) -> None:
        new_transaction = TransactionModel(
            transaction_id=transaction.transaction_id,
            account_id=transaction.account_id,
            account_number=transaction.account_number,
            amount=transaction.amount,
            balance_after=transaction.balance_after,
            transaction_type=TransactionType.DEPOSIT,
            description=transaction.description,
            is_active=transaction.is_active,
        )

        self.session.add(new_transaction)
        await self.session.flush()