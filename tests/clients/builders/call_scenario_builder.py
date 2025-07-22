from decimal import Decimal

import pytest

from src.clients.crypto_currency_rates_client import CryptoCurrencyRatesClient
from src.common.enums import Currency


class CallScenarioBuilder:
    def __init__(self) -> None:
        ...

    async def get_crypto_currency_rates(
        self,
        exception_handler: pytest.raises,
        client: CryptoCurrencyRatesClient,
    ) -> dict[Currency, Decimal] | None:
        with exception_handler:
            return await client.get_crypto_currency_rates(from_currency=Currency.BTC, to_currency=Currency.USDT)
        return None
