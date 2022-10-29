from random import choice
from common.errors import *
from common.states import states
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite


class Communications:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
		except Exception as e:
			logger.error(e)


	def exit(self):
		try:
			exit_answer = ('До скорой встречи', 'До свидания', 'Всего хорошего', 'Удачи', 'Всего доброго', 'Счастл+иво оставаться')
			synthesis_text(choice(exit_answer))
			return 0
		except Exception as e:
			logger.error(e)
			synthesis_text('Произошла ошибка при выходе')
			return -1


	def nothing_found(self):
		try:
			not_found_answer = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
			synthesis_text(choice(not_found_answer))
		except Exception as e:
			logger.error(e)


	def waiting_select_action(self):
		synthesis_text('Какое действие вы хотите выполнить?')


	def update_contacts(self):
		try:
			contacts = self.db.get_contacts()
			if contacts == 0:
				logger.error(ERROR_GET_CONTACTS)

			states.update_contacts(contacts)
			synthesis_text('Контакты успешно обновлены')
		except Exception as e:
			logger.error(e)