from pydantic import BaseModel
from decimal import Decimal
from enum import Enum


class MoneyOperationRequest(BaseModel):
    amount: Decimal
    description: str | None = None

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"