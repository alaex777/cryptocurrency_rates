from src.adapters.adapters_manager import AdaptersManager
from src.bl.managers.base_bl_manager import BaseBLManager
from src.bl.managers.currency_bl_manager import CurrencyBLManager
from src.bl.managers.service_bl import ServiceBLManager


class BLManager(BaseBLManager):
    def __init__(self, adapters_manager: AdaptersManager) -> None:
        super().__init__(adapters_manager=adapters_manager)
        self._service_bl_manager = ServiceBLManager(adapters_manager=adapters_manager)
        self._currency_bl_manager = CurrencyBLManager(adapters_manager=adapters_manager)

    @property
    def service_bl_manager(self) -> ServiceBLManager:
        return self._service_bl_manager

    @property
    def currency_bl_manager(self) -> CurrencyBLManager:
        return self._currency_bl_manager
