from unittest import mock

from src.db.managers.manager import DBManager


async def test_healthcheck(isolate_db_manager: DBManager):
    healthcheck_result = await isolate_db_manager.healthcheck()
    assert healthcheck_result is True

    with mock.patch.object(DBManager, 'session', new=lambda x: False):
        healthcheck_result = await isolate_db_manager.healthcheck()
        assert healthcheck_result is False
