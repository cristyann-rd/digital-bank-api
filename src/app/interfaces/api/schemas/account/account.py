from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from enum import Enum
from uuid import UUID
from datetime import datetime

class AccountCreate(BaseModel):
    name: str
    currency: str


class AccountUpdate(BaseModel):
    is_active: bool

class AccountResponse(BaseModel):
    account_number: str
    balance: Decimal
    currency: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class MoneyOperationRequest(BaseModel):
    amount: Decimal
    description: str | None = None

class TransactionTypeResponse(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class AccountTransactionResponseDeposit(BaseModel):
    transaction_id: UUID
    account_id: UUID
    amount: Decimal
    balance_after: Decimal
    transaction_type: TransactionTypeResponse = TransactionTypeResponse.DEPOSIT
    created_at: datetime | None = None

class AccountTransactionResponseWithdraw(BaseModel):
    transaction_id: UUID
    account_id: UUID
    amount: Decimal
    balance_after: Decimal
    transaction_type: TransactionTypeResponse = TransactionTypeResponse.WITHDRAW
    created_at: datetime | None = None
    
class DepositRequest(BaseModel):
    account_number: str
    amount: Decimal = Field(gt=0)
    

class WithdrawRequest(BaseModel):
    account_number: str
    amount: Decimal = Field(gt=0)
    