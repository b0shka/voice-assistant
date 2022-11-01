from domain.data_class.Topic import Topic
from domain.enum_class.Errors import Errors
from domain.enum_class.Services import Services
from domain.enum_class.ActionsAssistant import ActionsAssistant
from utils.logging import logger
from common.states import states
from handlers.config import *
from handlers.functions_names import TopicsNames, FunctionsNames
from app.functions.notifications import Notifications
from app.functions.communications import Communications
from app.functions.settings import Settings


class PerformingFunctions:
	
	def __init__(self) -> None:
		self.notifications = Notifications()
		self.communication = Communications()
		self.settings = Settings()


	def processing_topic(self, topic: Topic) -> None | ActionsAssistant | Errors:
		'''Выполнение функции исходя из полученной темы и вложенной в нее функции (не всегда)
'''

		try:
			print(topic)

			if states.WAITING_RESPONSE and topic.topic != states.TOPIC.topic:
				# если ассистент ожидает ответ, но полученная тема или функция темы не соответсвует ожидаемой
				self.communication.action_not_found_in_topic()

			elif not topic.topic:
				# если тема не была определена (несуществующая функция)
				self.communication.nothing_found()

			else:
				# обработка полученной темы и вложенной функции
				states.TOPIC = Topic(
					topic = topic.topic,
					functions = topic.functions
				)

				if not topic.functions:
					states.WAITING_RESPONSE = True
				else:
					states.WAITING_RESPONSE = False

				match topic.topic:
					case TopicsNames.EXIT_TOPIC:
						return self.communication.exit()

					case TopicsNames.NOTIFICATIONS_TOPIC:
						match topic.functions:
							case None:
								self.communication.waiting_select_action()

							case FunctionsNames.SHOW_NOTIFICATIONS:
								self.notifications.viewing_notifications()
			
							case FunctionsNames.CLEAN_NOTIFICATIONS:
								self.notifications.clean_notifications()

							case FunctionsNames.UPDATE_NOTIFICATIONS:
								self.settings.update_notifications()

					case TopicsNames.TELEGRAM_MESSAGES_TOPIC:
						match topic.functions:
							case None:
								self.communication.waiting_select_action()

							case FunctionsNames.SHOW_TELEGRAM_MESSAGES:
								self.notifications.viewing_messages(Services.TELEGRAM)
							
							case FunctionsNames.CLEAN_TELEGRAM_MESSAGES:
								self.notifications.clean_messages(Services.TELEGRAM)

							case FunctionsNames.SEND_TELEGRAM_MESSAGES:
								pass

					case TopicsNames.VK_MESSAGES_TOPIC:
						match topic.functions:
							case None:
								self.communication.waiting_select_action()

							case FunctionsNames.SHOW_VK_MESSAGES:
								self.notifications.viewing_messages(Services.VK)
							
							case FunctionsNames.CLEAN_VK_MESSAGES:
								self.notifications.clean_messages(Services.VK)

							case FunctionsNames.SEND_VK_MESSAGES:
								pass

					case TopicsNames.SOUND_TOPIC:
						match topic.functions:
							case None:
								self.communication.waiting_select_action()
								
							case FunctionsNames.SOUND_MUTE:
								states.change_mute_state(True)
							
							case FunctionsNames.SOUND_TURN_ON:
								states.change_mute_state(False)

					case TopicsNames.CONTACTS_TOPIC:
						match topic.functions:
							case None:
								self.communication.waiting_select_action()
								
							case FunctionsNames.UPDATE_CONTACTS:
								self.settings.update_contacts()
							
							case FunctionsNames.SHOW_CONTACTS:
								pass

							case FunctionsNames.ADD_CONTACT:
								pass

							case FunctionsNames.DELETE_CONTACT:
								pass

					case _:
						self.communication.nothing_found()

		except Exception as e:
			logger.error(e)
			return Errors.PROCESSING_TOPIC