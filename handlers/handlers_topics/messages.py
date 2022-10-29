from utils.logging import logger
from handlers.functions_name import FunctionsName


def handler_telegram_messages(function):
	try:
		match function:
			case None:
				pass
				#self.communication.waiting_select_action()
				#states.change_waiting_response_state(True)
				#states.change_topic(FunctionsName.TELEGRAM_MESSAGES_TOPIC)

			case FunctionsName.SHOW_TELEGRAM_MESSAGES:
				pass
				#self.notifications.viewing_messages(TELEGRAM_MESSAGES_NOTIFICATION)
			
			case FunctionsName.CLEAN_TELEGRAM_MESSAGES:
				pass
				#self.notifications.clean_messages(TELEGRAM_MESSAGES_NOTIFICATION)

			case FunctionsName.SEND_TELEGRAM_MESSAGES:
				pass

	except Exception as e:
		logger.error(e)


def handler_vk_messages(function):
	try:
		match function:
			case None:
				pass
				#self.communication.waiting_select_action()
				#states.change_waiting_response_state(True)
				#states.change_topic(FunctionsName.VK_MESSAGES_TOPIC)
				
			case FunctionsName.SHOW_VK_MESSAGES:
				pass
				#self.notifications.viewing_messages(VK_MESSAGES_NOTIFICATION)
			
			case FunctionsName.CLEAN_VK_MESSAGES:
				pass
				#self.notifications.clean_messages(VK_MESSAGES_NOTIFICATION)

			case FunctionsName.SEND_VK_MESSAGES:
				pass

	except Exception as e:
		logger.error(e)