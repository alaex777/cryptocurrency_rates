from datetime import datetime
from urllib.parse import quote

from aiohttp import web
from aiohttp.pytest_plugin import AiohttpClient

from src.api.http_server import HTTPServer


class CallScenarioBuilder:
    async def get_crypto_currency_rate(
        self,
        aiohttp_client: AiohttpClient,
        http_server: HTTPServer,
        timestamp: datetime | None = None,
    ) -> web.Response:
        client = await aiohttp_client(http_server.external_app)
        url = '/api/v1/convert?from=BTC&to=USDT&amount=1000'
        if timestamp is not None:
            timestamp_str = timestamp.isoformat().replace('+00:00', 'Z')
            url += f'&timestamp={quote(timestamp_str)}'
        return await client.get(url)
