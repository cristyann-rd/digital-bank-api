from uuid import UUID
from dataclasses import dataclass

@dataclass
class Account:
    account_number: str
    user_id: UUID
    name: str
    balance: float
    currency: str