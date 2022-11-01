from typing import NamedTuple


class Message(NamedTuple):
	text: str
	contact_id: int | None = None
	from_id: int | None = None
	first_name: str | None = None
	last_name: str | None = None