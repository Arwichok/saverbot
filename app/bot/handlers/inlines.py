from aiogram import Dispatcher
from aiogram.types import InlineQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.utils.results import get_results
from app.models.message import Message
from app.models.user import User
from app.bot.utils.constants import CONTENT_TYPES


async def search(iq: InlineQuery, session: AsyncSession, db_user: User):
    # Get content type by query or user default type
    content_type = CONTENT_TYPES.get(iq.query, db_user.default_type)
    # Get messages by content type
    messages = (await session.execute(select(Message).where(
        Message.uid == iq.from_user.id,
        Message.type == content_type,
    ))).scalars().all()
    # Write to `results` list of results by content type
    results = get_results(content_type, messages)
    await iq.answer(results, cache_time=1)


def register(dp: Dispatcher):
    dp.register_inline_handler(search)
