import logging

from sqlalchemy import Column, Integer, String
import aiogram.types as atp
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    default_type = Column(String, default=atp.ContentType.TEXT)

    @classmethod
    async def create(cls, session: AsyncSession, tg_user: atp.User):
        db_user = await session.get(cls, tg_user.id)
        if not db_user:
            db_user = cls(id=tg_user.id, name=tg_user.full_name)
            session.add(db_user)
            logging.info(f"New user {tg_user.full_name}({tg_user.id})")
            await session.commit()
        return db_user
