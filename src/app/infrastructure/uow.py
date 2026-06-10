from src.app.domain.unit_of_work import UnitOfWork
from src.app.infrastructure.repositories.transaction_repository_sqlalchemy import (
    TransactionRepositorySQLAlchemy,
)
from src.app.infrastructure.repositories.account_repository_sqlalchemy import (
    AccountRepositorySQLAlchemy,
)


class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.session = session
        self.committed = False

        self.accounts = AccountRepositorySQLAlchemy(session)
        self.transactions = TransactionRepositorySQLAlchemy(session)

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