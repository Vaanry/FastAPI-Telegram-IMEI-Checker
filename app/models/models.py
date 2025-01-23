from sqlalchemy import BigInteger, Boolean, Column, DateTime, String
from sqlalchemy.sql import func

from app.backend.back_config import Base


class Users(Base):
    reg_date = Column(DateTime(timezone=False), server_default=func.now())
    tg_id = Column(BigInteger, unique=True)
    username = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)
    is_white = Column(Boolean, default=False)
    hashed_password = Column(String)
