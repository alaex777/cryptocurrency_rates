from decimal import Decimal

from src.clients.crypto_currency_rates_client import CryptoCurrencyRatesClient
from src.common.enums import Currency
from tests.common.helpers import return_or_raise
from tests.testdata import BTC_TO_USDT_RATE


class FakeCryptoCurrencyRatesClient(CryptoCurrencyRatesClient):
    def __init__(self):
        super().__init__()
        self.called_args = []
        self.get_crypto_currency_rates_response = BTC_TO_USDT_RATE

    async def get_crypto_currency_rates(
        self,
        from_currency: Currency,
        to_currency: Currency,
    ) -> Decimal:
        self.called_args.append(
            {
                'method': 'get_crypto_currency_rates',
                'data': {},
            },
        )
        return return_or_raise(self.get_crypto_currency_rates_response)
