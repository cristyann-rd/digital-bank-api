import re

from app.domain.exceptions.user_exceptions import PasswordValidationError
from app.domain.policy.password_policy import PASSWORD_POLICY


class PasswordValidator:
    def __init__(self, policy=PASSWORD_POLICY):
        self.policy = policy

    def validate(self, password: str) -> None:
        if len(password) < self.policy["min_length"]:
            raise PasswordValidationError(
                f"Senha deve conter no minimo {self.policy['min_length']} caracteres."
            )
        if len(password) > self.policy["max_length"]:
            raise PasswordValidationError(
                f"Senha deve conter no maximo {self.policy['max_length']} caracteres."
            )
        if self.policy["require_uppercase"] and not re.search(r"[A-Z]", password):
            raise PasswordValidationError("Senha deve conter uma letra maiuscula.")
        if self.policy["require_lowercase"] and not re.search(r"[a-z]", password):
            raise PasswordValidationError("Senha deve conter uma letra minuscula.")
        if self.policy["require_number"] and not re.search(r"[0-9]", password):
            raise PasswordValidationError("Senha deve conter um numero.")
        if self.policy["require_symbol"] and not re.search(r"[^A-Za-z0-9]", password):
            raise PasswordValidationError("Senha deve conter um simbolo.")
