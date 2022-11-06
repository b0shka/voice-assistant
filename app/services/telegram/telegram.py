from telethon.sync import TelegramClient, events
from utils.logging import logger
from common.states import states
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
			say_error(Errors.CONNECT_TELEGRAM)


	def _get_contact_by_from_id(self, id: int) -> Contact:
		for contact in states.CONTACTS:
			if contact.telegram_id == id:
				return contact
		else:
			raise CantFoundContact

	
	async def check_new_messages(self) -> None:
		try:
			logger.info('Началась проверка на новые сообщения в Телеграм')

			@self.client.on(events.NewMessage(incoming=True))
			async def handler(event):
				self.processing_new_message(event.message.to_dict())

			await self.client.start()
			await self.client.run_until_disconnected()

		except Exception as e:
			logger.error(e)
			say_error(Errors.GET_NEW_TELEGRAM_MESSAGES)


	def processing_new_message(self, message: dict) -> None:
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

						try:
							self.messages.new_telegram_message(new_message, contact)
						except ErrAddTelegramMessage as e:
							say_error(e)

					except CantFoundContact:
						# сообщение не от контакта
						pass

				case 'PeerChat':
					chat_id = int(message['peer_id']['chat_id'])
					user_id = int(message['from_id']['user_id'])
					print(f'[CHAT MESSAGE {chat_id} от {user_id}] {id}: {text} ({date})')

				case 'PeerChannel':
					channel_id = int(message['peer_id']['channel_id'])
					print(f'[CHANNEL MESSAGE {channel_id}] {id}: {text} ({date})')

		except KeyError:
			say_error(Errors.TELEGRAM_MESSAGE_KEY_IS_EMPTY)

		except ValueError:
			say_error(Errors.TELEGRAM_INVALID_USER_ID)


	def send_message(self, user_id: int, message: str) -> None:
		pass

		
	def get_user_data_by_id(self, user_id: int) -> TelegramUserData:
		pass