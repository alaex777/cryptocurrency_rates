from typing import Any


class BaseError(Exception):
    def __init__(
        self,
        description: str | None = None,
        result_code: str | None = None,
        *args: Any,
        extra: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(*args)
        self.result_code = result_code or self.result_code
        self.description = description or self.description
        self.extra = extra or self.extra

    result_code: str | None = 'error'
    description: str | None = 'unknown error'
    extra: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            'description': self.description,
            'result_code': self.result_code,
            **(self.extra or {}),
        }


INVALID_ACCESS_TOKEN = dict(
    result_code='invalid_access_token',
    description='Could not evaluate provided access token',
)

INVALID_TOKEN = dict(
    result_code='invalid_token',
    description='Provided token is no longer valid, request a new one.',
)
