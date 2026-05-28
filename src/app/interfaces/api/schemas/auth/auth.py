from pydantic import BaseModel
from typing import Literal

class AccessTokenClaims(BaseModel):
    iss: str
    sub: str
    aud: str
    iat: int
    nbf: int
    exp: int
    jti: str
    typ: Literal["access"]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"