from telethon.sync import TelegramClient, events
from common.config import *
from domain.enum_class.Errors import Errors
from utils.logging import logger
from app.functions.messages import Messages


class Telegram:

	def __init__(self) -> None:
		try:
			self.messages = Messages()
			self.client = TelegramClient(
				PATH_FILE_SESSION_TELEGRAM, 
				TELEGRAM_API_ID, 
				TELEGRAM_API_HASH
			)

			logger.info("Успешное подключение к telegram api")
		except Exception as e:
			self.messages.say_error(Errors.CONNECT_TELEGRAM)
			logger.error(e)


	async def check_new_messages(self) -> None:
		try:
			logger.info('Началась проверка на новые сообщения в Телеграм')

			@self.client.on(events.NewMessage())
			async def handler(event):
				self.messages.new_telegram_message(event.message.to_dict())

			await self.client.start()
			await self.client.run_until_disconnected()
		except Exception as e:
			self.messages.say_error(Errors.GET_NEW_TELEGRAM_MESSAGES)
			logger.error(e)


	def send_message(self, user_id: int, message: str) -> None | Errors:
		try:
			pass
		except Exception as e:
			logger.error(e)
			return Errors.SEND_TELEGRAM_MESSAGE

		
	def get_user_data_by_id(self, user_id: int) -> dict | Errors:
		try:
			pass
		except Exception as e:
			logger.error(e)
			return Errors.GET_USER_DATA_TELEGRAM_BY_ID