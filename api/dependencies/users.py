from typing import TYPE_CHECKING
from fastapi import Depends
from src.database import get_db
from src.models import User


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_db(
        session: "AsyncSession" = Depends(get_db)
):
    yield User.get_db(session=session)
