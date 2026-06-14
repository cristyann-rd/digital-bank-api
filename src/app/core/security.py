from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.application.ports.security import PasswordHasher, TokenManager
from app.core.config import settings


class PwdlibPasswordHasher(PasswordHasher):
    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self._password_hash.verify(password, password_hash)


class JWTTokenManager(TokenManager):
    def create_access_token(self, user_id: UUID) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=settings.token_expire_minutes)

        payload: dict[str, str | int] = {
            "sub": str(user_id),
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
            "type": "access",
        }

        return jwt.encode(
            payload,
            settings.secret_key,
            algorithm=settings.algorithm,
        )

    def decode_access_token(self, token: str) -> UUID | None:
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm],
            )
            if payload.get("type") != "access":
                raise JWTError("Tipo de token invalido")
            subject = payload.get("sub")
            if subject is None:
                return None
            return UUID(subject)
        except (JWTError, ValueError):
            return None


password_hasher = PwdlibPasswordHasher()
token_manager = JWTTokenManager()
