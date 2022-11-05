from telethon.sync import TelegramClient, events
from common.exceptions.telegram import *
from domain.enum_class.Errors import Errors
from domain.named_tuple.UserServiceData import TelegramUserData
from utils.logging import logger
from app.functions.messages import Messages


class Telegram:

	def __init__(self, client: TelegramClient, messages: Messages) -> None:
		try:
			self.client = client
			self.messages = messages

			logger.info("Успешное подключение к telegram api")
		except Exception as e:
			logger.error(e)
			raise ErrConnectTelegram(Errors.CONNECT_TELEGRAM.value)


	async def check_new_messages(self) -> None:
		try:
			logger.info('Началась проверка на новые сообщения в Телеграм')

			@self.client.on(events.NewMessage())
			async def handler(event):
				self.messages.new_telegram_message(event.message.to_dict())

			await self.client.start()
			await self.client.run_until_disconnected()
		except Exception as e:
			logger.error(e)
			raise ErrGetNewTelegramMessages(Errors.GET_NEW_TELEGRAM_MESSAGES.value)


	def send_message(self, user_id: int, message: str) -> None:
		pass

		
	def get_user_data_by_id(self, user_id: int) -> TelegramUserData:
		pass