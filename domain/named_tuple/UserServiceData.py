from typing import NamedTuple


class VKUserData(NamedTuple):
	id: int
	first_name: str
	last_name: str


class TelegramUserData(NamedTuple):
	id: int
	first_name: str
	last_name: str | None
	phone: int | None