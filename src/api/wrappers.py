import logging
from functools import wraps
from typing import Awaitable, Callable, Type, TypeVar

from aiohttp import web
from mypy_extensions import Arg
from pydantic import ValidationError

from src.api.errors import BaseError
from src.api.schema import BaseJSONRequest
from src.common.context_variables import REQUEST_ID, REQUEST_PARAMS
from src.common.helpers import json_loads, str_uuid

H = TypeVar('H', bound=BaseJSONRequest)
V = TypeVar('V')

logger = logging.getLogger(__name__)


def http_api_method_wrapper(schema: Type[H]) -> Callable[
    [Callable[[V, H], Awaitable[web.Response]]],
    Callable[[Arg(V, 'cls'), web.Request], Awaitable[web.Response]],  # noqa: F821
]:

    def decorator(
        api_method: Callable[[V, H], Awaitable[web.Response]],
    ) -> Callable[[Arg(V, 'cls'), web.Request], Awaitable[web.Response]]:  # noqa: F821

        @wraps(api_method)
        async def wrapper(cls: V, request: web.Request, client_id: str | None = None) -> web.Response:
            REQUEST_ID.set(str_uuid())
            request_text = await request.text()
            try:
                json_body = json_loads(request_text)
            except ValueError:
                json_body = {}
            request_combined = {
                'headers': {**request.headers},
                'query': {**request.query},
                'body': json_body,
                'text': request_text,
                'match_info': {**request.match_info},
            }

            try:
                request_as_schema = schema.model_validate(request_combined)
                REQUEST_PARAMS.set(request_as_schema.model_dump())
                if client_id is None:
                    result = await api_method(cls, request_as_schema)  # type: ignore
                else:
                    result = await api_method(cls, request_as_schema, client_id=client_id)  # type: ignore
                logger.info(
                    f'receive request for {api_method.__name__} with {request_as_schema.model_dump()=}, {request_combined=}',  # noqa
                )
            except ValidationError as e:
                logger.exception(f'failed to validate {api_method.__name__} request with {request_combined=}')
                result = web.json_response(text=e.json(), status=400)
            except BaseError as e:
                logger.info(f'during {api_method.__name__} an error occurred', exc_info=True)
                result = web.json_response(
                    data=e.to_dict(),
                    status=400,
                )
            except Exception:
                logger.exception(f'during {api_method.__name__} unknown exception occurred, {request_combined=}')
                result = web.json_response(
                    data={
                        'result_code': 'error',
                        'description': 'unknown_error',
                    },
                    status=500,
                )

            logger.info(f'response {api_method.__name__} with {result=}')
            return result

        return wrapper

    return decorator
