import os

from dotenv import load_dotenv
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from sqlalchemy.sql import func

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)


Async_DATABASE_URL = os.getenv("DATABASE_URL")
async_engine = create_async_engine(Async_DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)


Base = declarative_base(cls=PreBase)


class Users(Base):
    reg_date = Column(DateTime(timezone=False), server_default=func.now())
    tg_id = Column(BigInteger, unique=True)
    username = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)
    is_white = Column(Boolean, default=False)
    hashed_password = Column(String)
