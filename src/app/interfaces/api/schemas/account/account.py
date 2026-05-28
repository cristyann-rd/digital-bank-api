from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    name: str
    balance: float
    currency: str

class AccountResponse(BaseModel):
    account_number: str
    balance: float
    currency: str
    model_config = ConfigDict(from_attributes=True)
