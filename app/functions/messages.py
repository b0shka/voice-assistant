from common.states import states
from domain.named_tuple.Contact import Contact
from domain.named_tuple.Message import Message
from domain.named_tuple.UserServiceData import VKUserData
from domain.repository.database_sqlite import DatabaseSQLite
from utils.speech.yandex_synthesis import synthesis_text


class Messages:

	def __init__(self, db: DatabaseSQLite) -> None:
		self.db = db


	def new_telegram_message(self, message: Message, contact: Contact) -> None:
		'''Озвучка нового сообщения от контакта в Телеграм'''

		if not states.MUTE:
			answer = f'У вас новое сообщение в Телеграм от контакта {contact.first_name}'
			if contact.last_name:
				answer += f' {contact.last_name}'
			synthesis_text(answer)

		states.NOTIFICATIONS.telegram_messages.append(message)
		self.db.add_telegram_message(message)


	def new_vk_message_from_contact(self, message: Message, contact: Contact) -> None:
		'''Озвучка нового сообщения от контакта в ВКонтакте'''

		if not states.MUTE:
			answer = f'У вас новое сообщение в Вконтакте от контакта {contact.first_name}'
			if contact.last_name:
				answer += f' {contact.last_name}'
			synthesis_text(answer)

		states.NOTIFICATIONS.vk_messages.append(message)
		self.db.add_vk_message(message)


	def new_vk_message_from_user(self, message: Message, user: VKUserData) -> None:
		'''Озвучка нового сообщения от пользователя в ВКонтакте'''

		if not states.get_mute_state():
			answer = f'У вас новое сообщение в Вконтакте от пользователя {user.first_name}'
			if user.last_name:
				answer += f' {user.last_name}'
			synthesis_text(answer)

		states.NOTIFICATIONS.vk_messages.append(message)
		self.db.add_vk_message(message)