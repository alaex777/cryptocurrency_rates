from decimal import Decimal

from src.api.http_server import HTTPServer
from tests.common.fake_bl_manager import FakeBLManager


class PrepareScenarioBuilder:
    def __init__(self) -> None:
        self._create_response = None

    @property
    def create_response(self):
        return self._create_response

    async def get_crypto_currency_rate(self, bl_response: Decimal | None) -> HTTPServer:
        bl_manager = FakeBLManager()
        bl_manager._currency_bl_manager.get_crypto_currency_rate_response = bl_response
        return HTTPServer(bl_manager=bl_manager)
