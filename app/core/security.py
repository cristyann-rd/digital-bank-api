from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt, JWTError
from app.core.config import settings
from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)

def create_access_token(user_id: int) -> str:

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.token_expire_minutes)
    
    payload: dict[str, str | int] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access"
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        if payload.get("type") != "access":
            raise JWTError("Tipo de token inválido")
        return payload
    except JWTError as e:
        raise ValueError(f"Erro no decode do token: {str(e)}")