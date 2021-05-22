from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app.utils import config


Base = declarative_base()


def init_engine():
    return create_async_engine(config.DB_URL)


def init_session(engine):
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
