from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.requests import Request
from fastapi.security import HTTPBasic, OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models import Users
from app.schemas import CreateUser

from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


async def authanticate_user(
    db: Annotated[AsyncSession, Depends(get_db)], user_data: CreateUser
):
    user = await db.scalar(select(Users).where(Users.username == user_data.username))
    if (
        not user
        or not bcrypt_context.verify(user_data.password, user.hashed_password)
        or user.hashed_password is None
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def create_access_token(
    username: str, id: int, is_admin: bool, expires_delta: timedelta
):

    encode = {"sub": username, "id": id, "is_admin": is_admin}
    expires = datetime.now() + expires_delta
    encode.update({"exp": datetime.timestamp(expires)})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login/")
async def auth_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        user_data = CreateUser(username=username, password=password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")

    check = await authanticate_user(db, user_data)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    access_token = await create_access_token(
        check.username,
        check.id,
        check.is_admin,
        timedelta(weeks=2),
    )
    response.set_cookie(
        key="users_access_token",
        value=access_token,
        httponly=True,
        secure=False,
        path="/",
    )

    return {"access_token": access_token, "token_type": "bearer"}


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен истёк. Пожалуйста, войдите снова.",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не валидный!",
        )

    username: str = payload.get("sub")
    id: int = payload.get("id")
    is_admin: bool = payload.get("is_admin")
    if username is None or id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невозможно проверить пользователя.",
        )

    return {"username": username, "id": id, "is_admin": is_admin}
