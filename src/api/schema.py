from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BaseJSONRequest(BaseModel):
    headers: BaseModel = Field(default_factory=BaseModel)
    query: BaseModel = Field(default_factory=BaseModel)
    text: str | None
    body: BaseModel = Field(default_factory=BaseModel)
    match_info: BaseModel = Field(default_factory=BaseModel)


class GetCryptoCurrencyRateRequestQuery(BaseModel):
    from_currency: str = Field(alias='from')
    to_currency: str = Field(alias='to')
    amount: Decimal
    timestamp: datetime | None = None

    class Config:
        allow_population_by_field_name = True


class GetCryptoCurrencyRateRequest(BaseJSONRequest):
    query: GetCryptoCurrencyRateRequestQuery
