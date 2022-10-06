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


	async def check_new_messages(self):
		try:
			@self.client.on(events.NewMessage())
			async def handler(event):
				message = event.message.to_dict()
				from_id = message['from_id']['user_id']

				if from_id in CONTACTS_IDS:
					print(message['message'])

			await self.client.start()
			await self.client.run_until_disconnected()
		except Exception as e:
			logger.error(e)