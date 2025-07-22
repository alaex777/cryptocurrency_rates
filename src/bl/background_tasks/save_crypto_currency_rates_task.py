import logging
from decimal import Decimal

from src.adapters.adapters_manager import AdaptersManager
from src.adapters.schema import CryptoCurrencyRatesTaskData
from src.common.context_variables import TASK_DATA

logger = logging.getLogger(__name__)


async def _process_crypto_currency_rate_in_case_of_success(
    task: CryptoCurrencyRatesTaskData,
    adapters_manager: AdaptersManager,
    rate: Decimal,
) -> None:
    await adapters_manager.crypto_currency_adapter.save_crypto_currency_rate(
        from_currency=task.from_currency,
        to_currency=task.to_currency,
        rate=rate,
    )
    adapters_manager.crypto_currency_adapter.update_crypto_currency_rates_task_in_case_of_success(task=task)


async def _request_crypto_currency_rate(
    task: CryptoCurrencyRatesTaskData,
    adapters_manager: AdaptersManager,
) -> Decimal | None:
    try:
        return await adapters_manager.crypto_currency_adapter.request_crypto_currency_rate(
            from_currency=task.from_currency,
            to_currency=task.to_currency,
        )
    except Exception:
        logger.exception('exception occurred while requesting crypto currency rates')
        return None


async def _delete_outdated_crypto_currency_rates(adapters_manager: AdaptersManager) -> None:
    await adapters_manager.crypto_currency_adapter.delete_outdated_crypto_currency_rates()


async def _request_and_save_new_crypto_currency_rate(
    task: CryptoCurrencyRatesTaskData,
    adapters_manager: AdaptersManager,
) -> None:
    rate = await _request_crypto_currency_rate(task=task, adapters_manager=adapters_manager)
    if rate is None:
        return
    await _process_crypto_currency_rate_in_case_of_success(task=task, adapters_manager=adapters_manager, rate=rate)


async def request_crypto_currency_rates_task(
    task: CryptoCurrencyRatesTaskData,
    adapters_manager: AdaptersManager,
) -> None:
    await _delete_outdated_crypto_currency_rates(adapters_manager=adapters_manager)
    await _request_and_save_new_crypto_currency_rate(task=task, adapters_manager=adapters_manager)


async def save_crypto_currency_rates(adapters_manager: AdaptersManager) -> None:
    try:
        async with adapters_manager.crypto_currency_adapter.init_adapter_session() as session:
            task = await adapters_manager.crypto_currency_adapter.get_crypto_currency_task(session=session)
            if task is None:
                return

            TASK_DATA.set({'tasks': [task.task.__dict__]})
            logger.info(
                f'started request crypto currency rates task for {task.from_currency} to {task.to_currency} pair',
            )

            await request_crypto_currency_rates_task(task=task, adapters_manager=adapters_manager)
    except Exception:
        logger.exception('exception occurred while requesting crypto currency rates')
        return
