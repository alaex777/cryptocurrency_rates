from datetime import datetime
from decimal import Decimal

from src.bl.managers.base_bl_manager import BaseBLManager
from src.common.enums import Currency
from src.common.exceptions import UnsupportedCurrencyError


class CurrencyBLManager(BaseBLManager):
    def _get_available_to_currencies(self) -> list[str]:
        return [Currency.USDT]

    def _get_available_from_currencies(self) -> list[str]:
        return [Currency.BTC, Currency.ETH]

    def _check_if_supported_currency(self, from_currency: str, to_currency: str) -> None:
        if (
            to_currency not in self._get_available_to_currencies()
            or from_currency not in self._get_available_from_currencies()
        ):
            raise UnsupportedCurrencyError

    async def _get_crypto_currency_rate(
        self,
        from_currency: Currency,
        to_currency: Currency,
        timestamp: datetime | None,
    ) -> Decimal | None:
        if timestamp is not None:
            return await self._adapters_manager.crypto_currency_adapter.get_rates_by_timestamp(
                from_currency=from_currency,
                to_currency=to_currency,
                timestamp=timestamp,
            )
        return await self._adapters_manager.crypto_currency_adapter.get_current_rates(
            from_currency=from_currency,
            to_currency=to_currency,
        )

    def _calculate_amount_in_to_currency(self, rate: Decimal | None, amount: Decimal) -> Decimal | None:
        if rate is None:
            return None
        return rate * amount

    async def get_crypto_currency_rate(
        self,
        from_currency: str,
        to_currency: str,
        amount: Decimal,
        timestamp: datetime | None,
    ) -> Decimal | None:
        self._check_if_supported_currency(from_currency=from_currency, to_currency=to_currency)
        rate = await self._get_crypto_currency_rate(
            from_currency=from_currency,  # type: ignore
            to_currency=to_currency,  # type: ignore
            timestamp=timestamp,
        )
        return self._calculate_amount_in_to_currency(rate=rate, amount=amount)
