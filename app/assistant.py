import os
import datetime
from common.states import states
from domain.data_class.Contact import Contact
from domain.data_class.Message import Message
from domain.enum_class.Errors import Errors
from domain.enum_class.CommandMode import CommandMode
from domain.enum_class.ActionsAssistant import ActionsAssistant
from handlers.handler import Handler
from database.database_sqlite import DatabaseSQLite
from utils.logging import logger
from utils.speech.yandex_recognition_streaming import listen


class Assistant:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.handler = Handler()
			
			error = self.db.create_tables()
			if isinstance(error, Errors):
				pass # say error

			self.completion_contacts()
			self.completion_notifications()
		except Exception as e:
			logger.error(e)


	def completion_contacts(self):
		'''Добавление контактов в глобальное состояние'''

		try:
			###
			contacts = self.db.get_contacts()
			if isinstance(contacts, Errors):
				logger.error(contacts.value)

			converted_contacts = []
			for contact in contacts:
				convert_contact = Contact(
					id = contact[0],
					first_name = contact[1],
					last_name = contact[2],
					phone = contact[3],
					telegram_id = contact[4],
					vk_id = contact[5],
					email = contact[6]
				)
				converted_contacts.append(convert_contact)

			states.CONTACTS = convert_contact

		except Exception as e:
			logger.error(e)
			# say error

	
	def completion_notifications(self):
		'''Добавление уведомлений (если такие существуют) в глобальное состояние'''

		try:
			telegram_messages = self.db.get_telegram_messages()
			if isinstance(telegram_messages, Errors):
				pass # say error
			else:
				for message in telegram_messages:
					states.NOTIFICATIONS.telegram_messages.append(
						self.get_message_object(message)
					)

			vk_messages = self.db.get_vk_messages()
			if isinstance(vk_messages, Errors):
				pass # say error
			else:
				for message in vk_messages:
					states.NOTIFICATIONS.vk_messages.append(
						self.get_message_object(message)
					)
				
		except Exception as e:
			logger.error(e)
			# say error

	
	def get_message_object(self, message: list) -> Message:
		return Message(
			text = message[1],
			contact_id = message[2],
			from_id = message[3],
			first_name = message[4],
			last_name = message[5]
		)


	def start(self):
		'''Начало прослушивания микрофона и выполнение комманд'''

		try:
			intended_topic = None

			for command in listen():
				time_now = datetime.datetime.now().time()

				if command.mode == CommandMode.INTERMEDIATE:
					# обработка промежуточного результата распознавания речи

					print(f'{time_now} [INTERMEDIATE] {command.text}')
					topic = self.handler.determinate_topic(command.text)

					if topic and topic.topic and not states.ACTION_WITHOUT_FUNCTION:
						# если была получена тема и в команде присутствует функция
						error = self.handler.check_nested_functions(topic.topic)

						if topic.functions or isinstance(error, bool):
							# если была определена вложенная функция или у темы в принципе их нет
							states.WAITING_RESULT_RECOGNITION = False

							# если уже получена тема, то сразу вызывать обработку темы и выполнение функции
							action_assistant = self.handler.processing_topic(topic)
							match self.handler.processing_topic(topic):
								case ActionsAssistant.EXIT:
									os._exit(1)
								case error if isinstance(error, Errors):
									pass # say error

						elif isinstance(error, Errors):
							pass # say error

						else:
							intended_topic = topic.topic

				elif command.mode == CommandMode.FINITE:
					# обработка конечного результата распознавания речи

					if not states.WAITING_RESULT_RECOGNITION:
						# если не ожидается получение конечного результата распознавания речи
						states.WAITING_RESULT_RECOGNITION = True
					else:
						# был получен конечный результат распознавания речи
						print(f'{time_now} [RESULT] {command.text}')

						if command.text:
							action_assistant = self.handler.processing_command(
								command = command.text,
								intended_topic = intended_topic
							)
							match action_assistant:
								case ActionsAssistant.EXIT:
									os._exit(1)
								case error if isinstance(error, Errors):
									pass # say error

		except Exception as e:
			logger.error(e)
			# say error