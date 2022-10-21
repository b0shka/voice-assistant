#import pymorphy2
from database.database_sqlite import DatabaseSQLite
from utils.logging import logger
from common.errors import *
from handlers.list_requests.commands import COMMANDS
from handlers.list_requests.config import *
from app.functions import notifications, communication


class Handlers:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			#self.morph = pymorphy2.MorphAnalyzer()
		except Exception as e:
			logger.error(e)


	def processing(self, command):
		try:
			topics = self.determinate_topics(command)
			print(topics)

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


	def determinate_topics(self, text_command):
		try:
			topics = {}

			for command in COMMANDS.keys():
				for word in text_command.split():
					if type(COMMANDS[command][FUNCTION][0]) == tuple:
						pass

					if word in COMMANDS[command][FUNCTION]:
						topics[command][FUNCTION] += 1
					
					if word in COMMANDS[command][ACTIONS]:
						topics[command][ACTIONS] += 1

					if word in COMMANDS[command][PRONOUNS]:
						topics[command][PRONOUNS] += 1

			#for word in text_command.split():
			#	#p = self.morph.parse(word.replace("\u200b", ""))[0]
			#	#normal_form = p.normal_form
			#	normal_form = word
				
			#	for i in COMMANDS.keys():
			#		if i not in topics.keys():
			#			topics[i] = {
			#				FUNCTION: 0,
			#				ACTIONS: 0,
			#				PRONOUNS: 0
			#			}

			#		if type(COMMANDS[i][FUNCTION][0]) == tuple:
			#			count_ = 0
						
			#			for func in COMMANDS[i][FUNCTION]:
			#				if normal_form in func:
			#					count_ += 1

			#			if count_ == len(COMMANDS[i][FUNCTION]):
			#				topics[i][FUNCTION] += 1
			#		else:
			#			if normal_form in COMMANDS[i][FUNCTION]:
			#				topics[i][FUNCTION] += 1

			#		if normal_form in COMMANDS[i][ACTIONS]:
			#			topics[i][ACTIONS] += 1

			#		if normal_form in COMMANDS[i][PRONOUNS]:
			#			topics[i][PRONOUNS] += 1

			#		if topics[i][FUNCTION] == 0:
			#			del topics[i]

			return topics

		except Exception as e:
			logger.error(e)