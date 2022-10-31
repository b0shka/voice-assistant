from utils.logging import logger
from common.notifications import *
from common.states import states
from handlers.topics import TOPICS
from handlers.config import *
from handlers.performing_functions import PerformingFunctions
from domain.Topic import Topic
from domain.Determinate import NestedFunction, DeterminateTopic, DeterminateTopics


class Handler:

	def __init__(self):
		self.performing_functions = PerformingFunctions()


	def processing_command(self, command: str, default_topic: Topic | None = None, intended_topic: str | None = None):
		'''
			Выполение действия (функции) исходя из темы команды
		'''
		try:
			topic = default_topic
			if not topic:
				# если нет уже полученной темы (при получении промежуточных результатов распознавания речи), то определять ее "вручную"
				#topic = self.determinate_topic(command, intended_topic)
				topic = self.new_determinate_topic(command, intended_topic)

			return self.performing_functions.processing_topic(topic)

		except Exception as e:
			logger.error(e)


	def check_topic_on_singleness(self, topic: str) -> bool:
		'''
			Проверка промежуточной темы на вложенность в нее функций
		'''
		try:
			if not TOPICS[topic][NESTED_FUNCTIONS]:
				return True

			return False
		except Exception as e:
			logger.error(e)
			return False


	def new_determinate_topic(self, command: str, intended_topic: str | None = None) -> Topic | None:
		'''
			Определение темы комманды, по словам комманды
		'''
		try:
			topics = {}
			input_topics = None

			if not intended_topic:
				input_topics = TOPICS.keys()
			else:
				# добавление уже заранее подобранной темы запроса (при промежуточной результате распознавания речи)
				input_topics = (intended_topic,)

			for topic in input_topics:
				print(topic)
				#if topic not in topics.topics.n
				
		except Exception as e:
			logger.error(e)
			return None


	def determinate_topic(self, command: str, intended_topic: str | None = None) -> Topic | None:
		'''
			Определение темы комманды, по словам комманды
		'''
		try:
			topics = {}
			input_topics = None

			if not intended_topic:
				input_topics = TOPICS.keys()
			else:
				# добавление уже заранее подобранной темы запроса (при промежуточной результате распознавания речи)
				input_topics = (intended_topic,)

			for topic in input_topics:
				if topic not in topics.keys():
					topics[topic] = {FUNCTIONS: False}

				number_occurrences = []
				for word in command.split():
					# определение функций в команде
					if word != '':
						if type(TOPICS[topic][FUNCTIONS][0]) == tuple:
							# проверка на вхожение слов команды во все кортежи возможных слов (которые являются обязательными)
							for index, func in enumerate(TOPICS[topic][FUNCTIONS]):
								if index not in number_occurrences and word in func:
									number_occurrences.append(index)
						else:
							if word in TOPICS[topic][FUNCTIONS]:
								topics[topic][FUNCTIONS] = True
								break

				if type(TOPICS[topic][FUNCTIONS][0]) == tuple and len(number_occurrences) == len(TOPICS[topic][FUNCTIONS]):
					topics[topic][FUNCTIONS] = True

				if topics[topic][FUNCTIONS] and TOPICS[topic][NESTED_FUNCTIONS]:
					# определение действий и доп. слов в команде, если была выявлена функция и у этой темы ксть вложенные функции
					topics[topic][NESTED_FUNCTIONS] = {}

					for function in TOPICS[topic][NESTED_FUNCTIONS].keys():
						topics[topic][NESTED_FUNCTIONS][function] = {
							ACTIONS: 0,
							ADDITIONALLY: 0
						}

						for word in command.split():
							if word in TOPICS[topic][NESTED_FUNCTIONS][function][ACTIONS]:
								topics[topic][NESTED_FUNCTIONS][function][ACTIONS] += 1

							if word in TOPICS[topic][NESTED_FUNCTIONS][function][ADDITIONALLY]:
								topics[topic][NESTED_FUNCTIONS][function][ADDITIONALLY] += 1

						if not topics[topic][NESTED_FUNCTIONS][function][ACTIONS] and \
						not topics[topic][NESTED_FUNCTIONS][function][ADDITIONALLY]:
							del topics[topic][NESTED_FUNCTIONS][function]

				else:
					if states.get_topic() == topic and TOPICS[topic][NESTED_FUNCTIONS]:
						# обработка команды без функции, но по теме диалога
						topics[topic][NESTED_FUNCTIONS] = {}
						
						for function in TOPICS[topic][NESTED_FUNCTIONS].keys():
							topics[topic][NESTED_FUNCTIONS][function] = {ACTIONS: 0}

							for word in command.split():
								if word in TOPICS[topic][NESTED_FUNCTIONS][function][ACTIONS]:
									topics[topic][NESTED_FUNCTIONS][function][ACTIONS] += 1

							if not topics[topic][NESTED_FUNCTIONS][function][ACTIONS]:
								del topics[topic][NESTED_FUNCTIONS][function]

						if not topics[topic][NESTED_FUNCTIONS]:
							del topics[topic]

					elif not topics[topic][FUNCTIONS]:
						# удаление темы если в ней не была найдена функция
						del topics[topic]

			return self.processing_functions(topics)

		except Exception as e:
			logger.error(e)
			return None


	def processing_functions(self, topics: dict) -> Topic | None:
		'''
			Обработка возможных функций темы и выявление наиболее подходящей
		'''
		try:
			print(topics)
			if len(topics) == 0:
				return None
			
			list_keys = tuple(topics.keys())
			handler_topic = list_keys[0]

			if len(topics) > 1 and not topics[handler_topic][FUNCTIONS]:
				# если было получено несколько тем и при этом у первой темы не была определена функция
				###
				handler_topic = list_keys[1]

			if topics[handler_topic][FUNCTIONS]:
				# обработка темы у которой была выявлена функция

				if NESTED_FUNCTIONS not in topics[handler_topic].keys() or not topics[handler_topic][NESTED_FUNCTIONS]:
					# возвращение темы у которой нет вложенных функций
					states.change_action_without_function_state(False)
					return Topic(handler_topic, None)

				else:
					if len(topics[handler_topic][NESTED_FUNCTIONS].keys()) == 1:
						# возвращение темы у которой была выявлена только одна подходящая вложенная функция
						states.change_action_without_function_state(False)
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
							states.change_action_without_function_state(False)
							return Topic(
								topic = handler_topic, 
								functions = result_function[NAME]
							)
						else:
							return None

			else:
				# обработка темы без функции (действие для темы)
				if not states.get_waiting_response_state():
					# Если ассистент не ожидает ответа в виде какого-то действия, то не дожидаться конечного результата распознавания речи
					states.change_action_without_function_state(True)

				return Topic(
					topic = handler_topic, 
					functions = next(iter(topics[handler_topic][NESTED_FUNCTIONS]))
				)

		except Exception as e:
			logger.error(e)
			return None
