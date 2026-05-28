import re
from src.app.domain.policy.password_policy import PASSWORD_POLICY

class PasswordValidator:
    
    def __init__(self, policy=PASSWORD_POLICY):
        self.policy = policy

    def validate(self, password: str):
        if len(password) < self.policy["min_length"]:
            raise ValueError(f"Senha deve conter no mínimo {self.policy['min_length']} caracteres.")
        if len(password) > self.policy["max_length"]:
            raise ValueError(f"Senha deve conter no máximo {self.policy['max_length']} caracteres.")
        if self.policy['require_uppercase'] and not re.search(r'[A-Z]', password):
            raise ValueError("Senha deve conter pelo Menos Uma Letra Maiúscula.")
        if self.policy['require_lowercase'] and not re.search(r'[a-z]', password):
            raise ValueError("Senha deve conter pleo Menos Uma Letra Miniscula.")
        if self.policy['require_number'] and not re.search(r'[0-9]', password):
            raise ValueError("Senha deve conter pelo Menos um Número.")