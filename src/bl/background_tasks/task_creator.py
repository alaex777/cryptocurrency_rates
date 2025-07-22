import logging

from src.adapters.adapters_manager import AdaptersManager
from src.bl.background_tasks.interval_task import IntervalTask
from src.bl.background_tasks.save_crypto_currency_rates_task import save_crypto_currency_rates
from src.common.constants import CRYPTO_CURRENCY_RATE_TASK_PERIOD

logger = logging.getLogger(__name__)


def create_crypto_currencies_task(adapters_manager: AdaptersManager) -> IntervalTask:
    return IntervalTask(
        name='crypto_currencies',
        period=CRYPTO_CURRENCY_RATE_TASK_PERIOD,
        func=lambda: save_crypto_currency_rates(adapters_manager=adapters_manager),
    )
