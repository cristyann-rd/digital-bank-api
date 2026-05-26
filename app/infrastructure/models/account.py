from sqlalchemy import Integer,Boolean, String, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.squence import account_number_seq
from app.infrastructure.database.base import Base


class AccountModel(Base):
    __tablename__ = "accounts"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    account_number : Mapped[str] = mapped_column(account_number_seq, server_default=account_number_seq.next_value(), nullable=False)
    account_digit : Mapped[str] = mapped_column(String(1), nullable=False, autoincrement=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())