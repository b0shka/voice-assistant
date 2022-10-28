from telethon.sync import TelegramClient, events
from common.config import *
from utils.logging import logger
from app.functions.messages import Messages


class Telegram:

	def __init__(self):
		try:
			self.client = TelegramClient(
				PATH_FILE_SESSION_TELEGRAM, 
				TELEGRAM_API_ID, 
				TELEGRAM_API_HASH
			)
			logger.info("Success connect telegram api")

			self.messages = Messages()
		except Exception as e:
			logger.error(e)


	async def check_new_messages(self):
		try:
			logger.info('Start check new messages in Telegram')

			@self.client.on(events.NewMessage())
			async def handler(event):
				self.messages.telegram_message(event.message.to_dict())

			await self.client.start()
			await self.client.run_until_disconnected()
		except Exception as e:
			logger.error(e)


	def send_message(self, user_id, message):
		try:
			pass
		except Exception as e:
			logger.error(e)

		
	def get_user_data_by_id(self, user_id):
		try:
			pass
		except Exception as e:
			logger.error(e)