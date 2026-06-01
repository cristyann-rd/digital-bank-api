from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
from uuid import UUID
from datetime import datetime


class MoneyOperationRequest(BaseModel):
    amount: Decimal
    description: str | None = None

class TransactionTypeResponse(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class AccountTransactionResponse(BaseModel):
    transaction_id: UUID
    account_id: UUID
    amount: Decimal
    balance_after: Decimal
    transaction_type: TransactionTypeResponse
    description: str | None = None
    created_at: datetime | None = None
    