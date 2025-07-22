from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class WhitebirdFee(BaseModel):
    asset: str | None
    network: Decimal | None
    service: Decimal | None
    total: Decimal | None


class WhitebirdCryptoTransaction(BaseModel):
    hash: str


class WhitebirdClient(BaseModel):
    client_id: str = Field(alias='clientId')

    class Config:
        allow_population_by_field_name = True


class WhitebirdCurrencyPair(BaseModel):
    from_currency: str = Field(alias='fromCurrency')
    to_currency: str = Field(alias='toCurrency')

    class Config:
        allow_population_by_field_name = True


class WhitebirdExchangeOperation(BaseModel):
    bonus_output_asset: Decimal = Field(alias='bonusOutputAsset')
    currency_pair: WhitebirdCurrencyPair = Field(alias='currencyPair')
    exchange_fee_asset_in_fiat: Decimal = Field(alias='exchangeFeeAssetInFiat')
    input_asset: Decimal = Field(alias='inputAsset')
    output_asset: Decimal = Field(alias='outputAsset')
    plain_ratio: Decimal = Field(alias='plainRatio')
    ratio: Decimal = Field(alias='ratio')

    class Config:
        allow_population_by_field_name = True


class WhitebirdFiatTransaction(BaseModel):
    currency: str
    internal_token: str = Field(alias='internalToken')
    link: str
    order_identity: str = Field(alias='orderIdentity')
    payment_token: str | None = Field(alias='paymentToken')
    payment_type: str = Field(alias='paymentType')
    processing_bank: str = Field(alias='processingBank')
    provider_type: str = Field(alias='providerType')
    result_message: str = Field(alias='resultMessage')
    status: str

    class Config:
        allow_population_by_field_name = True


class WhitebirdOrderResponse(BaseModel):
    client: WhitebirdClient
    completion_date: datetime | None = Field(alias='completionDate')
    creation_date: datetime = Field(alias='creationDate')
    crypto_transaction: WhitebirdCryptoTransaction | None = Field(alias='cryptoTransaction')
    exchange_operation: WhitebirdExchangeOperation = Field(alias='exchangeOperation')
    exchange_type: str = Field(alias='exchangeType')
    expires_at_date: datetime = Field(alias='expiresAtDate')
    fiat_transaction: WhitebirdFiatTransaction | None = Field(alias='fiatTransaction')
    from_source: str = Field(alias='fromSource')
    id: str
    merchant_bonus: Decimal = Field(alias='merchantBonus')
    merchant_name: str = Field(alias='merchantName')
    modification_date: datetime = Field(alias='modificationDate')
    number: int
    operation_type: str = Field(alias='operationType')
    order_type: str = Field(alias='orderType')
    promo_code_details: str | None = Field(alias='promoCodeDetails')
    result_message: str = Field(alias='resultMessage')
    server_date: datetime = Field(alias='serverDate')
    status: str
    submit_by_resident: bool = Field(alias='submitByResident')
    to_source: str = Field(alias='toSource')
    type: str

    class Config:
        allow_population_by_field_name = True


class WhitebirdAsset(BaseModel):
    amount: Decimal | None = None
    code: str
    id: str | None = None
    network: str | None = None
    protocol: str | None = None

    class Config:
        allow_population_by_field_name = True


class WhitebirdLimitResponse(BaseModel):
    asset: WhitebirdAsset
    max: Decimal
    min: Decimal

    class Config:
        allow_population_by_field_name = True


class WhitebirdAssetsResponse(BaseModel):
    crypto_assets: List[WhitebirdAsset] = Field(alias='cryptoAssets')
    crypto_currencies: List[WhitebirdAsset] = Field(alias='cryptoCurrencies')
    fiat_assets: List[WhitebirdAsset] = Field(alias='fiatAssets')
    fiat_currencies: List[WhitebirdAsset] = Field(alias='fiatCurrencies')

    class Config:
        allow_population_by_field_name = True


class WhitebirdBuyResponse(BaseModel):
    creation_date: datetime = Field(alias='creationDate')
    crypto_transaction: WhitebirdCryptoTransaction | None = Field(alias='cryptoTransaction')
    expires_at_date: datetime | None = Field(alias='expiresAtDate')
    fiat_payment_link: str = Field(alias='fiatPaymentLink')
    id: str
    modification_date: datetime = Field(alias='modificationDate')
    status: str
    type: str

    class Config:
        allow_population_by_field_name = True


class WhitebirdSellResponse(BaseModel):
    creation_date: datetime = Field(alias='creationDate')
    crypto_transaction: WhitebirdCryptoTransaction | None = Field(alias='cryptoTransaction')
    deposit_crypto_address: str = Field(alias='depositCryptoAddress')
    expires_at_date: datetime | None = Field(alias='expiresAtDate')
    id: str
    modification_date: datetime = Field(alias='modificationDate')
    status: str
    type: str

    class Config:
        allow_population_by_field_name = True


class WhitebirdQuoteResponse(BaseModel):
    expiration_date: datetime = Field(alias='expirationDate')
    fee: WhitebirdFee | None
    plain_rate: Decimal = Field(alias='plainRate')
    quote_id: str = Field(alias='quoteId')
    rate: Decimal

    class Config:
        allow_population_by_field_name = True


class WhitebirdClientStatusResponse(BaseModel):
    id: str
    status: str

    class Config:
        allow_population_by_field_name = True


class WhitebirdClientRegistrationRequest(BaseModel):
    email: str
    first_name_ru: str = Field(alias='firstNameRu')
    last_name_ru: str = Field(alias='lastNameRu')
    patronymic_ru: str = Field(alias='patronymicRu')
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    residence: str
    place_of_birth: str = Field(alias='placeOfBirth')
    birth_date: str = Field(alias='birthDate')
    nationality: str
    registration_country: str = Field(alias='registrationCountry')
    registration_region: str = Field(alias='registrationRegion')
    registration_city: str = Field(alias='registrationCity')
    registration_street: str = Field(alias='registrationStreet')
    registration_house_and_flat: str = Field(alias='registrationHouseAndFlat')
    identity_doc_type: str = Field(alias='identityDocType')
    identity_doc_issue_date: str = Field(alias='identityDocIssueDate')
    identity_doc_expire_date: str = Field(alias='identityDocExpireDate')
    identity_doc_number: str = Field(alias='identityDocNumber')
    personal_number: str = Field(alias='personalNumber')
    post_code: str = Field(alias='postCode')
    phone: str
    gender: str
    residence_district: str = Field(alias='residenceDistrict')
    identity_doc_issuer: str = Field(alias='identityDocIssuer')

    class Config:
        allow_population_by_field_name = True
