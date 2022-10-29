from utils.logging import logger
from common.notifications import *
from common.states import states
from handlers.commands import TOPICS
from handlers.config import *
from handlers.functions_name import FunctionsName
from app.functions.notifications import Notifications
from app.functions.communications import Communications


class Handlers:

	def __init__(self):
		try:
			self.notifications = Notifications()
			self.communication = Communications()
		except Exception as e:
			logger.error(e)


	def processing(self, command, default_topic=None, intended_topic=None):
		'''
			Выполение действия (функции) исходя из темы команды
		'''
		try:
			topic = default_topic
			if not topic:
				topic = self.determinate_topic(command, intended_topic)
			print(topic)

			if not topic:
				self.communication.nothing_found()

			else:
				match topic['topic']:
					case FunctionsName.EXIT_TOPIC:
						return self.communication.exit()

					case FunctionsName.NOTIFICATIONS_TOPIC:
						match topic['function']:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)
								states.change_topic(FunctionsName.NOTIFICATIONS_TOPIC)

							case FunctionsName.SHOW_NOTIFICATIONS:
								self.notifications.viewing_notifications()
			
							case FunctionsName.CLEAN_NOTIFICATIONS:
								self.notifications.clean_notifications()

					case FunctionsName.TELEGRAM_MESSAGES_TOPIC:
						match topic['function']:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)
								states.change_topic(FunctionsName.TELEGRAM_MESSAGES_TOPIC)

							case FunctionsName.SHOW_TELEGRAM_MESSAGES:
								self.notifications.viewing_messages(TELEGRAM_MESSAGES_NOTIFICATION)
							
							case FunctionsName.CLEAN_TELEGRAM_MESSAGES:
								self.notifications.clean_messages(TELEGRAM_MESSAGES_NOTIFICATION)

							case FunctionsName.SEND_TELEGRAM_MESSAGES:
								pass

					case FunctionsName.VK_MESSAGES_TOPIC:
						match topic['function']:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)
								states.change_topic(FunctionsName.VK_MESSAGES_TOPIC)

							case FunctionsName.SHOW_VK_MESSAGES:
								self.notifications.viewing_messages(VK_MESSAGES_NOTIFICATION)
							
							case FunctionsName.CLEAN_VK_MESSAGES:
								self.notifications.clean_messages(VK_MESSAGES_NOTIFICATION)

							case FunctionsName.SEND_VK_MESSAGES:
								pass

					case FunctionsName.SOUND_TOPIC:
						match topic['function']:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)
								states.change_topic(FunctionsName.SOUND_TOPIC)
								
							case FunctionsName.SOUND_MUTE:
								states.change_mute_state(True)
							
							case FunctionsName.SOUND_TURN_ON:
								states.change_mute_state(False)

					#case FunctionsName.UPDATE_CONTACTS:
					#	self.communication.update_contacts()

					case _:
						self.communication.nothing_found()

		except Exception as e:
			logger.error(e)


	def check_topic_on_singleness(self, topic):
		'''
			Проверка промежуточной темы на вложенность в нее функций
		'''
		try:
			if not TOPICS[topic][NESTED_FUNCTIONS]:
				return True

			return False
		except Exception as e:
			logger.error(e)
			return False


	def determinate_topic(self, command, intended_topic=None):
		'''
			Определение темы комманды, по словам комманды
		'''
		try:
			topics = {}
			topics_list = []

			if not intended_topic:
				topics_list = TOPICS.keys()
			else:
				topics_list = [intended_topic]

			for topic in topics_list:
				if topic not in topics.keys():
					topics[topic] = {FUNCTIONS: False}

				number_occurrences = []
				for word in command.split():
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

						for word in command.split():
							if word in TOPICS[topic][NESTED_FUNCTIONS][function][ACTIONS]:
								topics[topic][NESTED_FUNCTIONS][function][ACTIONS] += 1

							if word in TOPICS[topic][NESTED_FUNCTIONS][function][ADDITIONALLY]:
								topics[topic][NESTED_FUNCTIONS][function][ADDITIONALLY] += 1

						if not topics[topic][NESTED_FUNCTIONS][function][ACTIONS] and \
						not topics[topic][NESTED_FUNCTIONS][function][ADDITIONALLY]:
							del topics[topic][NESTED_FUNCTIONS][function]

				elif not topics[topic][FUNCTIONS]:
					del topics[topic]

			return self.processing_functions(topics)

		except Exception as e:
			logger.error(e)
			return None


	def processing_functions(self, topics):
		'''
			Обработка возможных функций темы и выявление наиболее подходящей
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
