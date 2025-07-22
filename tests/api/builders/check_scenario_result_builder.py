from typing import Any

from aiohttp import web


class CheckScenarioBuilder:
    def __init__(self) -> None:
        pass

    async def get_crypto_currency_rate(
        self,
        response: web.Response,
        expected_response: dict[str, Any],
        expected_status: int,
    ) -> None:
        assert response.status == expected_status
        assert await response.json() == expected_response
