from utils.logging import logger
from database.database_sqlite import DatabaseSQLite
from handlers.handlers import Handlers
from utils.speech.vosk_recognition import listen
from utils.speech.yandex_synthesis import synthesis_text
from common.states import states


class Assistant:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.db.create_tables()
			self.handlers = Handlers()

			self.contacts = self.db.get_contacts()
			self.check_notifications()
		except Exception as e:
			logger.error(e)


	def check_notifications(self):
		try:
			telegram_messages = self.db.get_telegram_messages()
			for message in telegram_messages:
				states.change_notifications(
					'telegram_messages',
					{
						'message': message[1],
						'from_id': message[2]
					}
				)

			vk_messages = self.db.get_vk_messages()
			for message in vk_messages:
				states.change_notifications(
					'vk_messages',
					{
						'message': message[1],
						'from_id': message[2]
					}
				)
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			intermediate_result = None

			for command in listen():
				if command['mode'] == 'finite':
					print('[RESULT]', command['text'])

				elif command['mode'] == 'intermediate' and command['text'] != intermediate_result:
					intermediate_result = command['text']
					print('[INTERMEDIATE]', intermediate_result)

				if 'закончить' in command['text']:
					synthesis_text('до скорой встречи')
					states.change_assistant_work_state(False)
					break
				#else:
				#	self.handlers.processing(command['text'])

		except Exception as e:
			logger.error(e)