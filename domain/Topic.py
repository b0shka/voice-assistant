from dataclasses import dataclass


@dataclass
class Topic:
	topic: str
	functions: str | None