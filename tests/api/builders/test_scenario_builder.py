from tests.api.builders.call_scenario_builder import CallScenarioBuilder
from tests.api.builders.check_scenario_result_builder import CheckScenarioBuilder
from tests.api.builders.prepare_scenario_builder import PrepareScenarioBuilder


class ApiTestCaseBuilder:
    def __init__(self) -> None:
        self._prepare_scenario = PrepareScenarioBuilder()
        self._call_scenario = CallScenarioBuilder()
        self._check_scenario = CheckScenarioBuilder()

    @property
    def prepare_scenario(self) -> PrepareScenarioBuilder:
        return self._prepare_scenario

    @property
    def call_scenario(self) -> CallScenarioBuilder:
        return self._call_scenario

    @property
    def check_scenario(self) -> CheckScenarioBuilder:
        return self._check_scenario
