import pytest

from tests.clients.builders.test_scenario_builder import ClientTestCaseBuilder


@pytest.fixture(scope='function')
def client_test_case_builder() -> ClientTestCaseBuilder:
    return ClientTestCaseBuilder()
