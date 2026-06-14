from typing import Literal

from pydantic import BaseModel


class AccessTokenClaims(BaseModel):
    sub: str
    iat: int
    exp: int
    type: Literal["access"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
