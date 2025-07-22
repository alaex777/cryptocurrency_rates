import logging
from contextvars import ContextVar
from typing import Any, Dict, TypeVar

T = TypeVar('T')


class LogContextBinder(logging.Filter):
    def __init__(self, name: str = '') -> None:
        super().__init__(name)
        self._tracking: Dict[str, ContextVar[Any]] = {}

    def bind(self, var: ContextVar[T], attr_name: str | None = None) -> ContextVar[T]:
        if attr_name is None:
            attr_name = var.name

        if attr_name in self._tracking:
            raise ValueError('Duplicated attr_name of bound ContextVar')

        self._tracking[attr_name] = var
        return var

    def filter(self, record: logging.LogRecord) -> bool:
        for attr_name, ctx_var in self._tracking.items():
            if hasattr(record, attr_name):
                continue

            try:
                value = ctx_var.get()
            except LookupError:
                pass
            else:
                setattr(record, attr_name, value)

        return True


LOG_CONTEXT_BINDER = LogContextBinder()
