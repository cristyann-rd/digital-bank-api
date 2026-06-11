from src.app.domain.unit_of_work import UnitOfWork
from src.app.infrastructure.repositories.deposit_repository_sqlalchemy import (
    DepositRepositorySQLAlchemy,
)
from src.app.infrastructure.repositories.withdraw_repository_sqlalchemy import (
    WithdrawRepositorySQLAlchemy,
)
from src.app.infrastructure.repositories.account_repository_sqlalchemy import (
    AccountRepositorySQLAlchemy,
)


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.session = session
        self.committed = False

        self.accounts = AccountRepositorySQLAlchemy(session)
        self.deposit_transactions = DepositRepositorySQLAlchemy(session)
        self.withdraw_transactions = WithdrawRepositorySQLAlchemy(session)

    async def __aenter__(self):
        self.committed = False
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.rollback()
            return

        if not self.committed:
            await self.rollback()

    async def commit(self):
        await self.session.commit()
        self.committed = True

    async def rollback(self):
        await self.session.rollback()