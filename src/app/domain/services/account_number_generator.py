from abc import ABC, abstractmethod

class AccountNumberGenerator(ABC):

    @abstractmethod
    def next(self) -> str:
        pass