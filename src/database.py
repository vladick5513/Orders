from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import URL, create_engine, text, String
from src.config import settings

Base = declarative_base()

# sync_engine = create_engine(
#     url=settings.DATABASE_URL_psycopg,
#     echo= True,
#     pool_size=5,
#     max_overflow=10
# )

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

#session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

def get_db():
    db = async_session_factory()
    try:
        yield db
    finally:
        db.close()




