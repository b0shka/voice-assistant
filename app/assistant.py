from utils.logging import logger
from database.database_sqlite import DatabaseSQLite
from handlers.handlers import Handlers
from utils.speech.vosk_recognition import listen
from utils.speech.yandex_synthesis import synthesis_text
from common.states import states
from app.functions.notifications import completion_notifications


class Assistant:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.db.create_tables()
			self.handlers = Handlers()

			self.contacts = self.db.get_contacts()
			completion_notifications(self.db.get_telegram_messages(), self.db.get_vk_messages())
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			intermediate_result = None

			for command in listen():
				if command['mode'] == 'intermediate' and command['text'] != intermediate_result:
					intermediate_result = command['text']
					print('[INTERMEDIATE]', intermediate_result)

				elif command['mode'] == 'finite':
					print('[RESULT]', command['text'])

					if 'закончить' in command['text']:
						synthesis_text('до скорой встречи')
						states.change_assistant_work_state(False)
						break
					else:
						self.handlers.processing(command['text'])

		except Exception as e:
			logger.error(e)