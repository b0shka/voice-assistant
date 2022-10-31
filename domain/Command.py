from dataclasses import dataclass


@dataclass
class Command:
	text: str | None
	mode: str