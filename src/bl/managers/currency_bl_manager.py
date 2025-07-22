from decimal import Decimal

from src.bl.managers.base_bl_manager import BaseBLManager
from src.common.enums import Currency


class CurrencyBLManager(BaseBLManager):
    async def get_crypto_currency_rate(self, from_currency: Currency, to_currency: Currency) -> Decimal | None:
        return await self._adapters_manager.crypto_currency_adapter.get_current_rates(
            from_currency=from_currency,
            to_currency=to_currency,
        )
