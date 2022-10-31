from random import choice
from common.errors import *
from common.states import states
from domain.data_class.Contact import Contact
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite


class Communications:

	def __init__(self):
		self.db = DatabaseSQLite()


	def exit(self) -> int:
		exit_answer = ('До скорой встречи', 'До свидания', 'Всего хорошего', 'Удачи', 'Всего доброго', 'Счастл+иво оставаться')
		synthesis_text(choice(exit_answer))
		return 0


	def nothing_found(self):
		not_found_answer = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
		synthesis_text(choice(not_found_answer))


	def waiting_select_action(self):
		synthesis_text('Какое действие вы хотите выполнить?')

	
	def action_not_found_in_topic(self):
		synthesis_text('В этой теме нет такого действия')
		states.WAITING_RESPONSE = False


	def update_contacts(self):
		try:
			###
			contacts = self.db.get_contacts()
			if contacts == 0:
				logger.error(ERROR_GET_CONTACTS)

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
			synthesis_text('Контакты успешно обновлены')
		except Exception as e:
			logger.error(e)
			synthesis_text('Ошибка при обновлении контактов')

	
	def error(self):
		synthesis_text('Произошла ошибка')