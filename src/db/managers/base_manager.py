from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio.session import _AsyncSessionContextManager, async_sessionmaker
from sqlalchemy.orm import close_all_sessions

T = TypeVar('T')


@dataclass(frozen=True)
class Omitted:
    pass

    def __bool__(self) -> bool:
        return False


Omittable = Union[T, Omitted]
OMITTED = Omitted()


class BaseDBManager:
    def __init__(self, async_engine: AsyncEngine):
        self._async_engine = async_engine
        self._async_session = async_sessionmaker(
            self._async_engine,
            expire_on_commit=False,
        )

    def session(self) -> _AsyncSessionContextManager[AsyncSession]:
        return self._async_session.begin()

    @asynccontextmanager
    async def use_or_create_session(
        self,
        current_session: AsyncSession | None,
    ) -> AsyncIterator[AsyncSession]:
        async with AsyncExitStack() as stack:
            if current_session is None:
                session = await stack.enter_async_context(self.session())
            else:
                session = current_session

            yield session

    async def close(self) -> None:
        close_all_sessions()
        await self._async_engine.dispose()
