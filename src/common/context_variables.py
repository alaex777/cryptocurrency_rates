from contextvars import ContextVar
from typing import Any

from src.common.context_binder import LOG_CONTEXT_BINDER

REQUEST_ID: ContextVar[str] = LOG_CONTEXT_BINDER.bind(ContextVar('REQUEST_ID'))
REQUEST_PARAMS: ContextVar[dict[str, Any]] = LOG_CONTEXT_BINDER.bind(ContextVar('REQUEST_PARAMS'))
TASK_DATA: ContextVar[dict[str, Any]] = LOG_CONTEXT_BINDER.bind(ContextVar('TASK_DATA'))
