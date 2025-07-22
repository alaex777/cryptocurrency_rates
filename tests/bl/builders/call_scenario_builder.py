from decimal import Decimal

from src.adapters.adapters_manager import AdaptersManager
from src.bl.background_tasks.save_crypto_currency_rates_task import save_crypto_currency_rates
from src.bl.bl_manager import BLManager
from src.common.enums import Currency


class CallScenarioBuilder:
    def __init__(self) -> None: ...

    async def save_crypto_currency_rates(self, adapters_manager: AdaptersManager) -> None:
        await save_crypto_currency_rates(adapters_manager=adapters_manager)

    async def get_crypto_currency_rate(self, adapters_manager: AdaptersManager) -> Decimal | None:
        return await BLManager(adapters_manager=adapters_manager).currency_bl_manager.get_crypto_currency_rate(
            from_currency=Currency.BTC,
            to_currency=Currency.USDT,
        )
