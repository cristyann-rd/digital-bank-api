from uuid import UUID
from dataclasses import dataclass
from decimal import Decimal

from src.app.domain.exceptions.account_exceptions import (InactiveAccountError, 
                                                          InvalidAmountError, 
                                                          InsufficientFundsError)

@dataclass
class Account:
    account_number: str
    user_id: UUID
    name: str
    balance: Decimal
    currency: str
    is_active: bool

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