from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class AccountCreate(BaseModel):
    name: str
    balance: Decimal
    currency: str
    is_active: bool

class AccountResponse(BaseModel):
    account_number: str
    balance: float
    currency: str
    model_config = ConfigDict(from_attributes=True)
