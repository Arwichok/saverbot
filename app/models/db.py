from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


async def init_session(db_url: str):
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
