from fastapi import APIRouter

from .admin import router as admin_router
from .auth import router as auth_router

main_router = APIRouter()


main_router.include_router(auth_router)
main_router.include_router(admin_router)
