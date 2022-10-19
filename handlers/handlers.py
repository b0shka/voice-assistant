from database.database_sqlite import DatabaseSQLite
from utils.logging import logger
from common.errors import *
from handlers.list_requests import *
from app.functions import notifications, communication


class Handlers:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
		except Exception as e:
			logger.error(e)


	def processing(self, command):
		try:
			if 'уведомления' in command:
				if 'мои' in command or 'посмотреть' in command or 'просмотреть' in command:
					notifications.viewing_notifications()

				elif 'удалить' in command or 'очистить' in command:
					notifications.clean_notifications()

			else:
				communication.nothing_found()

			result = self.db.add_request_answer_assistant(command, 'request')
			if result == 0:
				logger.error(ERROR_ADD_REQUEST_ANSWER)

			#if answer:
			#	result = self.db.add_request_answer_assistant(answer, 'answer')
			#	if result == 0:
			#		logger.error(ERROR_ADD_REQUEST_ANSWER)
		except Exception as e:
			logger.error(e)


	def determinate_action(self):
		try:
			pass
		except Exception as e:
			logger.error(e)