
from src.adapters.managers.crypto_currency_adapter import CryptoCurrencyAdapter
from src.adapters.managers.service_adapters import SerivceAdapter
from src.clients.crypto_currency_rates_client import CryptoCurrencyRatesClient
from src.db.managers.manager import DBManager


class AdaptersManager:
    def __init__(
        self,
        db_manager: DBManager,
        crypto_currency_rates_client: CryptoCurrencyRatesClient,
    ) -> None:
        self._service_adapter = SerivceAdapter(db_manager=db_manager)
        self._crypto_currency_adapter = CryptoCurrencyAdapter(
            db_manager=db_manager,
            crypto_currency_rates_client=crypto_currency_rates_client,
        )

    @property
    def crypto_currency_adapter(self) -> CryptoCurrencyAdapter:
        return self._crypto_currency_adapter

    @property
    def service_adapter(self) -> SerivceAdapter:
        return self._service_adapter
