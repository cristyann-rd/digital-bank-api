from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from uuid import UUID
from datetime import datetime


class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


@dataclass(frozen=True)
class Transaction:
    transaction_id: UUID
    account_number: str
    account_id: UUID
    amount: Decimal
    balance_after: Decimal
    transaction_type: TransactionType
    description: str | None = None
    created_at: datetime | None = None
    is_active: bool = True
    