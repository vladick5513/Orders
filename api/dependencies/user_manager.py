from authentication.user_manager import UserManager
from api.dependencies.users import get_user_db
from fastapi import Depends

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)