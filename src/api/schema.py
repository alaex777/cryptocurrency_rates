from pydantic import BaseModel, Field


class BaseJSONRequest(BaseModel):
    headers: BaseModel = Field(default_factory=BaseModel)
    query: BaseModel = Field(default_factory=BaseModel)
    text: str | None
    body: BaseModel = Field(default_factory=BaseModel)
    match_info: BaseModel = Field(default_factory=BaseModel)


class GetCryptoCurrencyRateRequestQuery(BaseModel):
    from_currency: str
    to_currency: str


class GetCryptoCurrencyRateRequest(BaseJSONRequest):
    query: GetCryptoCurrencyRateRequestQuery
