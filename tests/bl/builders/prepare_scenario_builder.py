from decimal import Decimal

from src.adapters.adapters_manager import AdaptersManager
from src.common.enums import Currency
from src.db.managers.manager import DBManager
from src.db.models import Base
from tests.common.fake_crypto_currency_rates_client import FakeCryptoCurrencyRatesClient


class PrepareScenarioBuilder:
    def __init__(self) -> None:
        ...

    async def save_crypto_currency_rates(
        self,
        isolate_db_manager: DBManager,
        db_data: list[Base],
        crypto_currency_rates_response: dict[Currency, Decimal] | Exception,
    ) -> AdaptersManager:
        async with isolate_db_manager.session() as session:
            session.add_all(db_data)
            await session.commit()

        crypto_currency_rates_client = FakeCryptoCurrencyRatesClient()
        crypto_currency_rates_client.get_crypto_currency_rates_response = crypto_currency_rates_response

        return AdaptersManager(
            db_manager=isolate_db_manager,
            crypto_currency_rates_client=crypto_currency_rates_client,
        )

    async def get_crypto_currency_rate(
        self,
        isolate_db_manager: DBManager,
        db_data: list[Base],
    ) -> AdaptersManager:
        async with isolate_db_manager.session() as session:
            session.add_all(db_data)
            await session.commit()

        return AdaptersManager(
            db_manager=isolate_db_manager,
            crypto_currency_rates_client=FakeCryptoCurrencyRatesClient(),
        )
