from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.user_service import UserService
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import (
    DuplicateEmailError,
    PasswordValidationError,
    UserNotFoundError,
)
from app.interfaces.api.dependency.user_dependencies import (
    get_current_user,
    get_user_service,
)
from app.interfaces.api.schemas.user.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)


public_router = APIRouter(prefix="/api/v1/users", tags=["users"])
private_router = APIRouter(prefix="/api/v1/users", tags=["users"])


@public_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
@public_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> User:
    try:
        return await user_service.create_user(
            name=user_data.name,
            email=str(user_data.email),
            password=user_data.password,
        )
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except PasswordValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc


@private_router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def read_current_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user


@private_router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> User:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado",
        )

    user = await user_service.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado",
        )
    return user


@private_router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def read_all_users(
    _: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> list[User]:
    return await user_service.get_all_users()


@private_router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> User:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado",
        )

    try:
        return await user_service.update_user(
            user_id,
            user_data.model_dump(exclude_unset=True, exclude_none=True),
        )
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except PasswordValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
