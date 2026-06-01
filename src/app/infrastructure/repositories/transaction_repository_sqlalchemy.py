from uuid import UUID


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.domain.entities.transaction import Transaction
from src.app.domain.repositories.transaction_repository import (
    AccountTransactionRepository,
)
from src.app.infrastructure.models.transaction import TransactionModel


class TransactionRepositorySQLAlchemy(AccountTransactionRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_model(self, transaction: Transaction) -> TransactionModel:
        return TransactionModel(
            transaction_id=transaction.transaction_id,
            account_id=transaction.account_id,
            amount=transaction.amount,
            balance_after=transaction.balance_after,
            transaction_type=transaction.transaction_type,
            created_at=transaction.created_at,
        )

    def _to_domain(self, db_transaction: TransactionModel) -> Transaction:
        return Transaction(
            transaction_id=db_transaction.transaction_id,
            account_id=db_transaction.account_id,
            amount=db_transaction.amount,
            balance_after=db_transaction.balance_after,
            transaction_type=db_transaction.transaction_type,
            created_at=db_transaction.created_at,
        )

    async def get_by_id(self, transaction_id: UUID) -> Transaction | None:
        
        
        stmt = select(TransactionModel).where(TransactionModel.transaction_id == transaction_id)

    
        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()

        if row is None:
           return None
        
        return self._to_domain(row)

    async def get_by_id_for_update(self, transaction_id: UUID) -> Transaction | None:
        stmt = (
            select(TransactionModel)
            .where(TransactionModel.transaction_id == transaction_id)
            .with_for_update()
        )

        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()

        if row is None:
            return None

        return self._to_domain(row)
    
    async def save(self, transaction: Transaction) -> None:
        model = self._to_model(transaction)

        await self.session.merge(model)


    async def list_by_account_id(self, account_id: UUID) -> list[Transaction]:

        stmt = select(TransactionModel).where(
           TransactionModel.account_id == account_id
        ).order_by(TransactionModel.transaction_id)

        result = await self.session.execute(stmt)

        transactions = result.scalars().all()

        return [
            self._to_domain(transaction)
            for transaction in transactions
        ]

