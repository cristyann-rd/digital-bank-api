from fastapi import FastAPI

from app.interfaces.api.v1.routes.account import (
    private_router as account_router_private,
)
from app.interfaces.api.v1.routes.auth import router as auth_router
from app.interfaces.api.v1.routes.transaction import (
    private_router as transaction_router_private,
)
from app.interfaces.api.v1.routes.user import (
    private_router as user_router_private,
)
from app.interfaces.api.v1.routes.user import public_router as user_router_public


def create_app() -> FastAPI:
    application = FastAPI(
        title="Bank DIO",
        version="1.0.0",
        description=(
            "API para gerenciamento de usuarios, autenticacao "
            "e movimentacoes bancarias."
        ),
    )

    @application.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    application.include_router(auth_router)
    application.include_router(user_router_public)
    application.include_router(user_router_private)
    application.include_router(account_router_private)
    application.include_router(transaction_router_private)

    return application


app = create_app()
