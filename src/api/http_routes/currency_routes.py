from aiohttp import web

from src.api.http_routes.base_routes import BASE_PATH, BaseRoutes
from src.api.schema import GetCryptoCurrencyRateRequest
from src.api.wrappers import http_api_method_wrapper
from src.common.enums import Currency


class CurrencyRoutes(BaseRoutes):
    def register(self, app: web.Application) -> None:
        app.router.add_get(BASE_PATH + 'crypto-currency/rate', self._get_crypto_currency_rate)

    @http_api_method_wrapper(GetCryptoCurrencyRateRequest)
    async def _get_crypto_currency_rate(self, request: GetCryptoCurrencyRateRequest) -> web.Response:
        if request.query.from_currency not in Currency or request.query.to_currency not in Currency:
            return web.json_response(
                {
                    'result_code': 'unsupported_currency',
                },
                status=400,
            )

        currencies_info = await self._bl_manager.currency_bl_manager.get_crypto_currency_rate(
            from_currency=Currency(request.query.from_currency),
            to_currency=Currency(request.query.to_currency),
        )

        if currencies_info is None:
            return web.json_response(
                {
                    'result_code': 'quotes_outdated',
                },
                status=400,
            )

        return web.json_response(
            {
                'result_code': 'success',
                'rate': str(currencies_info),
            },
            status=200,
        )
