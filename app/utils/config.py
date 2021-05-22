from pathlib import Path

from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
DB_URL = env("DB_URL")
OWNER_ID = env("OWNER_ID", 0)
I18N_DOMAIN = env("BOT_DOMAIN", "saver")
BASE_DIR = Path(__file__).parent.parent.parent
LOCALES_DIR = BASE_DIR / env("LOCALES_DIR", "locales")
