from enum import Enum


class Errors(Enum):

	# Database
	CONNECT_DB = 'Ошибка при подключении в базе данных'
	CREATE_TABLES = 'Ошибка при создании таблиц в базе данных'
	
	# Contacts
	GET_CONTACTS = 'Ошибка при получении контактов из базы данных'
	UPDATE_CONTACT = 'Ошибка при обновлении контактов'

	GET_CONTACT_BY_CONTACT_ID = 'Ошибка при получении контакта по contact_id'
	GET_CONTACT_BY_TELEGRAM_ID = 'Ошибка при получении контакта по telegram_id'
	GET_CONTACT_BY_VK_ID = 'Ошибка при получении контакта по vk_id'

	# Telegram
	ADD_TELEGRAM_MESSAGE = 'Ошибка при добавлении сообщения из Телеграм в базу данных'
	GET_TELEGRAM_MESSAGES = 'Ошибка при получении сообщений Телеграм из базы данных'
	DELETE_TELEGRAM_MESSAGE = 'Ошибка при удалении сообщения из Телеграм в базе данных'
	DELETE_TELEGRAM_MESSAGES = 'Ошибка при удалении сообщений из Телеграм в базе данных'

	# VK
	ADD_VK_MESSAGE = 'Ошибка при добавлении сообщения из ВКонтакте в базу данных'
	GET_VK_MESSAGES = 'Ошибка при получении сообщений ВКонтакте из базы данных'
	DELETE_VK_MESSAGE = 'Ошибка при удалении сообщения из ВКонтакте в базе данных'
	DELETE_VK_MESSAGES = 'Ошибка при удалении сообщений из ВКонтакте в базе данных'

	GET_USER_DATA_BY_ID = 'Ошибка при получении информации об аккаунте по id в ВК'
	FAILED_GET_USER_DATA_BY_ID = 'Не удалось получить об аккаунте по id в ВК'

	# Requests, answers
	ADD_REQUEST_ANSWER = 'Ошибка при добавлении запроса/ответа в БД'
	CLEAN_OLD_REQUESTS_ANSWERS = 'Ошибка при очищении старых запросов/ответов в БД'

	# Other
	SERVER = 'Ошибка на стороне сервера'