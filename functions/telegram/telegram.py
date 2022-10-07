from telethon.sync import TelegramClient, events
from common.config import *


class Telegram:

	def __init__(self):
		try:
			self.client = TelegramClient(
				PATH_FILE_SESSION_TELEGRAM, 
				TELEGRAM_API_ID, 
				TELEGRAM_API_HASH
			)
			logger.info("Success connect telegram api")
		except Exception as e:
			logger.error(e)