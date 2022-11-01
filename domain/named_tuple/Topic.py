from typing import NamedTuple
from domain.enum_class.TopicsNames import TopicsNames
from domain.enum_class.FunctionsNames import FunctionsNames


class Topic(NamedTuple):
	topic: TopicsNames | None = None
	functions: FunctionsNames | None = None