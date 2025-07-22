from dataclasses import dataclass

from src.common.enums import Currency
from src.db.models import CryptoCurrencyTask


@dataclass
class CryptoCurrencyRatesTaskData:
    task: CryptoCurrencyTask
    from_currency: Currency
    to_currency: Currency
