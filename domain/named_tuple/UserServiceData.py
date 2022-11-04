from typing import NamedTuple


class VKUserData(NamedTuple):
	'''Данные пользователя ВКонтакте, полученные с помощью vk_api'''

	id: int
	first_name: str
	last_name: str


class TelegramUserData(NamedTuple):
	'''Данные пользователя Телеграм, полученные с помощью telethon'''

	id: int
	first_name: str
	last_name: str | None
	phone: int | None