from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from uuid import UUID
from datetime import datetime

from app.domain.exceptions.transaction_exceptions import (InactiveAccountError, 
                                                          InvalidAmountError, 
                                                          InsufficientFundsError)

MONEY_QUANTUM = Decimal("0.01")

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

@dataclass
class MoneyOperationRequest:
    amount: Decimal
    description: str | None = None

@dataclass
class Transaction:
    transaction_id: UUID
    account_number: str
    account_id: UUID
    amount: Decimal
    balance_after: Decimal
    transaction_type: TransactionType
    description: str | None = None
    created_at: datetime | None = None
    is_active: bool = True
    


    def _ensure_active(self) -> None:
        if not self.is_active:
            raise InactiveAccountError("Conta Inativa.")
        
    def _validate_amount(self, amount: Decimal) -> Decimal:
        if not isinstance(amount, Decimal):
            raise InvalidAmountError("O valor precisa ser Decimal.")
        
        if not amount.is_finite():
            raise InvalidAmountError("O valor precisa ser finito.")
        
        if amount <= Decimal("0.00"):
            raise InvalidAmountError("O valor deve ser maior que zero.")
        
        if amount != amount.quantize(MONEY_QUANTUM):
            raise InvalidAmountError("O valor deve ter no máximo duas casas decimais")

        return amount
    
    def deposit(self, amount: Decimal) -> None:
        if not self.is_active:
            raise InactiveAccountError("Conta inativa.")

        if amount <= Decimal("0"):
            raise InvalidAmountError("O valor do depósito deve ser maior que zero.")

        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if not self.is_active:
            raise InactiveAccountError("Conta inativa.")

        if amount <= Decimal("0"):
            raise InvalidAmountError("O valor da retirada deve ser maior que zero.")

        if self.balance < amount:
            raise InsufficientFundsError("Saldo insuficiente.")

        self.balance -= amount