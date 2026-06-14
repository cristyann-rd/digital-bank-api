from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from app.domain.entities.transaction import Transaction, TransactionType
from app.domain.repositories.deposit_repository import DepositTransactionRepository
from app.infrastructure.models.transaction import TransactionModel


class DepositRepositorySQLAlchemy(DepositTransactionRepository):
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

    async def list_by_transactions_deposit(self, account_number: str, transaction_type: TransactionType = TransactionType.DEPOSIT) -> list[Transaction]:
        stmt = select(TransactionModel).where(
            TransactionModel.account_number == account_number,
            TransactionModel.transaction_type == transaction_type 
        ).order_by(TransactionModel.created_at.desc())

        result = await self.session.execute(stmt)
        transactions = result.scalars().all()

        return [self._to_domain(db_transaction) for db_transaction in transactions]