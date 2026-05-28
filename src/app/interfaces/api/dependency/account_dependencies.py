from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.infrastructure.database.connection import get_db
from src.app.domain.repositories.account_repository import AccountRepository, Account
from src.app.infrastructure.repositories.account_repository_sqlalchemy import AccountRepositorySQLAlchemy
from src.app.application.use_cases.account_service  import AccountService


def get_account_repository(db: AsyncSession = Depends(get_db)) -> AccountRepository:
    return AccountRepositorySQLAlchemy(db)

def get_account_service(account_repository: AccountRepository = Depends(get_account_repository)) -> AccountService:
    return AccountService(account_repository)
