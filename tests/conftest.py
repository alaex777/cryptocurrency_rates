import asyncio

import pytest
from aioresponses import aioresponses
from sqlalchemy.ext.asyncio import create_async_engine

import settings
from src.adapters.adapters_manager import AdaptersManager
from src.api.http_server import HTTPServer
from src.bl.bl_manager import BLManager
from src.db.managers.manager import init_db_manager
from src.db.models import Base
from tests.api.builders.test_scenario_builder import ApiTestCaseBuilder
from tests.bl.builders.test_scenario_builder import BLTestCaseBuilder
from tests.common.fake_bl_manager import FakeBLManager
from tests.common.fake_crypto_currency_rates_client import FakeCryptoCurrencyRatesClient

TEST_POSTGRES_STR_FOR_CONNECT = (
    f'postgresql+asyncpg://'
    f'{settings.POSTGRESQL_USER}:'
    f'{settings.POSTGRESQL_PASSWORD}@'
    f'{settings.POSTGRESQL_HOST}:'
    f'{settings.POSTGRESQL_PORT}/'
    f'{settings.TEST_POSTGRESQL_DATABASE}'
)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def isolate_db_manager(event_loop):
    db_manager = await init_db_manager(
        str_for_connect=TEST_POSTGRES_STR_FOR_CONNECT,
        run_migrations=False,
    )

    async with db_manager._async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield db_manager

    async with db_manager._async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db_manager.close()


@pytest.fixture(scope='function')
def alembic_engine():
    return create_async_engine(
        TEST_POSTGRES_STR_FOR_CONNECT,
        pool_pre_ping=True,
        pool_size=settings.POSTGRESQL_MAX_CONNECTIONS,
        future=True,
    )


@pytest.fixture
async def http_client(aiohttp_client, isolate_db_manager):
    crypto_currency_rates_client = FakeCryptoCurrencyRatesClient()

    adapters = AdaptersManager(
        db_manager=isolate_db_manager,
        crypto_currency_rates_client=crypto_currency_rates_client,
    )

    bl = BLManager(adapters_manager=adapters)
    server = HTTPServer(bl_manager=bl)

    client = await aiohttp_client(server.external_app)

    yield client


@pytest.fixture
def scenario_builder():
    return ApiTestCaseBuilder()


@pytest.fixture
def bl_scenario_builder():
    return BLTestCaseBuilder()


@pytest.fixture
async def mock_aioresponse(event_loop):
    with aioresponses() as mock:
        yield mock


async def fake_http_client(aiohttp_client):
    fake_bl = FakeBLManager()
    server = HTTPServer(bl_manager=fake_bl)
    client = await aiohttp_client(server.external_app)

    client.fake_bl = fake_bl

    yield client


@pytest.fixture(autouse=True)
def patch_env(monkeypatch):
    monkeypatch.setenv('ETHERSCAN_API_KEY', '6TQDKYBGR9DP85PE21GGHP69YM59E1NUYD')
