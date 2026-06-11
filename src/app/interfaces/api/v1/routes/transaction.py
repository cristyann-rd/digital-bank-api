from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException


from src.app.interfaces.api.schemas.account.account import(
    DepositRequest,
    WithdrawRequest,
    AccountTransactionResponseDeposit, 
    AccountTransactionResponseWithdraw
                                                           ) 

from src.app.interfaces.api.dependency.transaction_dependencies import (
    DepositMoneyUseCase,
    WithdrawMoneyUseCase,
    get_deposit_service,
    get_withdraw_service,
)

from src.app.interfaces.api.dependency.user_dependencies import get_current_user
 

private_router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"],
)

@private_router.post(
    "/deposit",
    status_code=200,
)

async def deposit(
    payload: DepositRequest,
    current_user = Depends(get_current_user),
    deposit_service: DepositMoneyUseCase = Depends(get_deposit_service),
):
    transaction_deposit = await deposit_service.execute(
        user_id=current_user.id,
        account_number=payload.account_number,
        amount=payload.amount,
    )
    if not transaction_deposit:
        raise HTTPException(status_code=400, detail="Erro ao realizar depósito")
    
    return AccountTransactionResponseDeposit.model_validate(transaction_deposit)

@private_router.post(
    "/withdraw",
    status_code=200,
)

async def withdraw(   
    payload: WithdrawRequest,
    current_user = Depends(get_current_user),
    withdraw_service : WithdrawMoneyUseCase = Depends(get_withdraw_service),
):

    transaction_withdraw = await withdraw_service.execute(
        user_id=current_user.id,
        account_number=payload.account_number,
        amount=payload.amount,
    )
    if not transaction_withdraw:
        raise HTTPException(status_code=400, detail="Erro ao realizar saque")
    
    return AccountTransactionResponseWithdraw.model_validate(transaction_withdraw)