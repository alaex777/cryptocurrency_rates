import logging

from aiohttp import web

from settings import PING_ROUTE
from src.api.http_routes.currency_routes import CurrencyRoutes
from src.bl.bl_manager import BLManager
from src.common.exceptions import ServiceNotWorkingError

logger = logging.getLogger(__name__)


class HTTPServer:
    def __init__(self, bl_manager: BLManager) -> None:
        self._bl_manager = bl_manager

        self._currency_routes = CurrencyRoutes(bl_manager=self._bl_manager)

        self.external_app = web.Application()
        self.internal_app = web.Application()

        self._currency_routes.register(self.external_app)

        self.internal_app.router.add_get(PING_ROUTE, self.ping)

    async def ping(self, _: web.Request) -> web.Response:
        logger.info('ping request')
        try:
            await self._bl_manager.service_bl_manager.check_service_alive()
        except ServiceNotWorkingError:
            return web.Response(status=500)
        except Exception:
            logger.exception('failed to healthcheck')
            return web.Response(status=500)
        return web.Response(status=200)

    @property
    def currency_routes(self) -> CurrencyRoutes:
        return self._currency_routes
