from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
DB_URL = env("DB_URL")
OWNER_ID = env("OWNER_ID", 0)
