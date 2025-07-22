import uuid
from datetime import date, datetime, timezone
from typing import Any

import ujson
from pydantic.json import pydantic_encoder


def json_dumps_default(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    else:
        return pydantic_encoder(value)


def json_dumps(data: Any) -> str:
    return ujson.dumps(data, ensure_ascii=False, default=json_dumps_default)


def json_loads(data: str) -> dict[Any, Any]:
    return ujson.loads(data)


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def str_uuid() -> str:
    return str(uuid.uuid4())
