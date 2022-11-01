import os
import datetime
from common.states import states
from domain.enum_class.Errors import Errors
from domain.enum_class.CommandMode import CommandMode
from domain.enum_class.ActionsAssistant import ActionsAssistant
from handlers.handler import Handler
from database.database_sqlite import DatabaseSQLite
from utils.logging import logger
from utils.speech.yandex_recognition_streaming import listen
from app.functions.settings import Settings


class Assistant:

	def __init__(self) -> None:
		try:
			self.db = DatabaseSQLite()
			self.handler = Handler()
			self.settings = Settings()
			
			error = self.db.create_tables()
			if isinstance(error, Errors):
				###
				self.settings.say_error(error)

			self.settings.update_contacts(isLauch=True)
			self.settings.update_notifications(isLauch=True)

		except Exception as e:
			logger.error(e)


	def start(self) -> None:
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

						if topic.functions or (isinstance(error, bool) and error):
							# если была определена вложенная функция или у темы в принципе их нет
							states.WAITING_RESULT_RECOGNITION = False

							# если уже получена тема, то сразу вызывать обработку темы и выполнение функции
							action_assistant = self.handler.processing_topic(topic)
							match action_assistant:
								case ActionsAssistant.EXIT:
									os._exit(1)
								case error if isinstance(error, Errors):
									self.settings.say_error(error)

						elif isinstance(error, Errors):
							self.settings.say_error(error)

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
									self.settings.say_error(error)

		except Exception as e:
			self.settings.say_error(Errors.START_LISTEN)
			logger.error(e)