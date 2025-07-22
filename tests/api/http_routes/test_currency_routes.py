from decimal import Decimal

from tests.api.builders.test_scenario_builder import ApiTestCaseBuilder
from tests.helpers import parametrize_with_dict
from tests.testdata import BTC_TO_USDT_RATE


@parametrize_with_dict(
    [
        'bl_response',
        'expected_response',
        'expected_status',
    ],
    [
        {
            'case_id': 'success',
            'bl_response': BTC_TO_USDT_RATE,
            'expected_response': {
                'result_code': 'success',
                'rate': str(BTC_TO_USDT_RATE),
            },
            'expected_status': 200,
        },
        {
            'case_id': 'outdated',
            'bl_response': None,
            'expected_response': {
                'result_code': 'quotes_outdated',
            },
            'expected_status': 400,
        },
    ],
)
async def test_get_crypto_currency_rate(
    aiohttp_client,
    api_scenario_builder: ApiTestCaseBuilder,
    bl_response: Decimal | None,
    expected_response: dict,
    expected_status: int,
):
    http_server = await api_scenario_builder.prepare_scenario.get_crypto_currency_rate(bl_response=bl_response)
    response = await api_scenario_builder.call_scenario.get_crypto_currency_rate(
        aiohttp_client=aiohttp_client,
        http_server=http_server,
    )
    await api_scenario_builder.check_scenario.get_crypto_currency_rate(
        response=response,
        expected_response=expected_response,
        expected_status=expected_status,
    )
