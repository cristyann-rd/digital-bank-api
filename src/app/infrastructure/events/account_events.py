from sqlalchemy import event
from src.app.infrastructure.models.account import (AccountModel)

from src.app.application.services.account_digit import (calculate_account_digit)


@event.listens_for(AccountModel, "before_insert")
def generate_digit(
    _mapper,
    _connection,
    target
):

    if target.account_number:

        target.account_digit = (
            calculate_account_digit(
                target.account_number
            )
        )