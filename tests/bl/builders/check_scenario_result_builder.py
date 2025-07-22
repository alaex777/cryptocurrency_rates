from decimal import Decimal
from typing import Any

from sqlalchemy import select

from src.db.managers.manager import DBManager
from src.db.models import CryptoCurrencyRate, CryptoCurrencyTask
from tests.helpers import compare_models_with_attrs


class CheckScenarioBuilder:
    def __init__(self) -> None:
        ...

    async def save_crypto_currency_rates(
        self,
        db_manager: DBManager,
        expected_crypto_currencies: list[dict[str, Any]],
        expected_crypto_currency_tasks: list[dict[str, Any]],
    ) -> None:
        async with db_manager.session() as session:
            crypto_currencies = (await session.scalars(select(CryptoCurrencyRate))).all()
            compare_models_with_attrs(crypto_currencies, expected_crypto_currencies)

            crypto_currency_tasks = (await session.scalars(select(CryptoCurrencyTask))).all()
            compare_models_with_attrs(crypto_currency_tasks, expected_crypto_currency_tasks)

    async def get_crypto_currency_rate(self, result: Decimal | None, expected_result: Decimal | None) -> None:
        assert result == expected_result
