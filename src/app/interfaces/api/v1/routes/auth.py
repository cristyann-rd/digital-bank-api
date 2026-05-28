from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.application.use_cases.auth_service import AuthService
from src.app.interfaces.api.dependency.user_dependencies import get_auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.login(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Usuário não encontrado",
        )

    token = auth_service.create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}