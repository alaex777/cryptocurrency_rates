from contextlib import nullcontext

import pytest

from src.clients.crypto_currency_rates_client import GetCryptoCurrencyRatesError
from tests.clients.builders.test_scenario_builder import ClientTestCaseBuilder
from tests.helpers import parametrize_with_dict
from tests.testdata import BTC_PRICE


@parametrize_with_dict(
    ['response_status', 'response_body', 'expected_response', 'exception_handler'],
    [
        {
            'case_id': 'error_400',
            'response_status': 400,
            'response_body': {},
            'expected_response': None,
            'exception_handler': pytest.raises(GetCryptoCurrencyRatesError),
        },
        {
            'case_id': 'error_empty_body',
            'response_status': 200,
            'response_body': {},
            'expected_response': None,
            'exception_handler': pytest.raises(GetCryptoCurrencyRatesError),
        },
        {
            'case_id': 'success',
            'response_status': 200,
            'response_body': {
                'price': BTC_PRICE,
            },
            'expected_response': BTC_PRICE,
            'exception_handler': nullcontext(),
        },
        {
            'case_id': 'error_500',
            'response_status': 500,
            'response_body': {
                'price': BTC_PRICE,
            },
            'expected_response': None,
            'exception_handler': pytest.raises(GetCryptoCurrencyRatesError),
        },
    ],
)
async def test_get_crypto_currency_rates(
    client_test_case_builder: ClientTestCaseBuilder,
    mock_aioresponse,
    response_status: int,
    response_body: dict,
    expected_response: dict | None,
    exception_handler: pytest.raises,
):
    client = await client_test_case_builder.prepare_scenario.get_crypto_currency_rates(
        mock_aioresponse=mock_aioresponse,
        response_status=response_status,
        response_body=response_body,
    )

    response = await client_test_case_builder.call_scenario.get_crypto_currency_rates(
        exception_handler=exception_handler,
        client=client,
    )

    await client_test_case_builder.check_scenario.get_crypto_currency_rates(
        mock_aioresponse=mock_aioresponse,
        response=response,
        expected_response=expected_response,
        client=client,
    )
