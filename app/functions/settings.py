from common.states import states
from common.exceptions.settings import ErrConvertContacts, ErrConvertMessage
from common.exceptions.database import ErrGetContacts, ErrGetTelegramMessages, ErrGetVKMessages
from domain.enum_class.Errors import Errors
from domain.named_tuple.Contact import Contact
from domain.named_tuple.Message import Message
from utils.speech.yandex_synthesis import synthesis_text
from data.database_sqlite import DatabaseSQLite
from app.functions.communications import say_error


class Settings:
	
	def __init__(self) -> None:
		self.db = DatabaseSQLite()


	def update_contacts(self, isLauch: bool = False) -> None:
		'''Добавление контактов в глобальное состояние'''

		try:
			contacts = self.db.get_contacts()
			converted_contacts = self._convert_contacts(contacts)
			states.CONTACTS = converted_contacts
			
			if not isLauch:
				synthesis_text('Контакты успешно обновлены')

		except (ErrGetContacts, ErrConvertContacts) as e:
			say_error(e)


	def _convert_contacts(self, contacts: list) -> list[Contact]:
		try:
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

			return convert_contact
		except IndexError:
			raise ErrConvertContacts(Errors.CONVERT_CONTACT)


	def update_notifications(self, isLauch: bool = False) -> None:
		'''Добавление уведомлений (если такие существуют) в глобальное состояние'''

		self._update_telegram_messages()
		self._update_vk_messages()
			
		if not isLauch:
			synthesis_text('Уведомления успешно обновлены')


	def _update_vk_messages(self) -> None:
		try:
			vk_messages = self.db.get_vk_messages()

			for message in vk_messages:
				states.NOTIFICATIONS.vk_messages.append(
					self._convert_message(message)
				)

		except (ErrGetVKMessages, ErrConvertMessage) as e:
			say_error(e)


	def _update_telegram_messages(self) -> None:
		try:
			telegram_messages = self.db.get_telegram_messages()

			for message in telegram_messages:
				states.NOTIFICATIONS.telegram_messages.append(
					self._convert_message(message)
				)

		except (ErrGetTelegramMessages, ErrConvertMessage) as e:
			say_error(e)


	def _convert_message(self, message: list) -> Message:
		try:
			return Message(
				text = message[1],
				contact_id = message[2],
				from_id = message[3],
				first_name = message[4],
				last_name = message[5]
			)

		except IndexError:
			raise ErrConvertMessage(Errors.CONVERT_MESSAGE)
