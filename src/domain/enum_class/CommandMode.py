from enum import Enum


class CommandMode(Enum):
	'''Типы команд возвращаемых функцией распознавания голоса'''
	FINITE = 'finite'
	INTERMEDIATE = 'intermediate'