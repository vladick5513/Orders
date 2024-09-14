
from api.dependencies.backend import authentication_backend
from fastapi_users import FastAPIUsers

from src.models import User
from api.dependencies.user_manager import get_user_manager
from src.types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)