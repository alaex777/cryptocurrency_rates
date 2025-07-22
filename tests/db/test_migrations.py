import pytest
from pytest_alembic.tests import test_model_definitions_match_ddl  # noqa
from pytest_alembic.tests import test_single_head_revision  # noqa
from pytest_alembic.tests import test_up_down_consistency  # noqa
from pytest_alembic.tests import test_upgrade  # noqa


@pytest.mark.alembic
def test_downgrade(alembic_runner):
    # pytest_alembic оставляет за собой актуальную версию базы, это может ломать последующие тесты.
    # Этот тест откатывает все миграции
    alembic_runner.migrate_down_to('base')
