from src.app.domain.unit_of_work import UnitOfWork
from src.app.infrastructure.repositories.transaction_repository_sqlalchemy import TransactionRepositorySQLAlchemy
from src.app.infrastructure.repositories.account_repository_sqlalchemy import AccountRepositorySQLAlchemy


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session):
        self.session = session

        
        self.accounts = AccountRepositorySQLAlchemy(session)
        self.transactions = TransactionRepositorySQLAlchemy(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()