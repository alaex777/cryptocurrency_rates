import logging
from decimal import Decimal

import aiohttp

import settings
from src.common.enums import Currency

logger = logging.getLogger(__name__)


class GetCryptoCurrencyRatesError(Exception):
    pass


class CryptoCurrencyRatesClient:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()
        self._base_url = settings.BINANCE_BASE_URL

    async def close(self) -> None:
        await self._session.close()

    async def get_crypto_currency_rates(self, from_currency: Currency, to_currency: Currency) -> Decimal:
        url = f'{self._base_url}/ticker/price'
        params = {
            'symbol': f'{from_currency}{to_currency}',
        }
        logger.info(f'requesting crypto currency rates for {from_currency} to {to_currency} on {url=}')

        try:
            async with self._session.get(url=url, params=params) as response:
                text = await response.text()
                logger.info(f'got {response.status=} with {text=} while requesting crypto currency rates')
                if response.status == 200:
                    data = await response.json()
                    return Decimal(data['price'])
                logger.error(f'got {response.status=} while requesting crypto currency rates')
        except Exception:
            logger.exception('exception occurred while requesting crypto currency rates')
        raise GetCryptoCurrencyRatesError
