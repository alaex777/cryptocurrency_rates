from src.bl.managers.base_bl_manager import BaseBLManager
from src.common.exceptions import ServiceNotWorkingError


class ServiceBLManager(BaseBLManager):
    async def check_service_alive(self) -> None:
        result = await self._adapters_manager.service_adapter.healthcheck()
        if not result:
            raise ServiceNotWorkingError
        return None
