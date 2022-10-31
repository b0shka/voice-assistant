from typing import NamedTuple
from domain.enum_class.CommandMode import CommandMode


class Command(NamedTuple):
	text: str | None
	mode: CommandMode