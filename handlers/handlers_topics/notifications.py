from utils.logging import logger
from handlers.functions_name import FunctionsName


def handler_notifications_topic(function):
	try:
		match function:
			case None:
				pass
				#self.communication.waiting_select_action()
				#states.change_waiting_response_state(True)
				#states.change_topic(FunctionsName.NOTIFICATIONS_TOPIC)

			case FunctionsName.SHOW_NOTIFICATIONS:
				pass
				#self.notifications.viewing_notifications()
			
			case FunctionsName.CLEAN_NOTIFICATIONS:
				pass
				#self.notifications.clean_notifications()


	except Exception as e:
		logger.error(e)