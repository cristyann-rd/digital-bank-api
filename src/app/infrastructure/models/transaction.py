import uuid
from decimal import Decimal
from datetime import datetime


from sqlalchemy import String, DateTime, Numeric, ForeignKey, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.app.infrastructure.database.base import Base
from src.app.domain.entities.transaction import TransactionType



class TransactionModel(Base):
    __tablename__ = "transactions"
    
    transaction_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
        )
    
    account_id : Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("accounts.account_id"),
        nullable=False
        )
    
    transaction_type: Mapped[TransactionType] = mapped_column(
    SAEnum(TransactionType),
    nullable=False
        )

    amount: Mapped[Decimal]= mapped_column(
        Numeric, 
        nullable=False
        )
    
    
    balance_after: Mapped[Decimal]= mapped_column(
        Numeric, 
        nullable=False
        )
    
    description: Mapped[str] = mapped_column(
        String(), 
        nullable=False
        )
    
    
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
        )
    
