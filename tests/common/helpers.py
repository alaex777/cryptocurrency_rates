from typing import Any


def return_or_raise(v: Any) -> Any:
    if isinstance(v, Exception):
        raise v
    return v
