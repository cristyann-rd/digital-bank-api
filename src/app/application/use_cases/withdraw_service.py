from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.entities.transaction import Transaction, TransactionType
from app.domain.exceptions.account_exceptions import (
    AccountNotFoundError,
    AccountOwnershipError,
)
from app.domain.unit_of_work import UnitOfWork


class WithdrawMoneyUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(
        self,
        user_id: UUID,
        account_number: str,
        amount: Decimal,
        description: str | None = None,
    ) -> Transaction:
        async with self.uow:
            account = await self.uow.accounts.get_by_account_for_update(
                user_id=user_id,
                account_number=account_number,
            )
            if account is None:
                raise AccountNotFoundError("Conta nao encontrada.")
            if account.user_id != user_id:
                raise AccountOwnershipError(
                    "A conta nao pertence ao usuario informado."
                )

            account.withdraw(amount)
            transaction = Transaction(
                transaction_id=uuid4(),
                account_number=account.account_number,
                account_id=account.account_id,
                amount=amount,
                transaction_type=TransactionType.WITHDRAW,
                balance_after=account.balance,
                description=description,
            )

            await self.uow.accounts.save(account)
            await self.uow.withdraw_transactions.create(transaction)
            await self.uow.commit()
            return transaction
