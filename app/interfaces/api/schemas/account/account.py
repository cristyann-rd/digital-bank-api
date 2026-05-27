from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    account_number: str
    user_id: int
    name: str
    balance: float
    currency: str

class AccountResponse(BaseModel):
    account_number: str
    balance: float
    currency: str
    model_config = ConfigDict(from_attributes=True)
