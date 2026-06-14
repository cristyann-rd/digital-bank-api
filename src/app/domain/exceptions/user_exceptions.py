class DuplicateEmailError(Exception):
    pass


class PasswordValidationError(ValueError):
    pass


class UserNotFoundError(Exception):
    pass
