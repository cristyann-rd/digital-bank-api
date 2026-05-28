from dataclasses import dataclass
from typing import Optional

@dataclass
class Transaction:
    id: Optional[int]
    account_id: int
    balance: float
    description: str