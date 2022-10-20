import pymorphy2
from database.database_sqlite import DatabaseSQLite
from utils.logging import logger
from common.errors import *
from handlers.list_requests.commands import COMMANDS
from app.functions import notifications, communication


class Handlers:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.morph = pymorphy2.MorphAnalyzer()
		except Exception as e:
			logger.error(e)


	def processing(self, command):
		try:
			topics = self.determinate_topic(command)

			if topics == []:
				communication.nothing_found()

			#if 'уведомления' in command:
			#	if 'мои' in command or 'посмотреть' in command or 'просмотреть' in command:
			#		notifications.viewing_notifications()

			#	elif 'удалить' in command or 'очистить' in command:
			#		notifications.clean_notification

			result = self.db.add_request_answer_assistant(command, 'request')
			if result == 0:
				logger.error(ERROR_ADD_REQUEST_ANSWER)

			#if answer:
			#	result = self.db.add_request_answer_assistant(answer, 'answer')
			#	if result == 0:
			#		logger.error(ERROR_ADD_REQUEST_ANSWER)
		except Exception as e:
			logger.error(e)


	def determinate_topic(self, command):
		try:
			print(command)
			list_command = command.split()
			topics = []

			for i in list_command:
				p = self.morph.parse(i.replace("\u200b", ""))[0]
				normal_form = p.normal_form
				print(normal_form)

			return topics

		except Exception as e:
			logger.error(e)