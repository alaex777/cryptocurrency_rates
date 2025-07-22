import asyncio
import logging.config
import sys
import warnings
from functools import wraps
from typing import Any, Awaitable, Callable

import uvloop
from aiohttp import web

import settings
from src.adapters.adapters_manager import AdaptersManager
from src.api.http_server import HTTPServer
from src.bl.background_tasks.task_creator import create_crypto_currencies_task
from src.bl.bl_manager import BLManager
from src.clients.crypto_currency_rates_client import CryptoCurrencyRatesClient
from src.common.context_binder import LOG_CONTEXT_BINDER
from src.db.managers.manager import init_db_manager

logger = logging.getLogger(__name__)


def on_shutdown_wrapper(coroutine: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
    """
    Wrapper to run on_cleanup coroutines without aiohttp app argument.
    """

    @wraps(coroutine)
    async def skip_app_wrapper(_):
        try:
            return await coroutine()
        except Exception:
            logger.exception('exception occurred on graceful shutdown')

    return skip_app_wrapper


def on_shutdown_wrapper_for_common_func(func: Callable[..., Any]) -> Callable[..., Awaitable]:

    @wraps(func)
    async def skip_app_wrapper(_):
        try:
            return func()
        except Exception:
            logger.exception('exception occurred on graceful shutdown')

    return skip_app_wrapper


async def get_http_server() -> HTTPServer:
    logger.info('create db manager')
    db_manager = await init_db_manager(str_for_connect=settings.POSTGRES_STR_FOR_CONNECT)

    logger.info('create crypto currency rates client')
    crypto_currency_rates_client = CryptoCurrencyRatesClient()

    logger.info('create adapters manager')
    adapters_manager = AdaptersManager(
        db_manager=db_manager,
        crypto_currency_rates_client=crypto_currency_rates_client,
    )

    logger.info('create bl manager')
    bl_manager = BLManager(adapters_manager=adapters_manager)

    logger.info('create save crypto currency rates task')
    save_crypto_currency_rates_task = create_crypto_currencies_task(adapters_manager=adapters_manager)
    save_crypto_currency_rates_task.start()

    logger.info('create http server')
    http_server = HTTPServer(bl_manager=bl_manager)
    http_server.external_app.on_shutdown.extend(
        [
            on_shutdown_wrapper(save_crypto_currency_rates_task.stop),
            on_shutdown_wrapper(db_manager.close),
        ],
    )

    return http_server


async def start_server(app: web.Application, port: int, runners: list[web.AppRunner]):
    logger.info(f'starting http server on {port=}')
    runner = web.AppRunner(app, handle_signals=True)
    runners.append(runner)
    await runner.setup()
    site = web.TCPSite(runner, settings.APP_HOST, port)
    await site.start()


if __name__ == '__main__':
    logging.getLogger('').addFilter(LOG_CONTEXT_BINDER)
    logging.config.dictConfig(settings.LOGGING)
    for handler in logging.getLogger('').handlers:
        handler.addFilter(LOG_CONTEXT_BINDER)
    warnings.filterwarnings('ignore')

    logger.info('set event loop as uvloop')
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        http_server = loop.run_until_complete(get_http_server())
    except Exception:
        logger.critical('failed to initialize http server', exc_info=True)
        sys.exit(1)

    logger.info('start http servers')
    runners = []
    loop.create_task(start_server(app=http_server.internal_app, port=settings.INTERNAL_PORT, runners=runners))
    loop.create_task(start_server(app=http_server.external_app, port=settings.EXTERNAL_PORT, runners=runners))

    try:
        loop.run_forever()
    except Exception:
        logger.warning('server loop stopped', exc_info=True)
        pass
    finally:
        logger.info('run cleanup')
        for runner in runners:
            loop.run_until_complete(runner.cleanup())
