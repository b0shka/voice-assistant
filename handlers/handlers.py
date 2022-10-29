from utils.logging import logger
from common.notifications import *
from handlers.commands import TOPICS
from handlers.config import *
from handlers.functions_name import FunctionsName
from handlers.handlers_topics import notifications, messages, communications
from app.functions.notifications import Notifications
from app.functions.communications import Communications


class Handlers:

	def __init__(self):
		try:
			self.notifications = Notifications()
			self.communication = Communications()
		except Exception as e:
			logger.error(e)


	def processing(self, command):
		'''
			Выполение действия (функции) исходя из темы команды
		'''
		try:
			topic = self.determinate_topics(command)
			print(topic)

			if not topic:
				self.communication.nothing_found()

			else:
				match topic['topic']:
					case FunctionsName.EXIT_TOPIC:
						return self.communication.exit()

					case FunctionsName.NOTIFICATIONS_TOPIC:
						notifications.handler_notifications_topic(topic['function'])

					case FunctionsName.TELEGRAM_MESSAGES_TOPIC:
						messages.handler_telegram_messages(topic['function'])

					case FunctionsName.VK_MESSAGES_TOPIC:
						messages.handler_vk_messages(topic['function'])

					case FunctionsName.SOUND_TOPIC:
						communications.handler_sound_topic(topic['function'])

					#case FunctionsName.UPDATE_CONTACTS:
					#	self.communication.update_contacts()

					case _:
						self.communication.nothing_found()

		except Exception as e:
			logger.error(e)


	def determinate_intermediate_result(self, text_command):
		'''
			Определение возможных тем промежуточной команды
		'''
		try:
			topics = self.determinate_topics(text_command)
			print(topics)
		except Exception as e:
			logger.error(e)


	def determinate_topics(self, text_command):
		'''
			Определение всех допустимых тем комманды, по словам комманды
		'''
		try:
			topics = {}

			for topic in TOPICS.keys():
				if topic not in topics.keys():
					topics[topic] = {FUNCTIONS: False}

				number_occurrences = []
				for word in text_command.split():
					if word != '':
						if type(TOPICS[topic][FUNCTIONS][0]) == tuple:
							###
							for index, func in enumerate(TOPICS[topic][FUNCTIONS]):
								if index not in number_occurrences and word in func:
									number_occurrences.append(index)
						else:
							if word in TOPICS[topic][FUNCTIONS]:
								topics[topic][FUNCTIONS] = True
								break

				if type(TOPICS[topic][FUNCTIONS][0]) == tuple and len(number_occurrences) == len(TOPICS[topic][FUNCTIONS]):
					topics[topic][FUNCTIONS] = True

				if topics[topic][FUNCTIONS] and TOPICS[topic][NESTED_FUNCTIONS]:
					topics[topic][NESTED_FUNCTIONS] = {}

					for function in TOPICS[topic][NESTED_FUNCTIONS].keys():
						topics[topic][NESTED_FUNCTIONS][function] = {
							ACTIONS: 0,
							ADDITIONALLY: 0
						}

						for word in text_command.split():
							if word in TOPICS[topic][NESTED_FUNCTIONS][function][ACTIONS]:
								topics[topic][NESTED_FUNCTIONS][function][ACTIONS] += 1

							if word in TOPICS[topic][NESTED_FUNCTIONS][function][ADDITIONALLY]:
								topics[topic][NESTED_FUNCTIONS][function][ADDITIONALLY] += 1

						if not topics[topic][NESTED_FUNCTIONS][function][ACTIONS] and \
						not topics[topic][NESTED_FUNCTIONS][function][ADDITIONALLY]:
							del topics[topic][NESTED_FUNCTIONS][function]

				elif not topics[topic][FUNCTIONS]:
					del topics[topic]

			return self.processing_topics(topics)

		except Exception as e:
			logger.error(e)
			return None


	def processing_topics(self, topics):
		'''
			Обработка всех возможных тем комманды и выявление наиболее подходящей
		'''
		try:
			if len(topics) == 0:
				return None
			
			else:
				first_topic = next(iter(topics))

				if NESTED_FUNCTIONS not in topics[first_topic].keys() or not topics[first_topic][NESTED_FUNCTIONS]:
					return {
						TOPIC: first_topic,
						FUNCTION: None
					}

				else:
					if len(topics[first_topic][NESTED_FUNCTIONS].keys()) == 1:
						return {
							TOPIC: first_topic,
							FUNCTION: next(iter(topics[first_topic][NESTED_FUNCTIONS]))
						}

					else:
						result_function = {
							NAME: None,
							ACTIONS: 0,
							ADDITIONALLY: 0
						}

						for function in topics[first_topic][NESTED_FUNCTIONS].keys():
							if topics[first_topic][NESTED_FUNCTIONS][function][ACTIONS] > result_function[ACTIONS]:
								result_function = topics[first_topic][NESTED_FUNCTIONS][function]
								result_function[NAME] = function

							elif topics[first_topic][NESTED_FUNCTIONS][function][ADDITIONALLY] > result_function[ADDITIONALLY]:
								result_function = topics[first_topic][NESTED_FUNCTIONS][function]
								result_function[NAME] = function

						if result_function[NAME]:
							return {
								TOPIC: first_topic,
								FUNCTION: result_function[NAME]
							}
						else:
							return None

		except Exception as e:
			logger.error(e)
			return None