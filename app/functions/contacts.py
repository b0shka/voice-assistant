from common.states import states
from common.exceptions.contacts import ErrConvertContacts
from common.exceptions.database import ErrGetContacts
from domain.enum_class.Errors import Errors
from domain.named_tuple.Contact import Contact
from domain.repository.database_sqlite import DatabaseSQLite
from utils.speech.yandex_synthesis import synthesis_text
from app.functions.communications import say_error


class Contacts:
	
	def __init__(self, db: DatabaseSQLite) -> None:
		self.db = db


	def update_contacts(self, isLauch: bool = False) -> None:
		'''Добавление контактов в глобальное состояние'''

		try:
			contacts = self.db.get_contacts()
			converted_contacts = self._convert_contacts(contacts)
		except (ErrGetContacts, ErrConvertContacts) as e:
			say_error(e)
		else:
			states.CONTACTS = converted_contacts
			
			if not isLauch:
				synthesis_text('Контакты успешно обновлены')


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

			return converted_contacts
		except IndexError:
			raise ErrConvertContacts(Errors.CONVERT_CONTACTS)