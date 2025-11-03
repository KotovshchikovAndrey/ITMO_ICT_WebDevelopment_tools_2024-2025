import asyncio
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    async_scoped_session,
    create_async_engine,
    AsyncSession,
)


class SQLConnection:
    def __init__(self, database_uri: str):
        self._engine = create_async_engine(url=database_uri, echo=True)

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autocommit=False,
        )

    def get_session(self) -> async_scoped_session[AsyncSession]:
        session = async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=asyncio.current_task,
        )

        return session

    async def close(self) -> None:
        await self._engine.dispose()
