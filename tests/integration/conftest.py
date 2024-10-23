import pytest
from httpx import AsyncClient
from src.config import settings
from src.main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=settings.DATABASE_URL_TEST_asyncpg) as ac:
        yield ac

