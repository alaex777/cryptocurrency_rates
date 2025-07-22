from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.common.enums import Currency
from src.common.helpers import utcnow


class Base(DeclarativeBase):
    pass


class CryptoCurrencyRate(Base):
    __tablename__ = 'crypto_currency_rate'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    from_currency: Mapped[Currency] = mapped_column(String, nullable=False)
    to_currency: Mapped[Currency] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )


class CryptoCurrencyTask(Base):
    __tablename__ = 'crypto_currency_task'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    from_currency: Mapped[Currency] = mapped_column(String, nullable=False)
    to_currency: Mapped[Currency] = mapped_column(String, nullable=False)
    next_attempt_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )
