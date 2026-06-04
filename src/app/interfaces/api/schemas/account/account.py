from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from enum import Enum
from uuid import UUID
from datetime import datetime

class AccountCreate(BaseModel):
    name: str
    currency: str


class AccountUpdate(BaseModel):
    is_active: bool

class AccountResponse(BaseModel):
    account_number: str
    balance: float
    currency: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

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
    