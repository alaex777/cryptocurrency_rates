from datetime import datetime, timezone
from decimal import Decimal

from freezegun import freeze_time

from src.common.enums import Currency
from src.db.managers.manager import DBManager
from src.db.models import Base
from tests.bl.builders.test_scenario_builder import BLTestCaseBuilder
from tests.bl.testdata import get_crypto_currency_rate_model
from tests.helpers import parametrize_with_dict
from tests.testdata import BTC_TO_USDT_RATE


@freeze_time(datetime(2025, 1, 1, tzinfo=timezone.utc))
@parametrize_with_dict(
    [
        'db_data',
        'expected_result',
    ],
    [
        {
            'case_id': 'success',
            'db_data': [
                get_crypto_currency_rate_model(
                    from_currency=Currency.BTC,
                    to_currency=Currency.USDT,
                    price=BTC_TO_USDT_RATE,
                ),
            ],
            'expected_result': BTC_TO_USDT_RATE,
        },
        {
            'case_id': 'no_data',
            'db_data': [],
            'expected_result': None,
        },
        {
            'case_id': 'outdated_data',
            'db_data': [
                get_crypto_currency_rate_model(
                    from_currency=Currency.BTC,
                    to_currency=Currency.USDT,
                    price=BTC_TO_USDT_RATE,
                    created_at=datetime(2024, 12, 31, 23, 58, 59, tzinfo=timezone.utc),
                    updated_at=datetime(2024, 12, 31, 23, 58, 59, tzinfo=timezone.utc),
                ),
            ],
            'expected_result': None,
        },
    ],
)
async def test_get_currencies_info(
    isolate_db_manager: DBManager,
    bl_test_case_builder: BLTestCaseBuilder,
    db_data: list[Base],
    expected_result: Decimal | None,
):
    adapters_manager = await bl_test_case_builder.prepare_scenario.get_crypto_currency_rate(
        isolate_db_manager=isolate_db_manager,
        db_data=db_data,
    )
    result = await bl_test_case_builder.call_scenario.get_crypto_currency_rate(adapters_manager=adapters_manager)
    await bl_test_case_builder.check_scenario.get_crypto_currency_rate(result=result, expected_result=expected_result)
