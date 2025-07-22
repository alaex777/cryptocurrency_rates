from aioresponses import aioresponses

from src.clients.crypto_currency_rates_client import CryptoCurrencyRatesClient
from src.common.helpers import json_dumps


class PrepareScenarioBuilder:
    def __init__(self) -> None:
        ...

    async def get_crypto_currency_rates(
        self,
        mock_aioresponse: aioresponses,
        response_status: int,
        response_body: dict,
    ) -> CryptoCurrencyRatesClient:
        mock_aioresponse.get(
            url='https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT',
            status=response_status,
            body=json_dumps(response_body),
        )
        client = CryptoCurrencyRatesClient()
        return client
