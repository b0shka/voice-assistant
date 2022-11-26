from telethon.sync import TelegramClient, events
from utils.logging import logger
from common.states import states
from common.exceptions.messages import CantGetUserData
from common.exceptions.contacts import CantFoundContact
from common.exceptions.database import ErrAddTelegramMessage
from domain.enum_class.Errors import Errors
from domain.named_tuple.Message import Message
from domain.named_tuple.Contact import Contact
from domain.named_tuple.UserServiceData import TelegramUserData
from app.functions.messages import Messages
from app.functions.communications import say_error


class Telegram:

	def __init__(self, client: TelegramClient, messages: Messages) -> None:
		try:
			self.client = client
			self.messages = messages

			logger.info("Успешное подключение к telegram api")
		except Exception as e:
			logger.error(e)
			say_error(Errors.CONNECT_TELEGRAM.value)


	def _get_contact_by_from_id(self, id: int) -> Contact:
		for contact in states.CONTACTS:
			if contact.telegram_id == id:
				return contact
		else:
			raise CantFoundContact

	
	async def check_new_messages(self) -> None:
		'''Мониторинг новых входящих сообщений в Телеграм'''

		logger.info('Началась проверка на новые сообщения в Телеграм')
		
		try:
			@self.client.on(events.NewMessage(incoming=True))
			async def handler(event):
				try:
					await self.processing_new_message(event.message.to_dict())
				except Exception as e:
					logger.error(e)
					say_error(Errors.PROCESSING_NEW_TELEGRAM_MESSAGES.value)

			await self.client.start()
			await self.client.run_until_disconnected()

		except Exception as e:
			logger.error(e)
			say_error(Errors.MONITORING_NEW_TELEGRAM_MESSAGES.value)


	async def processing_new_message(self, message: dict) -> None:
		try:
			id = message['id']
			text = message['message']
			date = message['date']

			match message['peer_id']['_']:
				case 'PeerUser':
					user_id = int(message['peer_id']['user_id'])

					try:
						contact = self._get_contact_by_from_id(user_id)
						new_message = Message(
							text = text,
							from_id = user_id,
							contact_id = contact.id,
							first_name = contact.first_name,
							last_name = contact.last_name
						)

						self.messages.new_telegram_message_from_contact(new_message, contact)

					except CantFoundContact:
						# сообщение не от контакта
						try:
							user = await self._get_user_data_by_id(user_id)
						except CantGetUserData as e:
							say_error(e)
						else:
							new_message = Message(
								text = text, 
								from_id = user_id,
								first_name = user.first_name,
								last_name = user.last_name
							)

							self.messages.new_telegram_message_from_user(new_message, user)

				case 'PeerChat':
					chat_id = int(message['peer_id']['chat_id'])
					user_id = int(message['from_id']['user_id'])
					print(f'[CHAT MESSAGE {chat_id} от {user_id}] {id}: {text} ({date})')

				case 'PeerChannel':
					channel_id = int(message['peer_id']['channel_id'])
					print(f'[CHANNEL MESSAGE {channel_id}] {id}: {text} ({date})')

		except KeyError:
			say_error(Errors.TELEGRAM_MESSAGE_KEY_IS_EMPTY.value)

		except ValueError:
			say_error(Errors.TELEGRAM_INVALID_USER_ID.value)

		except ErrAddTelegramMessage as e:
			say_error(e)


	def send_message(self, user_id: int, message: str) -> None:
		pass

		
	async def _get_user_data_by_id(self, user_id: int) -> TelegramUserData:
		try:
			user_data = await self.client.get_entity(user_id)
			return TelegramUserData(
				id = user_data.id,
				first_name = user_data.first_name,
				last_name = user_data.last_name,
			)
		except Exception as e:
			logger.error(e)
			raise CantGetUserData(Errors.GET_USER_DATA_TELEGRAM_BY_ID.value)