from api.dependencies.fastapi_users import fastapi_users
from fastapi import APIRouter
from src.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])
#/me
#/{id}
router.include_router(router=fastapi_users.get_users_router(UserRead, UserUpdate))