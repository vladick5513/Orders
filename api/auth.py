from api.dependencies.backend import authentication_backend
from api.dependencies.fastapi_users import fastapi_users
from fastapi import APIRouter
from src.schemas.user import UserRead, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])
#login
#logout
router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend)
)
#register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),

)