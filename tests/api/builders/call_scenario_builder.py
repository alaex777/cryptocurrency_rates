from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

from src.api.http_server import HTTPServer


class CallScenarioBuilder:
    async def get_crypto_currency_rate(self, aiohttp_client: AiohttpClient, http_server: HTTPServer) -> web.Response:
        client = await aiohttp_client(http_server.external_app)
        return await client.get('/api/v1/crypto-currency/rate?from_currency=BTC&to_currency=USDT')
