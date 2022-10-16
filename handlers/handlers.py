from random import choice
from database.database_sqlite import DatabaseSQLite
#from services.telegram.telegram import Telegram
#from services.vk.vk import VK
#from services.yandex.yandex import Yandex
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text
from common.errors import *
from handlers.list_requests import *


class Handlers:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			#self.telegram = Telegram()
			#self.vk = VK()
			#self.yandex = Yandex()
		except Exception as e:
			logger.error(e)


	def processing(self, command):
		try:
			answer = None

			if 'привет' in command:
				answer = 'привет'
				synthesis_text(answer)

			else:
				not_found_command = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
				synthesis_text(choice(not_found_command))

			result = self.db.add_request_answer_assistant(command, 'request')
			if result == 0:
				logger.error(ERROR_ADD_REQUEST_ANSWER)

			if answer:
				result = self.db.add_request_answer_assistant(answer, 'answer')
				if result == 0:
					logger.error(ERROR_ADD_REQUEST_ANSWER)
		except Exception as e:
			logger.error(e)


	def determinate_action(self):
		try:
			pass
		except Exception as e:
			logger.error(e)