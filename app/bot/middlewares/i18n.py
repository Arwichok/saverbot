from typing import Tuple, Any, Optional

from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware


class I18nMiddleware(BaseI18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        data = args[-1]
        data["_"] = self.gettext
        if user := data.get("db_user"):
            return user.language or self.default
        return self.default
