from aioresponses import aioresponses

from src.clients.crypto_currency_rates_client import CryptoCurrencyRatesClient


class CheckScenarioBuilder:
    def __init__(self) -> None:
        ...

    async def get_crypto_currency_rates(
        self,
        mock_aioresponse: aioresponses,
        response: dict | None,
        expected_response: dict | None,
        client: CryptoCurrencyRatesClient,
    ) -> None:
        assert response == expected_response
        assert list(mock_aioresponse.requests.values())[0][0].kwargs['params'] == {'symbol': 'BTCUSDT'}
        await client.close()
