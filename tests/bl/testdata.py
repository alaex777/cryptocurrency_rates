from datetime import datetime, timezone
from decimal import Decimal

from src.common.enums import Currency
from src.db.models import CryptoCurrencyRate, CryptoCurrencyTask
from tests.testdata import USDT_PRICE


def get_crypto_currency_rate_model(
    from_currency: Currency = Currency.BTC,
    to_currency: Currency = Currency.USDT,
    price: Decimal = USDT_PRICE,
    created_at: datetime = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    updated_at: datetime = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
) -> CryptoCurrencyRate:
    return CryptoCurrencyRate(
        from_currency=from_currency,
        to_currency=to_currency,
        price=price,
        created_at=created_at,
        updated_at=updated_at,
    )


def get_crypto_currency_task_model(
    from_currency: Currency = Currency.BTC,
    to_currency: Currency = Currency.USDT,
    next_attempt_at: datetime = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
) -> CryptoCurrencyTask:
    return CryptoCurrencyTask(
        from_currency=from_currency,
        to_currency=to_currency,
        next_attempt_at=next_attempt_at,
    )
