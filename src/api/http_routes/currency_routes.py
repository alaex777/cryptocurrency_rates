from aiohttp import web

from src.api.http_routes.base_routes import BASE_PATH, BaseRoutes
from src.api.schema import GetCryptoCurrencyRateRequest
from src.api.wrappers import http_api_method_wrapper
from src.common.exceptions import UnsupportedCurrencyError


class CurrencyRoutes(BaseRoutes):
    def register(self, app: web.Application) -> None:
        app.router.add_get(BASE_PATH + 'convert', self._get_crypto_currency_rate)

    @http_api_method_wrapper(GetCryptoCurrencyRateRequest)
    async def _get_crypto_currency_rate(self, request: GetCryptoCurrencyRateRequest) -> web.Response:
        try:
            rate = await self._bl_manager.currency_bl_manager.get_crypto_currency_rate(
                from_currency=request.query.from_currency,
                to_currency=request.query.to_currency,
                amount=request.query.amount,
                timestamp=request.query.timestamp,
            )
        except UnsupportedCurrencyError:
            return web.json_response(
                {
                    'result_code': 'unsupported_currency',
                },
                status=400,
            )

        if rate is None:
            return web.json_response(
                {
                    'result_code': 'quotes_outdated',
                },
                status=400,
            )

        return web.json_response(
            {
                'result_code': 'success',
                'rate': str(rate),
            },
            status=200,
        )
