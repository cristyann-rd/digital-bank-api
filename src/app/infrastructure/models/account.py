import uuid

from sqlalchemy import Integer,Boolean, String, DateTime, Numeric, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from src.app.infrastructure.database.base import Base
from decimal import Decimal


class AccountModel(Base):
    __tablename__ = "accounts"
    
    account_id : Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        autoincrement=True
        )
    
    user_id : Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
        )
    
    account_number : Mapped[str] = mapped_column(
        String(36), unique=True, 
        index=True, nullable=False,
        default=lambda: str(uuid.uuid4())
        )
    
    name : Mapped[str] = mapped_column(
        String, 
        nullable=False
        )
    
    account_digit : Mapped[str | None] = mapped_column(
        String(1), 
        nullable=True
        )
    
    balance: Mapped[Decimal]= mapped_column(
        Numeric, 
        nullable=False
        )
    
    currency: Mapped[str] = mapped_column(
        String(3), 
        nullable=False
        )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True
        )
    
    created_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
        )
    
    updated_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
        )
