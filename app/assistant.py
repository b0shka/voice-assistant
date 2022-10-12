import time
from database.database_sqlite import DatabaseSQLite
from utils.speech.synthesizer import say
from common.errors import *
from utils.logging import logger
from handlers.handlers import Handlers


class Assistant:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.db.create_tables()
			self.handlers = Handlers()

			self.contacts = self.db.get_contacts()
			self.telegram_messages = self.db.get_telegram_messages()
			self.vk_messages = self.db.get_vk_messages()
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			while True:
				request = input('Enter: ')
				self.handlers.processing(request)

				result = self.db.add_request_answer_assistant(request, 'request')
				if result == 0:
					logger.error(ERROR_ADD_REQUEST_ANSWER)
		except Exception as e:
			logger.error(e)


	def monitoring(self):
		try:
			while True:
				telegram_messages = self.db.get_telegram_messages()
				if telegram_messages == 0:
					logger.error(ERROR_GET_TELEGRAM_MESSAGES)

				vk_messages = self.db.get_vk_messages()
				if vk_messages == 0:
					logger.error(ERROR_GET_VK_MESSAGES)

				if len(telegram_messages):
					answer = f'У вас {len(telegram_messages)} сообщений в Телеграм'
					#say(answer)

				if len(vk_messages):
					answer = f'У вас {len(vk_messages)} сообщений в Вконтакте'
					#say(answer)

				self.last_requests_answers = self.db.get_requests_answers()
				if len(self.last_requests_answers) > 10:
					requests_answer = self.last_requests_answers[::-1]
					result = self.db.delete_old_requests_answer(requests_answer[10:])
					if result == 0:
						logger.error(ERROR_CLEAN_OLD_REQUESTS_ANSWERS)

				time.sleep(5)
		except Exception as e:
			logger.error(e)
