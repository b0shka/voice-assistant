import time
from random import choice
from database.database_sqlite import DatabaseSQLite
from functions.telegram.telegram import Telegram
from functions.vk.vk import VK
from functions.yandex.yandex import Yandex
from functions.speech.synthesizer import say
from common.config import *
from common.errors import *
from request_processing.processing import processing


class Assistant:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.db.create_tables()
			#self.telegram = Telegram()
			#self.vk = VK()
			#self.yandex = Yandex()

			self.contacts = self.db.get_contacts()
			self.telegram_messages = self.db.get_telegram_messages()
			self.vk_messages = self.db.get_vk_messages()
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			#asyncio.create_task(self.monitoring())
			answer = None

			while True:
				#await asyncio.sleep(0.5)
				req = input('')
				result = self.db.add_request_answer_assistant(req, 'request')
				if result == 0:
					logger.error(ERROR_ADD_REQUEST_ANSWER)

				#processing(req)
				
				if req == 'exit':
					break
				elif req == 'hello':
					answer = 'привет'
				elif 'как дела' in req:
					answer = 'В целом не плохо, но я прогулял первую лекцию'
				else:
					answers_else = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
					answer = choice(answers_else)
				
				if answer:
					print(answer)
					say(answer)
					result = self.db.add_request_answer_assistant(answer, 'answer')
					if result == 0:
						logger.error(ERROR_ADD_REQUEST_ANSWER)
		except Exception as e:
			logger.error(e)


	def monitoring(self):
		try:
			while True:
				#await asyncio.sleep(5)

				telegram_messages = self.db.get_telegram_messages()
				if telegram_messages == 0:
					logger.error(ERROR_GET_TELEGRAM_MESSAGES)

				vk_messages = self.db.get_vk_messages()
				if vk_messages == 0:
					logger.error(ERROR_GET_VK_MESSAGES)

				if len(telegram_messages):
					answer = f'У вас {len(telegram_messages)} сообщений в Телеграм'
					say('У вас есть новые сообщения в телеграм')

				if len(vk_messages):
					answer = f'У вас {len(vk_messages)} сообщений в Вконтакте'
					say('У вас есть новые сообщения в Вконтакте')

				self.last_requests_answers = self.db.get_requests_answers()
				if len(self.last_requests_answers) > 10:
					requests_answer = self.last_requests_answers[::-1]
					result = self.db.delete_old_requests_answer(requests_answer[10:])
					if result == 0:
						logger.error(ERROR_CLEAN_OLD_REQUESTS_ANSWERS)

				time.sleep(5)
		except Exception as e:
			logger.error(e)