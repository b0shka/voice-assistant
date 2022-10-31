

from enum import Enum


class TablesDB(Enum):
	TELEGRAM_MESSAGES = 'telegram_messages'
	VK_MESSAGES = 'vk_messages'
	YANDEX_MESSAGES = 'yandex_messages'
	CONTACTS = 'contacts'