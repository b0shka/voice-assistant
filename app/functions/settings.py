from common.states import states
from domain.enum_class.Errors import Errors
from domain.data_class.Contact import Contact
from domain.data_class.Message import Message
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite


class Settings:
	
	def __init__(self) -> None:
		self.db = DatabaseSQLite()

	
	def say_error(self, error: Errors) -> None:
		synthesis_text(error.value)


	def update_contacts(self, isLauch: bool = False) -> None:
		'''Добавление контактов в глобальное состояние'''

		try:
			contacts = self.db.get_contacts()
			if isinstance(contacts, Errors):
				self.say_error(contact)

			converted_contacts = []
			for contact in contacts:
				convert_contact = Contact(
					id = contact[0],
					first_name = contact[1],
					last_name = contact[2],
					phone = contact[3],
					telegram_id = contact[4],
					vk_id = contact[5],
					email = contact[6]
				)
				converted_contacts.append(convert_contact)

			states.CONTACTS = convert_contact
			if not isLauch:
				synthesis_text('Контакты успешно обновлены')

		except Exception as e:
			self.say_error(Errors.UPDATE_CONTACT)
			logger.error(e)


	def update_notifications(self, isLauch: bool = False) -> None:
		'''Добавление уведомлений (если такие существуют) в глобальное состояние'''

		try:
			telegram_messages = self.db.get_telegram_messages()
			if isinstance(telegram_messages, Errors):
				self.say_error(telegram_messages)
			else:
				for message in telegram_messages:
					states.NOTIFICATIONS.telegram_messages.append(
						self.get_message_object(message)
					)

			vk_messages = self.db.get_vk_messages()
			if isinstance(vk_messages, Errors):
				self.say_error(vk_messages)
			else:
				for message in vk_messages:
					states.NOTIFICATIONS.vk_messages.append(
						self.get_message_object(message)
					)
				
			if not isLauch:
				synthesis_text('Уведомления успешно обновлены')

		except Exception as e:
			self.say_error(Errors.UPDATE_NOTIFICATIONS)
			logger.error(e)


	def get_message_object(self, message: list) -> Message:
		return Message(
			text = message[1],
			contact_id = message[2],
			from_id = message[3],
			first_name = message[4],
			last_name = message[5]
		)