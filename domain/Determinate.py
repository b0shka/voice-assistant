from dataclasses import dataclass
from typing import List


@dataclass
class NestedFunction:
	name: str
	key: str
	value: int


@dataclass
class DeterminateTopic:
	name: str
	function: bool
	nested_functions: List[NestedFunction]


@dataclass
class DeterminateTopics:
	topics: List[DeterminateTopic]