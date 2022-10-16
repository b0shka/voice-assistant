import time
from utils.logging import logger
from common.errors import *
from database.database_sqlite import DatabaseSQLite
from utils.speech.yandex_synthesis import synthesis_text


class Monitoring:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.db.create_tables()

			self.contacts = self.db.get_contacts()
			self.telegram_messages = self.db.get_telegram_messages()
			self.vk_messages = self.db.get_vk_messages()
		except Exception as e:
			logger.error(e)


	def check_telegram_messages(self):
		try:
			telegram_messages = self.db.get_telegram_messages()
			if telegram_messages == 0:
				logger.error(ERROR_GET_TELEGRAM_MESSAGES)

			count_telegram_messages = str(len(telegram_messages))
			if int(count_telegram_messages):
				if count_telegram_messages[-1] == '1':
					answer = 'У вас одно новое сообщение в Телеграм'
				elif count_telegram_messages[-1] in ('2', '3', '4'):
					answer = f'У вас {count_telegram_messages} новых сообщения в Телеграм'
				else:
					answer = f'У вас {count_telegram_messages} новых сообщений в Телеграм'
				synthesis_text(answer)

				for message in telegram_messages:
					result = self.db.delete_telegram_message(message[0])
					if result == 0:
						logger.error(ERROR_DELETE_NEW_TELEGRAM_MESSAGE)
		except Exception as e:
			logger.error(e)


	def check_vk_messages(self):
		try:
			vk_messages = self.db.get_vk_messages()
			if vk_messages == 0:
				logger.error(ERROR_GET_VK_MESSAGES)

			count_vk_messages = str(len(vk_messages))
			if int(count_vk_messages):
				if count_vk_messages[-1] == '1':
					answer = 'У вас одно новое сообщение в Вконтакте'
				elif count_vk_messages[-1] in ('2', '3', '4'):
					answer = f'У вас {count_vk_messages} новых сообщения в Вконтакте'
				else:
					answer = f'У вас {count_vk_messages} новых сообщений в Вконтакте'
				synthesis_text(answer)

				for message in vk_messages:
					result = self.db.delete_vk_message(message[0])
					if result == 0:
						logger.error(ERROR_DELETE_NEW_VK_MESSAGE)
		except Exception as e:
			logger.error(e)


	def check_overcrowding_old_requests(self):
		try:
			self.last_requests_answers = self.db.get_requests_answers()
			if len(self.last_requests_answers) > 10:
				requests_answer = self.last_requests_answers[::-1]
				result = self.db.delete_old_requests_answer(requests_answer[10:])
				if result == 0:
					logger.error(ERROR_CLEAN_OLD_REQUESTS_ANSWERS)
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			while True:
				self.check_telegram_messages()
				self.check_vk_messages()
				self.check_overcrowding_old_requests()

				time.sleep(5)
		except Exception as e:
			logger.error(e)