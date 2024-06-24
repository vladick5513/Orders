from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import URL, create_engine, text, String
from config import settings

Base = declarative_base()

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo= True,
    pool_size=5,
    max_overflow=10
)

# async_engine = create_async_engine(
#     url=settings.DATABASE_URL_asyncpg,
#     echo=True
# )

session_factory = sessionmaker(sync_engine)
#async_session_factory = async_sessionmaker(async_engine)




