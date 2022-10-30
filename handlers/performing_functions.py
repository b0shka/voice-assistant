from utils.logging import logger
from common.states import states
from common.notifications import *
from handlers.config import *
from handlers.functions_name import FunctionsName
from app.functions.notifications import Notifications
from app.functions.communications import Communications


class PerformingFunctions:
	
	def __init__(self):
		self.notifications = Notifications()
		self.communication = Communications()


	def processing_topic(self, topic: dict):
		try:
			if states.get_waiting_response_state() and (not topic or topic[TOPIC] != states.get_topic()):
				# если ассистент ожидает ответ, но полученная тема или функция темы не соответсвует ожидаемой
				self.communication.action_not_found_in_topic()

			elif not topic:
				# если тема не была определена (несуществующая функция)
				self.communication.nothing_found()

			else:
				# обработка полученной темы и вложенной функции
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