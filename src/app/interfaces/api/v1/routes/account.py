from fastapi import APIRouter, Depends, HTTPException, status

from src.app.domain.entities.user import User
from src.app.interfaces.api.dependency.account_dependencies import (
    AccountUseCase,
    get_account_use_case,
)
from src.app.interfaces.api.dependency.user_dependencies import get_current_user
from src.app.interfaces.api.schemas.account.account import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
)

private_router = APIRouter(
    prefix="/api/v1/account",
    tags=["Account"],
    dependencies=[Depends(get_current_user)],
)


@private_router.post(
    "/accounts",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    payload: AccountCreate,
    current_user: User = Depends(get_current_user),
    account_service: AccountUseCase = Depends(get_account_use_case),
):
    return await account_service.create(
        user_id=current_user.id,
        name=payload.name,
        currency=payload.currency,
        
    )



@private_router.get(
    "/{account_number}",
    response_model=AccountResponse,
    status_code=status.HTTP_200_OK,
)
async def find_by_account_number(
    account_number: str,
     current_user: User = Depends(get_current_user),
    account_service: AccountUseCase = Depends(get_account_use_case),
):

    account = await account_service.find_by_account_number(current_user.id, account_number)
    if account is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Numero de conta nao encontrado",
        )
    return account


@private_router.get(
    "/",
    response_model=list[AccountResponse],
    status_code=status.HTTP_200_OK,
)
async def list_accounts(
    account_service: AccountUseCase = Depends(get_account_use_case),
    current_user: User = Depends(get_current_user)
):
    accounts = await account_service.list_accounts(current_user.id)
    if not accounts:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Nenhuma conta encontrada",
        )
    return accounts

@private_router.patch(
    "/{account_number}", 
    response_model=AccountResponse,
    status_code=status.HTTP_200_OK,)
async def update_account(
    account_number: str,
    payload: AccountUpdate,
    current_user: User = Depends(get_current_user),
    account_service: AccountUseCase = Depends(get_account_use_case),
):
    account = await account_service.find_by_account_number(current_user.id, account_number)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Numero de conta nao encontrado",
        )
    if payload.is_active is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'is_active' é obrigatório para atualizar o status da conta.",
        )
    
    account = await account_service.update_account_status(
    user_id=current_user.id,
    account_number=account_number,
    is_active=payload.is_active
)

    return account