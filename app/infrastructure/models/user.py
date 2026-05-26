from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base


class UserModel(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash : Mapped[str] = mapped_column(String, nullable=False)
    
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())