from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.interfaces.api.v1.routes.auth import router as auth_router
from app.interfaces.api.v1.routes.user import public_router as user_router_public
from app.interfaces.api.v1.routes.user import private_router as user_router_private

def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Iniciando a aplicação...")
        yield
        print("Finalizando a aplicação...")

    app = FastAPI(title="Bank DIO", 
                  version="1.0", 
                  description="API para gerenciamento de usuários, autenticação e movimentações bancárias.", 
                  lifespan=lifespan)
    
    app.include_router(auth_router)
    app.include_router(user_router_public)
    app.include_router(user_router_private)
    return app