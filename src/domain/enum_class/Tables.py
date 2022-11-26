from enum import Enum


class TablesDB(Enum):
	'''Названия таблиц в базе данных sqlite'''

	TELEGRAM_MESSAGES = 'telegram_messages'
	VK_MESSAGES = 'vk_messages'
	YANDEX_MESSAGES = 'yandex_messages'
	CONTACTS = 'contacts'