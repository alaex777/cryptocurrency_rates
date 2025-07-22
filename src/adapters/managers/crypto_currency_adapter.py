from datetime import timedelta
from decimal import Decimal

from sqlalchemy.ext.asyncio.session import _AsyncSessionContextManager

from src.adapters.helpers import AdapterSession
from src.adapters.schema import CryptoCurrencyRatesTaskData
from src.clients.crypto_currency_rates_client import CryptoCurrencyRatesClient
from src.common.constants import (
    CRYPTO_CURRENCY_RATE_ACTUAL_LIFETIME,
    CRYPTO_CURRENCY_RATE_LIFETIME,
    REQUEST_CRYPTO_CURRENCY_DELAY,
)
from src.common.enums import Currency
from src.common.helpers import utcnow
from src.db.managers.manager import DBManager


class CryptoCurrencyAdapter:
    def __init__(self, db_manager: DBManager, crypto_currency_rates_client: CryptoCurrencyRatesClient) -> None:
        self._db_manager = db_manager
        self._crypto_currency_client = crypto_currency_rates_client

    def init_adapter_session(self) -> _AsyncSessionContextManager[AdapterSession]:
        return self._db_manager.session()

    def update_crypto_currency_rates_task_in_case_of_success(
        self,
        task: CryptoCurrencyRatesTaskData,
    ) -> CryptoCurrencyRatesTaskData:
        task.task = self._db_manager.crypto_currency_manager.update_crypto_currency_task(
            crypto_currency_task=task.task,
            next_attempt_at=utcnow() + timedelta(seconds=REQUEST_CRYPTO_CURRENCY_DELAY),
        )
        return task

    async def get_crypto_currency_task(
        self,
        session: AdapterSession,
    ) -> CryptoCurrencyRatesTaskData | None:
        crypto_currency_task = await self._db_manager.crypto_currency_manager.get_crypto_currency_task(
            current_session=session,
        )
        return CryptoCurrencyRatesTaskData(
            task=crypto_currency_task,
            from_currency=crypto_currency_task.from_currency,
            to_currency=crypto_currency_task.to_currency,
        ) if crypto_currency_task else None

    async def request_crypto_currency_rate(self, from_currency: Currency, to_currency: Currency) -> Decimal:
        return await self._crypto_currency_client.get_crypto_currency_rates(
            from_currency=from_currency,
            to_currency=to_currency,
        )

    async def get_current_rates(self, from_currency: Currency, to_currency: Currency) -> Decimal | None:
        crypto_currency_rate = await self._db_manager.crypto_currency_manager.get_actual_crypto_currency_rate(
            from_currency=from_currency,
            to_currency=to_currency,
            lifetime=CRYPTO_CURRENCY_RATE_ACTUAL_LIFETIME,
        )
        if crypto_currency_rate is None:
            return None
        return crypto_currency_rate.price

    async def save_crypto_currency_rate(
        self,
        from_currency: Currency,
        to_currency: Currency,
        rate: Decimal,
    ) -> None:
        await self._db_manager.crypto_currency_manager.create_crypto_currency_rate(
            from_currency=from_currency,
            to_currency=to_currency,
            price=rate,
        )

    async def delete_outdated_crypto_currency_rates(self) -> None:
        await self._db_manager.crypto_currency_manager.delete_outdated_crypto_currency_rates(
            lifetime=CRYPTO_CURRENCY_RATE_LIFETIME,
        )
