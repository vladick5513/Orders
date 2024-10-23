import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.database import Base
from src.config import settings
from sqlalchemy.orm import sessionmaker
from typing import Generator, Any
from asyncio import AbstractEventLoop
from asyncio import get_event_loop_policy


async_engine_test = create_async_engine(
    url=settings.DATABASE_URL_TEST_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_session_factory_test = async_sessionmaker(
    async_engine_test,
    expire_on_commit=False
)

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_session():
    async with async_session_factory_test() as session:
        yield session

@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator["AbstractEventLoop", Any, None]:
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()