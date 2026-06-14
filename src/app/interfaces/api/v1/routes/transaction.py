from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.exceptions.account_exceptions import (
    AccountNotFoundError,
    AccountOwnershipError,
    InactiveAccountError,
    InsufficientFundsError,
    InvalidAmountError,
)
from app.interfaces.api.dependency.transaction_dependencies import (
    DepositMoneyUseCase,
    WithdrawMoneyUseCase,
    get_deposit_service,
    get_withdraw_service,
)
from app.interfaces.api.dependency.user_dependencies import get_current_user
from app.interfaces.api.schemas.account.account import (
    AccountTransactionResponseDeposit,
    AccountTransactionResponseWithdraw,
    DepositRequest,
    WithdrawRequest,
)


private_router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"],
)


def map_account_error(exc: Exception) -> HTTPException:
    if isinstance(exc, AccountNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, AccountOwnershipError):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    if isinstance(exc, InvalidAmountError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        )
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@private_router.post("/deposit", status_code=status.HTTP_200_OK)
async def deposit(
    payload: DepositRequest,
    current_user=Depends(get_current_user),
    deposit_service: DepositMoneyUseCase = Depends(get_deposit_service),
):
    try:
        transaction = await deposit_service.execute(
            user_id=current_user.id,
            account_number=payload.account_number,
            amount=payload.amount,
        )
    except (
        AccountNotFoundError,
        AccountOwnershipError,
        InvalidAmountError,
        InactiveAccountError,
    ) as exc:
        raise map_account_error(exc) from exc

    return AccountTransactionResponseDeposit.model_validate(transaction)


@private_router.post("/withdraw", status_code=status.HTTP_200_OK)
async def withdraw(
    payload: WithdrawRequest,
    current_user=Depends(get_current_user),
    withdraw_service: WithdrawMoneyUseCase = Depends(get_withdraw_service),
):
    try:
        transaction = await withdraw_service.execute(
            user_id=current_user.id,
            account_number=payload.account_number,
            amount=payload.amount,
        )
    except (
        AccountNotFoundError,
        AccountOwnershipError,
        InvalidAmountError,
        InactiveAccountError,
        InsufficientFundsError,
    ) as exc:
        raise map_account_error(exc) from exc

    return AccountTransactionResponseWithdraw.model_validate(transaction)
