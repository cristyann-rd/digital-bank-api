from app.domain.repositories.account_repository import AccountRepository
from app.core.security import hash_password


class AccountService():
    
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository
   
    @staticmethod
    def calculate_account_digit(
        account_number: int
    ) -> str:

        total = sum(
            int(digit)
            for digit in str(account_number)
        )

        return str(total % 10)