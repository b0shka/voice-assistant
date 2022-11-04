from typing import NamedTuple
from domain.enum_class.CommandMode import CommandMode


class Command(NamedTuple):
	'''Хранения результатов распознования голосовой команды'''

	text: str | None
	mode: CommandMode