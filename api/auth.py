from api.dependencies.backend import authentication_backend
from api.dependencies.fastapi_users import fastapi_users
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from src.schemas.user import UserRead, UserCreate

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])

#/login
#/logout
router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend)
)
#/register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),

)

#/request-verify-token
#/verify
router.include_router(
    router=fastapi_users.get_verify_router(UserRead)
)

#/ forgot-password
#/ reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router()
)