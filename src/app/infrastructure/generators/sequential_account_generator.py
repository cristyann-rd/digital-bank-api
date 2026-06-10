from src.app.domain.services.account_number_generator import AccountNumberGenerator


class SequentialAccountGenerator(AccountNumberGenerator):
    def __init__(self, start: int = 1):
        self.current = start

    def next(self) -> str:
        account_number = f"{self.current:010d}"
        self.current += 1
        return account_number