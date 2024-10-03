import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.database import Base
from src.config import settings

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

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_session(event_loop):
    async with async_session_factory_test() as session:
        yield session
        await session.rollback()
