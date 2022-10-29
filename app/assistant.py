import os
from common.states import states
from common.errors import *
from common.notifications import *
from database.database_sqlite import DatabaseSQLite
from handlers.handlers import Handlers
from utils.logging import logger
#from utils.speech.vosk_recognition import listen
from utils.speech.yandex_recognition_streaming import listen
from domain.Message import Message


class Assistant:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.handlers = Handlers()
			
			self.db.create_tables()
			self.completion_contacts()
			self.completion_notifications()
		except Exception as e:
			logger.error(e)


	def completion_contacts(self):
		'''
			Добавление контактов в глобальное состояние
		'''
		try:
			contacts = self.db.get_contacts()
			if contacts == 0:
				logger.error(ERROR_GET_CONTACTS)

			states.update_contacts(contacts)
		except Exception as e:
			logger.error(e)

	
	def completion_notifications(self):
		'''
			Добавление уведомлений (если такие существуют) в глобальное состояние
		'''
		try:
			telegram_messages = self.db.get_telegram_messages()
			if telegram_messages != 0:
				for message in telegram_messages:
					self.append_message_service(message, TELEGRAM_MESSAGES_NOTIFICATION)
			else:
				logger.error(ERROR_GET_TELEGRAM_MESSAGES)

			vk_messages = self.db.get_vk_messages()
			if vk_messages != 0:
				for message in vk_messages:
					self.append_message_service(message, VK_MESSAGES_NOTIFICATION)
			else:
				logger.error(ERROR_GET_VK_MESSAGES)
		except Exception as e:
			logger.error(e)


	def append_message_service(self, message, service):
		try:
			states.change_notifications(
				service,
				Message(
					message = message[1],
					contact_id = message[2],
					from_id = message[3],
					first_name = message[4],
					last_name = message[5]
				)
			)
		except Exception as e:
			logger.error(e)


	def start(self):
		'''
			Начало прослушивания микрофона и выполнение комманд
		'''
		try:
			intermediate_result = None

			for command in listen():
				if command['mode'] == 'intermediate' and command['text'] != intermediate_result:
					intermediate_result = command['text']
					print('[INTERMEDIATE]', intermediate_result)
					self.handlers.determinate_intermediate_result(intermediate_result)

				elif command['mode'] == 'finite':
					print('[RESULT]', command['text'])

					status_exit = self.handlers.processing(command['text'])
					if status_exit == 0:
						os._exit(1)

					result = self.db.add_request_answer(command['text'], 'request')
					if not result:
						logger.error(ERROR_ADD_REQUEST_ANSWER)

					#if answer:
					#	result = self.db.add_request_answer(answer, 'answer')
					#	if result == 0:
					#		logger.error(ERROR_ADD_REQUEST_ANSWER)


		except Exception as e:
			logger.error(e)