from typing import NamedTuple
from handlers.functions_names import TopicsNames, FunctionsNames


class Topic(NamedTuple):
	topic: TopicsNames | None = None
	functions: FunctionsNames | None = None