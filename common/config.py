import logging
import os
from dotenv import load_dotenv


load_dotenv()

if not os.path.exists('info'):
	os.mkdir('info')

logging.basicConfig(filename="info/info.log", format = u'[%(levelname)s][%(asctime)s] %(funcName)s:%(lineno)s: %(message)s', level='INFO')
logger = logging.getLogger()

VK_TOKEN = os.getenv("VK_TOKEN")
PATH_FILE_DB = os.getenv("PATH_FILE_DB")
PATH_FILE_SESSION_TELEGRAM = os.getenv("PATH_FILE_SESSION_TELEGRAM")
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
CONTACTS_IDS = []