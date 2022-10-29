from utils.logging import logger
from handlers.functions_name import FunctionsName


def handler_sound_topic(function):
	try:
		match function:
			case None:
				pass
				#self.communication.waiting_select_action()
				#states.change_waiting_response_state(True)
				#states.change_topic(FunctionsName.SOUND_TOPIC)
				
			case FunctionsName.SOUND_MUTE:
				pass
				#states.change_mute_state(True)
			
			case FunctionsName.SOUND_TURN_ON:
				pass
				#states.change_mute_state(False)

	except Exception as e:
		logger.error(e)