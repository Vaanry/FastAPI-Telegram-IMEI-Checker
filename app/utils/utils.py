from fastapi import HTTPException, status


async def check_admin_permissions(user: dict):
    """Проверка, что пользователь является администратором."""
    if not user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be admin user for this",
        )
