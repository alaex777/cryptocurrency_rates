from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from freezegun import freeze_time

from src.common.enums import Currency
from src.db.managers.manager import DBManager
from src.db.models import Base
from tests.bl.builders.test_scenario_builder import BLTestCaseBuilder
from tests.bl.testdata import get_crypto_currency_rate_model, get_crypto_currency_task_model
from tests.helpers import parametrize_with_dict
from tests.testdata import BTC_TO_USDT_RATE


@freeze_time(datetime(2025, 1, 1, tzinfo=timezone.utc))
@parametrize_with_dict(
    [
        'db_data',
        'crypto_currency_rates_response',
        'expected_crypto_currencies',
        'expected_crypto_currency_tasks',
    ],
    [
        {
            'case_id': 'empty_db',
            'db_data': [],
            'crypto_currency_rates_response': None,
            'expected_crypto_currencies': [],
            'expected_crypto_currency_tasks': [],
        },
        {
            'case_id': 'success',
            'db_data': [
                get_crypto_currency_task_model(from_currency=Currency.BTC, to_currency=Currency.USDT),
            ],
            'crypto_currency_rates_response': BTC_TO_USDT_RATE,
            'expected_crypto_currencies': [
                {
                    'from_currency': Currency.BTC,
                    'to_currency': Currency.USDT,
                    'price': BTC_TO_USDT_RATE,
                },
            ],
            'expected_crypto_currency_tasks': [
                {
                    'from_currency': Currency.BTC,
                    'to_currency': Currency.USDT,
                    'next_attempt_at': datetime(2025, 1, 1, 0, 0, 30, tzinfo=timezone.utc),
                },
            ],
        },
        {
            'case_id': 'success_with_outdated_data',
            'db_data': [
                get_crypto_currency_task_model(from_currency=Currency.BTC, to_currency=Currency.USDT),
                get_crypto_currency_rate_model(
                    from_currency=Currency.BTC,
                    to_currency=Currency.USDT,
                    price=BTC_TO_USDT_RATE,
                    created_at=datetime(2024, 12, 25, tzinfo=timezone.utc),
                    updated_at=datetime(2024, 12, 25, tzinfo=timezone.utc),
                ),
            ],
            'crypto_currency_rates_response': BTC_TO_USDT_RATE,
            'expected_crypto_currencies': [
                {
                    'from_currency': Currency.BTC,
                    'to_currency': Currency.USDT,
                    'price': BTC_TO_USDT_RATE,
                },
            ],
            'expected_crypto_currency_tasks': [
                {
                    'from_currency': Currency.BTC,
                    'to_currency': Currency.USDT,
                    'next_attempt_at': datetime(2025, 1, 1, 0, 0, 30, tzinfo=timezone.utc),
                },
            ],
        },
    ],
)
async def test_save_crypto_currency_rates(
    bl_test_case_builder: BLTestCaseBuilder,
    isolate_db_manager: DBManager,
    db_data: list[Base],
    crypto_currency_rates_response: dict[Currency, Decimal],
    expected_crypto_currencies: list[dict[str, Any]],
    expected_crypto_currency_tasks: list[dict[str, Any]],
):
    adapters_manager = await bl_test_case_builder.prepare_scenario.save_crypto_currency_rates(
        isolate_db_manager=isolate_db_manager,
        db_data=db_data,
        crypto_currency_rates_response=crypto_currency_rates_response,
    )

    await bl_test_case_builder.call_scenario.save_crypto_currency_rates(adapters_manager=adapters_manager)

    await bl_test_case_builder.check_scenario.save_crypto_currency_rates(
        db_manager=isolate_db_manager,
        expected_crypto_currencies=expected_crypto_currencies,
        expected_crypto_currency_tasks=expected_crypto_currency_tasks,
    )
