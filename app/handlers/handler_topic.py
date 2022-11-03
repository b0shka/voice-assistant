from common.states import states
from common.exceptions.handlers import *
from domain.named_tuple.Topic import Topic
from domain.enum_class.Errors import Errors
from domain.enum_class.TopicsNames import TopicsNames
from app.handlers.topics import TOPICS
from app.handlers.config import *


def check_nested_functions(topic: TopicsNames) -> bool:
	'''Проверка промежуточной темы на вложенность в нее функций'''

	try:
		if not TOPICS[topic][NESTED_FUNCTIONS]:
			return False

		return True
	except KeyError:
		raise ErrCheckNestedFunctions(Errors.CHECK_NESTED_FUNCIONS.value)


def determinate_topic(command: str, intended_topic: TopicsNames | None = None) -> Topic:
	'''Определение темы комманды, по словам комманды'''

	try:
		topics = {}

		if not intended_topic:
			input_topics = TOPICS.keys()
		else:
			# добавление уже заранее подобранной темы запроса (при промежуточной результате распознавания речи)
			input_topics = (intended_topic,)

		for topic in input_topics:
			if topic not in topics.keys():
				topics[topic] = {FUNCTIONS: False}

			status = _find_functions_command(command, topic)
			topics[topic][FUNCTIONS] = status

			if topics[topic][FUNCTIONS] and TOPICS[topic][NESTED_FUNCTIONS]:
				nested_functions = _find_nested_functions_with_function(command, topic)
				topics[topic][NESTED_FUNCTIONS] = nested_functions

			elif states.TOPIC.topic == topic and TOPICS[topic][NESTED_FUNCTIONS]:
				nested_functions = _find_nested_functions_without_function(command, topic)
				if not nested_functions:
					del topics[topic]
				else:
					topics[topic][NESTED_FUNCTIONS] = nested_functions

			elif not topics[topic][FUNCTIONS]:
				# удаление темы если в ней не была найдена функция
				del topics[topic]

		return _processing_functions(topics)
	
	except KeyError:
		raise ErrDeterminateTopic(Errors.DETERMINATE_TOPIC.value)

	
def _find_functions_command(command: str, topic: TopicsNames) -> bool:
	'''Определение функций в команде'''

	number_occurrences = []

	for word in command.split():
		if word != '':
			if isinstance(TOPICS[topic][FUNCTIONS][0], tuple):
				# проверка на вхожение слов команды во все кортежи возможных слов (которые являются обязательными)
				for index, func in enumerate(TOPICS[topic][FUNCTIONS]):
					if index not in number_occurrences and word in func:
						number_occurrences.append(index)
			else:
				if word in TOPICS[topic][FUNCTIONS]:
					return True

	if isinstance(TOPICS[topic][FUNCTIONS][0], tuple) \
	and len(number_occurrences) == len(TOPICS[topic][FUNCTIONS]):
		return True

	return False


def _find_nested_functions_with_function(command: str, topic: TopicsNames) -> dict:
	'''Определение действий и доп. слов в команде, если была выявлена функция и у этой темы есть вложенные функции'''
	
	nested_functions = {}

	for function in TOPICS[topic][NESTED_FUNCTIONS].keys():
		nested_functions[function] = {
			ACTIONS: 0,
			ADDITIONALLY: 0
		}

		for word in command.split():
			if word in TOPICS[topic][NESTED_FUNCTIONS][function][ACTIONS]:
				nested_functions[function][ACTIONS] += 1

			if word in TOPICS[topic][NESTED_FUNCTIONS][function][ADDITIONALLY]:
				nested_functions[function][ADDITIONALLY] += 1

		if not nested_functions[function][ACTIONS] and \
		not nested_functions[function][ADDITIONALLY]:
			del nested_functions[function]

	return nested_functions


def _find_nested_functions_without_function(command: str, topic: TopicsNames) -> dict:
	'''Обработка команды без функции, но по теме диалога'''

	nested_functions = {}

	for function in TOPICS[topic][NESTED_FUNCTIONS].keys():
		nested_functions[function] = {ACTIONS: 0}

		for word in command.split():
			if word in TOPICS[topic][NESTED_FUNCTIONS][function][ACTIONS]:
				nested_functions[function][ACTIONS] += 1

		if not nested_functions[function][ACTIONS]:
			del nested_functions[function]

	return nested_functions


def _processing_functions(topics: dict) -> Topic:
	'''Обработка возможных функций темы и выявление наиболее подходящей'''

	if len(topics) == 0:
		return Topic()
	
	list_topics = tuple(topics.keys())
	handler_topic = list_topics[0]

	if len(topics) > 1 and not topics[handler_topic][FUNCTIONS]:
		# если было получено несколько тем и при этом у первой темы не была определена функция
		handler_topic = list_topics[1]

	if topics[handler_topic][FUNCTIONS]:
		# обработка темы у которой была выявлена функция

		if NESTED_FUNCTIONS not in topics[handler_topic].keys() or not topics[handler_topic][NESTED_FUNCTIONS]:
			# возвращение темы у которой нет вложенных функций
			states.ACTION_WITHOUT_FUNCTION = False
			return Topic(handler_topic, None)

		else:
			if len(topics[handler_topic][NESTED_FUNCTIONS].keys()) == 1:
				# возвращение темы у которой была выявлена только одна подходящая вложенная функция
				states.ACTION_WITHOUT_FUNCTION = False
				return Topic(
					topic = handler_topic, 
					functions = next(iter(topics[handler_topic][NESTED_FUNCTIONS]))
				)

			else:
				# определение наиболее подходящей вложенной функции из нескольких допустимых
				###
				result_function = {
					NAME: None,
					ACTIONS: 0,
					ADDITIONALLY: 0
				}

				for function in topics[handler_topic][NESTED_FUNCTIONS].keys():
					if topics[handler_topic][NESTED_FUNCTIONS][function][ACTIONS] > result_function[ACTIONS]:
						result_function = topics[handler_topic][NESTED_FUNCTIONS][function]
						result_function[NAME] = function

					elif topics[handler_topic][NESTED_FUNCTIONS][function][ADDITIONALLY] > result_function[ADDITIONALLY]:
						result_function = topics[handler_topic][NESTED_FUNCTIONS][function]
						result_function[NAME] = function

				if result_function[NAME]:
					# если определилась наиболее подходящая функция
					states.ACTION_WITHOUT_FUNCTION = False
					return Topic(
						topic = handler_topic, 
						functions = result_function[NAME]
					)
				else:
					return Topic()

	else:
		# обработка темы без функции (действие для темы)
		if not states.WAITING_RESPONSE:
			# Если ассистент не ожидает ответа в виде какого-то действия, то не дожидаться конечного результата распознавания речи
			states.ACTION_WITHOUT_FUNCTION = True

		return Topic(
			topic = handler_topic, 
			functions = next(iter(topics[handler_topic][NESTED_FUNCTIONS]))
		)
