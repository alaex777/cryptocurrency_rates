import pytest

from tests.api.builders.test_scenario_builder import ApiTestCaseBuilder


@pytest.fixture
def api_scenario_builder() -> ApiTestCaseBuilder:
    return ApiTestCaseBuilder()
