from decimal import Decimal
from uuid import UUID, uuid4


from src.app.domain.entities.transaction import (AccountTransaction,
                                                 TransactionType)
from src.app.domain.unit_of_work import UnitOfWork


class AccountNotFoundError(Exception):
    pass


class DepositMoneyUseCase:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(
        self,
        account_id: UUID,
        amount: Decimal,
        description: str | None = None,
    ) -> None:
        async with self.uow:
            account = await self.uow.accounts.get_by_id_for_update(account_id)

            if account is None:
                raise AccountNotFoundError("Conta não encontrada.")

            account.deposit(amount)

            transaction = AccountTransaction(
                transaction_id=uuid4(),
                account_id=account.account_id,
                amount=amount,
                transaction_type=TransactionType.DEPOSIT,
                balance_after=account.balance,
                description=description,
            )

            await self.uow.accounts.save(account)
            await self.uow.transactions.create(transaction)

            await self.uow.commit()