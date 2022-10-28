from utils.logging import logger
from common.states import states
from common.notifications import *
from handlers.commands import COMMANDS, ALL_FUNCTIONS
from handlers.config import *
from handlers.functions_name import FunctionsName
from app.functions.notifications import Notifications
from app.functions.communication import Communication


class Handlers:

	def __init__(self):
		try:
			self.notifications = Notifications()
			self.communication = Communication()
		except Exception as e:
			logger.error(e)


	def processing(self, command):
		try:
			topic = self.determinate_topics(command)
			print(topic)

			match topic:
				case None:
					self.communication.nothing_found()

				case FunctionsName.EXIT_TOPIC:
					return self.communication.exit()

				case FunctionsName.UPDATE_CONTACTS:
					pass


				# Notifications
				case FunctionsName.NOTIFICATIONS_TOPIC:
					states.change_waiting_response_state(True, FunctionsName.NOTIFICATIONS_TOPIC)
					self.notifications.waiting_select_action()

				case FunctionsName.SHOW_NOTIFICATIONS:
					states.change_waiting_response_state(False, FunctionsName.NOTIFICATIONS_TOPIC)
					self.notifications.viewing_notifications()
				
				case FunctionsName.CLEAN_NOTIFICATIONS:
					states.change_waiting_response_state(False, FunctionsName.NOTIFICATIONS_TOPIC)
					self.notifications.clean_notifications()


				# Telegram
				case FunctionsName.TELEGRAM_MESSAGES_TOPIC:
					states.change_waiting_response_state(True, FunctionsName.TELEGRAM_MESSAGES_TOPIC)
					self.notifications.waiting_select_action()

				case FunctionsName.SHOW_TELEGRAM_MESSAGES:
					self.notifications.viewing_messages(TELEGRAM_MESSAGES_NOTIFICATION)

				case FunctionsName.CLEAN_TELEGRAM_MESSAGES:
					self.notifications.clean_messages(TELEGRAM_MESSAGES_NOTIFICATION)

				case FunctionsName.SEND_TELEGRAM_MESSAGES:
					pass


				# VK
				case FunctionsName.VK_MESSAGES_TOPIC:
					states.change_waiting_response_state(True, FunctionsName.VK_MESSAGES_TOPIC)
					self.notifications.waiting_select_action()

				case FunctionsName.SHOW_VK_MESSAGES:
					self.notifications.viewing_messages(VK_MESSAGES_NOTIFICATION)

				case FunctionsName.CLEAN_VK_MESSAGES:
					self.notifications.clean_messages(VK_MESSAGES_NOTIFICATION)

				case FunctionsName.SEND_VK_MESSAGES:
					pass

				
				# Mute
				case FunctionsName.SOUND_TOPIC:
					states.change_waiting_response_state(True, FunctionsName.SOUND_TOPIC)

				case FunctionsName.SOUND_MUTE:
					states.change_mute_state(True)

				case FunctionsName.SOUND_TURN_ON:
					states.change_mute_state(False)


				case _:
					self.communication.nothing_found()

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
						ADDITIONALLY: 0
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

						if word in COMMANDS[command][ADDITIONALLY]:
							topics[command][ADDITIONALLY] += 1

				if type(COMMANDS[command][FUNCTIONS][0]) == tuple and len(number_occurrences) == len(COMMANDS[command][FUNCTIONS]):
					topics[command][FUNCTIONS] += len(number_occurrences)

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
					ADDITIONALLY: 0
				}

				for topic in topics.keys():
					if topics[topic][ACTIONS] or topics[topic][ADDITIONALLY]:
						if topics[topic][FUNCTIONS] > result_topic[FUNCTIONS]:
							result_topic = topics[topic]
							result_topic[NAME] = topic

						elif topics[topic][ACTIONS] > result_topic[ACTIONS]:
							result_topic = topics[topic]
							result_topic[NAME] = topic

						elif topics[topic][ADDITIONALLY] > result_topic[ADDITIONALLY]:
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