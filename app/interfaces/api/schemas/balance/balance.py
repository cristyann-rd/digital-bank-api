from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class AccountCreate(BaseModel):
    account_id: int
    email: EmailStr
    password: str 

class AccountResponse(BaseModel):
    id: int
    account_id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class BalanceRequest(BaseModel):
    account_id: int
    balance: Optional [float] = None

class BalanceResponse(BaseModel):
    balance: float
    account_id: int
    model_config = ConfigDict(from_attributes=True)
