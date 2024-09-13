from typing import TYPE_CHECKING

import src.config
from api.dependencies.access_tokens import get_access_token_db
from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy


if TYPE_CHECKING:
    from src.models import AccessToken

def get_database_strategy(
    access_token_db: AccessTokenDatabase["AccessToken"] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=src.config.settings.ACCESS_TOKEN_LIFETIME
    )