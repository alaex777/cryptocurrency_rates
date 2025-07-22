import pytest

from tests.bl.builders.test_scenario_builder import BLTestCaseBuilder


@pytest.fixture(scope='function')
def bl_test_case_builder() -> BLTestCaseBuilder:
    return BLTestCaseBuilder()
