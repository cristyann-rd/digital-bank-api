from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    
    algorithm: str = "HS256"
    secret_key: str
    token_expire_minutes: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def sync_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()  # type: ignore[call-arg]

"""
@dataclass(frozen=True, slots=True)
class JwtConfig:
    issuer: str
    audience: str
    private_key: str
    public_key: str
    key_id: str
    algorithm: Literal["RS256"]
    access_token_ttl_minutes: int
    leeway_seconds: int = 30

"""