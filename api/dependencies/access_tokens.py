from src.database import get_db
from typing import TYPE_CHECKING

from fastapi import Depends
from src.models import AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: "AsyncSession" = Depends(get_db),
):
    yield AccessToken.get_db(session=session)