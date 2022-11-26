from enum import Enum


class ActionsAssistant(Enum):
	'''Возможные действия возвращаемые ассистентом после обработки команды и вызова функции'''
	EXIT = 'exit'