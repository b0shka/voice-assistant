import os
import datetime
from common.states import states
from common.exceptions.handlers import *
from domain.named_tuple.Command import Command
from domain.enum_class.TopicsNames import TopicsNames
from domain.enum_class.CommandMode import CommandMode
from domain.enum_class.ActionsAssistant import ActionsAssistant
from app.handlers.handler_topic import determinate_topic, check_nested_functions
from app.handlers.performing_functions import processing_topic
from app.functions.communications import say_error


intended_topic = None

def processing_command(command: Command) -> None:
	'''Обработка полученной команды'''
	global intended_topic

	if command.mode == CommandMode.INTERMEDIATE:
		find_topic = _processing_intermediate_command(command)
		if find_topic is not None:
			intended_topic = find_topic

	elif command.mode == CommandMode.FINITE:
		_processing_finite_command(command, intended_topic)
		intended_topic = None


def _processing_intermediate_command(command: Command) -> None | TopicsNames:
	'''Обработка промежуточного результата распознавания речи'''

	try:
		time_now = datetime.datetime.now().time()
		print(f'{time_now} [INTERMEDIATE] {command.text}')
		topic = determinate_topic(command.text)

		if topic.topic and not states.ACTION_WITHOUT_FUNCTION:
			# если была получена тема и в команде присутствует функция
			status = check_nested_functions(topic.topic)
			print('STATUS NESTED FUNCTIONS: ', status)

			if topic.functions or not status:
				# если была определена вложенная функция или у темы в принципе их нет
				states.WAITING_RESULT_RECOGNITION = False

				# если уже получена тема, то сразу вызывать обработку темы и выполнение функции
				action_assistant = processing_topic(topic)
				match action_assistant:
					case ActionsAssistant.EXIT:
						os._exit(1)

			else:
				return(topic.topic)
	
	except (ErrCheckNestedFunctions, ErrDeterminateTopic) as e:
		say_error(e)



def _processing_finite_command(command: Command, intended_topic: TopicsNames) -> None:
	'''Обработка конечного результата распознавания речи'''

	try:
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

	except ErrDeterminateTopic as e:
		say_error(e)
