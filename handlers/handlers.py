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

			if states.get_waiting_response_state() and (not topic or topic[TOPIC] != states.get_topic()):
				self.communication.action_not_found_in_topic()

			elif not topic:
				self.communication.nothing_found()

			else:
				match topic[TOPIC]:
					case FunctionsName.EXIT_TOPIC:
						return self.communication.exit()

					case FunctionsName.NOTIFICATIONS_TOPIC:
						states.change_topic(FunctionsName.NOTIFICATIONS_TOPIC)
						
						match topic[FUNCTION]:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)

							case FunctionsName.SHOW_NOTIFICATIONS:
								self.notifications.viewing_notifications()
								states.change_waiting_response_state(False)
			
							case FunctionsName.CLEAN_NOTIFICATIONS:
								self.notifications.clean_notifications()
								states.change_waiting_response_state(False)

					case FunctionsName.TELEGRAM_MESSAGES_TOPIC:
						states.change_topic(FunctionsName.TELEGRAM_MESSAGES_TOPIC)

						match topic[FUNCTION]:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)

							case FunctionsName.SHOW_TELEGRAM_MESSAGES:
								self.notifications.viewing_messages(TELEGRAM_MESSAGES_NOTIFICATION)
								states.change_waiting_response_state(False)
							
							case FunctionsName.CLEAN_TELEGRAM_MESSAGES:
								self.notifications.clean_messages(TELEGRAM_MESSAGES_NOTIFICATION)
								states.change_waiting_response_state(False)

							case FunctionsName.SEND_TELEGRAM_MESSAGES:
								states.change_waiting_response_state(False)

					case FunctionsName.VK_MESSAGES_TOPIC:
						states.change_topic(FunctionsName.VK_MESSAGES_TOPIC)

						match topic[FUNCTION]:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)

							case FunctionsName.SHOW_VK_MESSAGES:
								self.notifications.viewing_messages(VK_MESSAGES_NOTIFICATION)
								states.change_waiting_response_state(False)
							
							case FunctionsName.CLEAN_VK_MESSAGES:
								self.notifications.clean_messages(VK_MESSAGES_NOTIFICATION)
								states.change_waiting_response_state(False)

							case FunctionsName.SEND_VK_MESSAGES:
								states.change_waiting_response_state(False)

					case FunctionsName.SOUND_TOPIC:
						states.change_topic(FunctionsName.SOUND_TOPIC)
						
						match topic[FUNCTION]:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)
								
							case FunctionsName.SOUND_MUTE:
								states.change_mute_state(True)
								states.change_waiting_response_state(False)
							
							case FunctionsName.SOUND_TURN_ON:
								states.change_mute_state(False)
								states.change_waiting_response_state(False)

					case FunctionsName.CONTACTS_TOPIC:
						states.change_topic(FunctionsName.CONTACTS_TOPIC)

						match topic[FUNCTION]:
							case None:
								self.communication.waiting_select_action()
								states.change_waiting_response_state(True)
								
							case FunctionsName.UPDATE_CONTACTS:
								self.communication.update_contacts()
								states.change_waiting_response_state(False)
							
							case FunctionsName.SHOW_CONTACTS:
								states.change_waiting_response_state(False)

							case FunctionsName.ADD_CONTACT:
								states.change_waiting_response_state(False)

							case FunctionsName.DELETE_CONTACT:
								states.change_waiting_response_state(False)

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
			topics_list = None

			if not intended_topic:
				topics_list = TOPICS.keys()
			else:
				topics_list = (intended_topic,)

			for topic in topics_list:
				if topic not in topics.keys():
					topics[topic] = {FUNCTIONS: False}

				number_occurrences = []
				for word in command.split():
					if word != '':
						if type(TOPICS[topic][FUNCTIONS][0]) == tuple:
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

				else:
					if states.get_topic() == topic and TOPICS[topic][NESTED_FUNCTIONS]:
						topics[topic][NESTED_FUNCTIONS] = {}
						
						for function in TOPICS[topic][NESTED_FUNCTIONS].keys():
							topics[topic][NESTED_FUNCTIONS][function] = {ACTIONS: 0}

							for word in command.split():
								if word in TOPICS[topic][NESTED_FUNCTIONS][function][ACTIONS]:
									topics[topic][NESTED_FUNCTIONS][function][ACTIONS] += 1

							if not topics[topic][NESTED_FUNCTIONS][function][ACTIONS]:
								del topics[topic][NESTED_FUNCTIONS][function]

						if not topics[topic][NESTED_FUNCTIONS]:
							del topics[topic]

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
			
			list_keys = tuple(topics.keys())
			handler_topic = list_keys[0]

			if len(topics) > 1 and not topics[handler_topic][FUNCTIONS]:
				###
				handler_topic = list_keys[1]

			if topics[handler_topic][FUNCTIONS]:
				if NESTED_FUNCTIONS not in topics[handler_topic].keys() or not topics[handler_topic][NESTED_FUNCTIONS]:
					states.change_action_without_function_state(False)
					return {
						TOPIC: handler_topic,
						FUNCTION: None
					}

				else:
					if len(topics[handler_topic][NESTED_FUNCTIONS].keys()) == 1:
						states.change_action_without_function_state(False)
						return {
							TOPIC: handler_topic,
							FUNCTION: next(iter(topics[handler_topic][NESTED_FUNCTIONS]))
						}

					else:
						###
						result_function = {
							NAME: None,
							ACTIONS: 0,
							ADDITIONALLY: 0
						}

						for function in topics[handler_topic][NESTED_FUNCTIONS].keys():
							if topics[handler_topic][NESTED_FUNCTIONS][function][ACTIONS] > result_function[ACTIONS]:
								result_function = topics[handler_topic][NESTED_FUNCTIONS][function]
								result_function[NAME] = function

							elif topics[handler_topic][NESTED_FUNCTIONS][function][ADDITIONALLY] > result_function[ADDITIONALLY]:
								result_function = topics[handler_topic][NESTED_FUNCTIONS][function]
								result_function[NAME] = function

						if result_function[NAME]:
							states.change_action_without_function_state(False)
							return {
								TOPIC: handler_topic,
								FUNCTION: result_function[NAME]
							}
						else:
							return None

			else:
				if not states.get_waiting_response_state():
					# Если ассистент не ожидает ответа в виде какого-то действия, то не дожидаться конечного результата распознавания речи
					states.change_action_without_function_state(True)

				return {
					TOPIC: handler_topic,
					FUNCTION: next(iter(topics[handler_topic][NESTED_FUNCTIONS]))
				}

		except Exception as e:
			logger.error(e)
			print(topics)
			return None
