from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.common.constants import CRYPTO_CURRENCY_RATE_TIMESTAMP_TOLERANCE
from src.common.enums import Currency
from src.common.helpers import utcnow
from src.db.managers.base_manager import OMITTED, BaseDBManager, Omittable
from src.db.models import CryptoCurrencyRate, CryptoCurrencyTask


class CryptoCurrencyDBManager(BaseDBManager):
    def __init__(self, async_engine: AsyncEngine) -> None:
        super().__init__(async_engine)

    def update_crypto_currency_task(
        self,
        crypto_currency_task: CryptoCurrencyTask,
        next_attempt_at: Omittable[datetime] = OMITTED,
    ) -> CryptoCurrencyTask:
        for attr, value in [
            ('next_attempt_at', next_attempt_at),
        ]:
            if value is not OMITTED:
                setattr(crypto_currency_task, attr, value)

        return crypto_currency_task

    async def get_crypto_currency_task(
        self,
        current_session: AsyncSession | None = None,
    ) -> CryptoCurrencyTask | None:
        async with self.use_or_create_session(current_session) as session:
            return await session.scalar(
                select(CryptoCurrencyTask)
                .with_for_update(skip_locked=True)
                .where(CryptoCurrencyTask.next_attempt_at <= utcnow())
                .order_by(desc(CryptoCurrencyTask.next_attempt_at))
                .limit(1),
            )

    async def get_actual_crypto_currency_rate(
        self,
        from_currency: Currency,
        to_currency: Currency,
        lifetime: int,
        current_session: AsyncSession | None = None,
    ) -> CryptoCurrencyRate | None:
        async with self.use_or_create_session(current_session) as session:
            return await session.scalar(
                select(CryptoCurrencyRate)
                .where(
                    CryptoCurrencyRate.from_currency == from_currency,
                    CryptoCurrencyRate.to_currency == to_currency,
                    CryptoCurrencyRate.created_at >= utcnow() - timedelta(seconds=lifetime),
                )
                .order_by(desc(CryptoCurrencyRate.created_at))
                .limit(1),
            )

    async def get_crypto_currency_rate_by_timestamp(
        self,
        from_currency: Currency,
        to_currency: Currency,
        timestamp: datetime,
        current_session: AsyncSession | None = None,
    ) -> CryptoCurrencyRate | None:
        async with self.use_or_create_session(current_session) as session:
            return await session.scalar(
                select(CryptoCurrencyRate)
                .where(
                    CryptoCurrencyRate.from_currency == from_currency,
                    CryptoCurrencyRate.to_currency == to_currency,
                    CryptoCurrencyRate.created_at <= timestamp,
                    CryptoCurrencyRate.created_at >= timestamp - timedelta(
                        seconds=CRYPTO_CURRENCY_RATE_TIMESTAMP_TOLERANCE,
                    ),
                )
                .order_by(desc(CryptoCurrencyRate.created_at))
                .limit(1),
            )

    async def create_crypto_currency_rate(
        self,
        from_currency: Currency,
        to_currency: Currency,
        price: Decimal,
        current_session: AsyncSession | None = None,
    ) -> CryptoCurrencyRate:
        async with self.use_or_create_session(current_session) as session:
            crypto_currency_rate = CryptoCurrencyRate(
                from_currency=from_currency,
                to_currency=to_currency,
                price=price,
            )
            session.add(crypto_currency_rate)
        return crypto_currency_rate

    async def delete_outdated_crypto_currency_rates(
        self,
        lifetime: int,
        current_session: AsyncSession | None = None,
    ) -> None:
        async with self.use_or_create_session(current_session) as session:
            await session.execute(
                delete(CryptoCurrencyRate)
                .where(CryptoCurrencyRate.created_at <= utcnow() - timedelta(seconds=lifetime)),
            )
