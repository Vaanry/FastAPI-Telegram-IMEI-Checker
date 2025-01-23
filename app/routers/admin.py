from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.db_depends import get_db
from app.models import Users
from app.utils import check_admin_permissions

from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.patch("/update_user_status/")
async def update_user_status(
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
    username: str,
):
    """Добавление/удаление пользователя в белый список"""
    await check_admin_permissions(get_user)
    is_white = await db.scalar(select(Users.is_white).where(Users.username == username))

    new_status = not is_white

    await db.execute(
        update(Users).where(Users.username == username).values(is_white=new_status)
    )
    await db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "User's stutus has been updated",
    }
