from database.database_sqlite import DatabaseSQLite
from utils.logging import logger
from common.errors import *
from handlers.list_requests.commands import COMMANDS, ALL_FUNCTIONS
from handlers.list_requests.config import *
from handlers.list_requests.functions_name import *
from app.functions import notifications, communication


class Handlers:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
		except Exception as e:
			logger.error(e)


	def processing(self, command):
		try:
			topic = self.determinate_topics(command.lower())
			print(topic)

			match topic:
				case None:
					communication.nothing_found()

				case topic if topic == EXIT_TOPIC:
					return communication.exit()

				case topic if topic == NOTIFICATIONS_TOPIC:
					pass

				case topic if topic == SHOW_NOTIFICATIONS:
					notifications.viewing_notifications()
				
				case topic if topic == CLEAN_NOTIFICATIONS:
					notifications.clean_all_notifications()

				case topic if topic == TELEGRAM_MESSAGES_TOPIC:
					pass

				case topic if topic == SHOW_TELEGRAM_MESSAGES:
					notifications.viewing_telegram_messages()

				case topic if topic == CLEAN_TELEGRAM_MESSAGES:
					notifications.clean_telegram_messages()

				case topic if topic == SEND_TELEGRAM_MESSAGES:
					pass

				case topic if topic == VK_MESSAGES_TOPIC:
					pass

				case topic if topic == SHOW_VK_MESSAGES:
					notifications.viewing_vk_messages()

				case topic if topic == CLEAN_VK_MESSAGES:
					notifications.clean_vk_messages()

				case topic if topic == SEND_VK_MESSAGES:
					pass

				case _:
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


	def determinate_topics(self, text_command):
		try:
			topics = {}

			for command in COMMANDS.keys():
				if command not in topics.keys():
					topics[command] = {
						FUNCTIONS: 0,
						ACTIONS: 0,
						PRONOUNS: 0
					}

				number_occurrences = []
				for word in text_command.split():
					if word != '':
						if type(COMMANDS[command][FUNCTIONS][0]) == tuple:
							for index, func in enumerate(COMMANDS[command][FUNCTIONS]):
								if word in func and index not in number_occurrences:
									number_occurrences.append(index)
						else:
							if word in COMMANDS[command][FUNCTIONS]:
								topics[command][FUNCTIONS] += 1
						
						if word in COMMANDS[command][ACTIONS]:
							topics[command][ACTIONS] += 1

						if word in COMMANDS[command][PRONOUNS]:
							topics[command][PRONOUNS] += 1

				if len(number_occurrences) == len(COMMANDS[command][FUNCTIONS]):
					topics[command][FUNCTIONS] = len(number_occurrences)

				if topics[command][FUNCTIONS] == 0:
					del topics[command]

			return self.processing_topics(topics)

		except Exception as e:
			logger.error(e)
			return None


	def processing_topics(self, topics):
		try:
			if len(topics) > 1:
				result_topic = {
					NAME: None,
					FUNCTIONS: 0,
					ACTIONS: 0,
					PRONOUNS: 0
				}

				for topic in topics.keys():
					if topics[topic][ACTIONS] or topics[topic][PRONOUNS]:
						if topics[topic][FUNCTIONS] > result_topic[FUNCTIONS]:
							result_topic = topics[topic]
							result_topic[NAME] = topic

						elif topics[topic][ACTIONS] > result_topic[ACTIONS]:
							result_topic = topics[topic]
							result_topic[NAME] = topic

						elif topics[topic][PRONOUNS] > result_topic[PRONOUNS]:
							result_topic = topics[topic]
							result_topic[NAME] = topic

				if result_topic['name']:
					return result_topic['name']

				for func in ALL_FUNCTIONS.keys():
					if tuple(topics.keys()) == ALL_FUNCTIONS[func]:
						return func

			list_topics = list(topics.keys())
			if len(list_topics) >= 1:
				return list_topics[0]
			else:
				return None

		except Exception as e:
			logger.error(e)
			return None