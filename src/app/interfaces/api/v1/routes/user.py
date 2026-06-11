from uuid import UUID
from fastapi import HTTPException, APIRouter, status, Depends

from src.app.interfaces.api.schemas.user.user import UserResponse, UserCreate
from src.app.interfaces.api.dependency.user_dependencies import get_user_service, get_current_user, UserService

public_router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

private_router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)

@public_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    if await user_service.email_exists(user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Email já existe no sistema")
    user = await user_service.create_user(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )
    return {
        "id": user.id,
        "email": user.email,
    }

@private_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, _: UserResponse = Depends(get_current_user),
                   user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@private_router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def read_all_users(_: UserResponse = Depends(get_current_user),
                         user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users()
    return users

@private_router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: UUID, user_data: UserCreate, _: UserResponse = Depends(get_current_user),
                      user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    updated_user = await user_service.update_user(user_id, user_data.model_dump(exclude_unset=True))
    return updated_user