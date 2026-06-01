from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from uuid import UUID
from datetime import datetime


class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

@dataclass
class MoneyOperationRequest:
    amount: Decimal
    description: str | None = None

@dataclass
class Transaction:
    transaction_id: UUID
    account_id: UUID
    amount: Decimal
    balance_after: Decimal
    transaction_type: TransactionType
    description: str | None = None
    created_at: datetime | None = None
    