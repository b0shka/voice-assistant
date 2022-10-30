from dataclasses import dataclass


@dataclass
class Message:
	text: str
	contact_id: int | None = None
	from_id: int | None = None
	first_name: str | None = None
	last_name: str | None = None