from dataclasses import dataclass

@dataclass
class Account:
    account_number: str
    user_id: int
    name: str
    email: str
    balance: float
    currency: str