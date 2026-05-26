from dataclasses import dataclass
from typing import Optional

@dataclass
class Account:
    account_id: Optional[int]
    user_id: int
    name: str
    email: str
    password_hash: str
    balance: float
    currency: str