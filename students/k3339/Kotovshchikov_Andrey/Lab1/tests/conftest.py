import asyncio
from typing import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from faker import Faker
from httpx import ASGITransport, AsyncClient


@pytest.fixture(scope="session")
def faker() -> Faker:
    return Faker()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    from main import app

    async with LifespanManager(app), AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
