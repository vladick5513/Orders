from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr
from sqlalchemy import URL, create_engine, text, String, MetaData
from src.config import settings, naming_convention
from src.utils.case_converter import camel_case_to_snake_case

class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Преобразование CamelCase в snake_case для таблиц
        return f"{camel_case_to_snake_case(cls.__name__)}s"


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_session_factory = async_sessionmaker(async_engine)

async def get_db():
    db = async_session_factory()
    try:
        yield db
    finally:
        await db.close()




