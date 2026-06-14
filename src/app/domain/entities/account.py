import uuid
from uuid import UUID

from dataclasses import dataclass
from decimal import Decimal


from app.domain.exceptions.account_exceptions import (
    InactiveAccountError,
    InsufficientFundsError,
    InvalidAmountError,
)

MONEY_QUANTUM = Decimal("0.01")
@dataclass
class Account:
    account_number: str
    user_id: UUID
    account_id: UUID
    name: str
    balance: Decimal
    currency: str
    is_active: bool = True


    @classmethod
    def open(
            cls,
            user_id: UUID,
            name: str,
            currency: str,
            account_number: str
        ) -> "Account":
            return cls(
                account_number=account_number,
                account_id=uuid.uuid4(),
                user_id=user_id,
                name=name,
                balance=Decimal("0.00"),
                currency=currency,
                is_active=True,
            )


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
    
        amount = self._validate_amount(amount)    
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if not self.is_active:
            raise InactiveAccountError("Conta inativa.")

        amount = self._validate_amount(amount)

        if self.balance < amount:
            raise InsufficientFundsError("Saldo insuficiente.")

        self.balance -= amount
