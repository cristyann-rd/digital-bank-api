from sqlalchemy import Integer,Boolean, String, DateTime, Float, func
from sqlalchemy.orm import Mapped, mapped_column
from src.app.infrastructure.database.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id : Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())