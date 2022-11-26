from typing import NamedTuple


class Message(NamedTuple):
	'''Хранение данных сообщения полученного из добавленных сервисов, по которым происходит мониторинг на новые сообщения'''

	text: str
	from_id: int
	contact_id: int | None = None
	first_name: str | None = None
	last_name: str | None = None