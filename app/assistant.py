import os
import datetime
from common.states import states
from domain.enum_class.CommandMode import CommandMode
from domain.enum_class.TopicsNames import TopicsNames
from domain.enum_class.ActionsAssistant import ActionsAssistant
from domain.named_tuple.Command import Command
from utils.speech.yandex_recognition_streaming import listen
from app.handlers.handler_command import determinate_topic, check_nested_functions
from app.handlers.performing_functions import processing_topic


def launch() -> None:
	pass # get notifications, contacts


def start_listen() -> None:
	'''Начало прослушивания микрофона'''

	intended_topic = None

	for command in listen():
		if command.mode == CommandMode.INTERMEDIATE:
			find_topic = _processing_intermediate_command(command)
			if find_topic is not None:
				intended_topic = find_topic

		elif command.mode == CommandMode.FINITE:
			_processing_finite_command(command, intended_topic)


def _processing_intermediate_command(command: Command) -> None | TopicsNames:
	'''Обработка промежуточного результата распознавания речи'''

	time_now = datetime.datetime.now().time()
	print(f'{time_now} [INTERMEDIATE] {command.text}')
	topic = determinate_topic(command.text)

	if topic and topic.topic and not states.ACTION_WITHOUT_FUNCTION:
		# если была получена тема и в команде присутствует функция
		status = check_nested_functions(topic.topic)

		if topic.functions or status:
			# если была определена вложенная функция или у темы в принципе их нет
			states.WAITING_RESULT_RECOGNITION = False

			# если уже получена тема, то сразу вызывать обработку темы и выполнение функции
			action_assistant = processing_topic(topic)
			match action_assistant:
				case ActionsAssistant.EXIT:
					os._exit(1)

		else:
			return(topic.topic)



def _processing_finite_command(command: Command, intended_topic: TopicsNames) -> None:
	'''Обработка конечного результата распознавания речи'''

	time_now = datetime.datetime.now().time()

	if not states.WAITING_RESULT_RECOGNITION:
		# если не ожидается получение конечного результата распознавания речи
		states.WAITING_RESULT_RECOGNITION = True
	else:
		print(f'{time_now} [RESULT] {command.text}')

		topic = determinate_topic(command.text, intended_topic)
		action_assistant = processing_topic(topic)

		match action_assistant:
			case ActionsAssistant.EXIT:
				os._exit(1)
