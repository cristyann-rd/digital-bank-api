from uuid import UUID
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Account:
    account_number: str
    user_id: UUID
    name: str
    balance: Decimal
    currency: str