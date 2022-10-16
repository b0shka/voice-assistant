import time
from database.database_sqlite import DatabaseSQLite
from common.errors import *
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text
from utils.speech.vosk_recognition import listen
from handlers.handlers import Handlers


class Assistant:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.db.create_tables()
			self.handlers = Handlers()

			self.contacts = self.db.get_contacts()
			self.telegram_messages = self.db.get_telegram_messages()
			self.vk_messages = self.db.get_vk_messages()
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			pass
			#for command in listen():
			#	print(command)

			#	if 'закончить' in command:
			#		synthesis_text('до скорой встречи')
			#		break
			#	else:
			#		self.handlers.processing(command)
			#		result = self.db.add_request_answer_assistant(command, 'request')
			#		if result == 0:
			#			logger.error(ERROR_ADD_REQUEST_ANSWER)

		except Exception as e:
			logger.error(e)


	def monitoring(self):
		try:
			while True:
				telegram_messages = self.db.get_telegram_messages()
				if telegram_messages == 0:
					logger.error(ERROR_GET_TELEGRAM_MESSAGES)

				if len(telegram_messages):
					if str(len(vk_messages))[-1] == '1':
						answer = 'У вас одно новое сообщение в Телеграм'
					elif str(len(vk_messages))[-1] in ('2', '3', '4'):
						answer = f'У вас {len(telegram_messages)} новых сообщения в Телеграм'
					else:
						answer = f'У вас {len(telegram_messages)} новых сообщений в Телеграм'
					synthesis_text(answer)
					
					for message in telegram_messages:
						result = self.db.delete_telegram_message(message[0])
						if result == 0:
							logger.error(ERROR_DELETE_NEW_TELEGRAM_MESSAGE)

				vk_messages = self.db.get_vk_messages()
				if vk_messages == 0:
					logger.error(ERROR_GET_VK_MESSAGES)

				if len(vk_messages):
					if str(len(vk_messages))[-1] == '1':
						answer = 'У вас одно новое сообщение в Вконтакте'
					elif str(len(vk_messages))[-1] in ('2', '3', '4'):
						answer = f'У вас {len(vk_messages)} новых сообщения в Вконтакте'
					else:
						answer = f'У вас {len(vk_messages)} новых сообщений в Вконтакте'
					synthesis_text(answer)

					for message in vk_messages:
						result = self.db.delete_vk_message(message[0])
						if result == 0:
							logger.error(ERROR_DELETE_NEW_VK_MESSAGE)

				self.last_requests_answers = self.db.get_requests_answers()
				if len(self.last_requests_answers) > 10:
					requests_answer = self.last_requests_answers[::-1]
					result = self.db.delete_old_requests_answer(requests_answer[10:])
					if result == 0:
						logger.error(ERROR_CLEAN_OLD_REQUESTS_ANSWERS)

				time.sleep(5)
		except Exception as e:
			logger.error(e)
