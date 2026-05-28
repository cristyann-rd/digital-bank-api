import uuid

from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from src.app.infrastructure.database.base import Base


class UserModel(Base):
    __tablename__ = "users"
    
    id : Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash : Mapped[str] = mapped_column(String, nullable=False)
    
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
