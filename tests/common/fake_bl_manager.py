from datetime import datetime
from decimal import Decimal

from src.bl.bl_manager import BLManager
from src.bl.managers.currency_bl_manager import CurrencyBLManager
from src.bl.managers.service_bl import ServiceBLManager
from tests.common.helpers import return_or_raise
from tests.testdata import BTC_TO_USDT_RATE


class FakeBLManager(BLManager):
    def __init__(self) -> None:
        self._service_bl_manager = FakeServiceBLManager()
        self._currency_bl_manager = FakeCurrencyBLManager()


class FakeServiceBLManager(ServiceBLManager):
    def __init__(self) -> None:
        self.called_args = []

    async def check_service_alive(self) -> None:
        self.called_args.append(
            {
                'method': 'check_service_alive',
                'data': {},
            },
        )
        return None


class FakeCurrencyBLManager(CurrencyBLManager):
    def __init__(self) -> None:
        self.called_args = []
        self.get_crypto_currency_rate_response = BTC_TO_USDT_RATE

    async def get_crypto_currency_rate(
        self,
        from_currency: str,
        to_currency: str,
        amount: Decimal,
        timestamp: datetime | None,
    ) -> Decimal | None:
        return return_or_raise(self.get_crypto_currency_rate_response)


async def get_fake_bl_manager() -> FakeBLManager:
    return FakeBLManager()
