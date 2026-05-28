from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.app.domain.entities.user import User
from src.app.interfaces.api.dependency.account_dependencies import (
    AccountService,
    get_account_service,
)
from src.app.interfaces.api.dependency.user_dependencies import get_current_user
from src.app.interfaces.api.schemas.account.account import (
    AccountCreate,
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
    account_service: AccountService = Depends(get_account_service),
):
    return await account_service.create(
        user_id=current_user.id,
        name=payload.name,
        balance=payload.balance,
        currency=payload.currency,
    )


@private_router.delete("/{account_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_number: str,
    service: AccountService = Depends(get_account_service),
):
    deleted = await service.delete(account_number)

    if not deleted:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Numero de conta nao encontrado",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@private_router.get(
    "/{account_number}",
    response_model=AccountResponse,
    status_code=status.HTTP_200_OK,
)
async def find_by_account_number(
    account_number: str,
    account_service: AccountService = Depends(get_account_service),
):
    account = await account_service.find_by_account_number(account_number)
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
    account_service: AccountService = Depends(get_account_service),
):
    accounts = await account_service.list_accounts()
    if not accounts:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Nenhuma conta encontrada",
        )
    return accounts
