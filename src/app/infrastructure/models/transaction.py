import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Enum as SAEnum
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.entities.transaction import TransactionType
from app.infrastructure.database.base import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    account_number: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.account_number"),
        nullable=False,
        index=True,
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("accounts.account_id"),
        nullable=False,
        index=True,
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        SAEnum(TransactionType),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    balance_after: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
