from environs import Env


env = Env()
env.read_env('.env')

VK_TOKEN = env.str("VK_TOKEN")
PATH_FILE_DB = env.str("PATH_FILE_DB")
PATH_FILE_SESSION_TELEGRAM = env.str("PATH_FILE_SESSION_TELEGRAM")
TELEGRAM_API_ID = env.int("TELEGRAM_API_ID")
TELEGRAM_API_HASH = env.str("TELEGRAM_API_HASH")