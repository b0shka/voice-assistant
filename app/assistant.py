from utils.logging import logger
from handlers.handlers import Handlers
from utils.speech.vosk_recognition import listen
from utils.speech.yandex_synthesis import synthesis_text
from common.states import states


class Assistant:

	def __init__(self):
		try:
			self.handlers = Handlers()
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			for command in listen():
				print(command)

				if 'закончить' in command:
					synthesis_text('до скорой встречи')
					states.change_assistant_work_state(False)
					break
				else:
					self.handlers.processing(command)

		except Exception as e:
			logger.error(e)