from enum import Enum


class Errors(Enum):

	# Database
	CONNECT_DB = 'Ошибка при подключении в базе данных'
	CREATE_TABLES = 'Ошибка при создании таблиц в базе данных'

	# Handler
	DETERMINATE_TOPIC = 'Ошибка при определении темы команды'
	PROCESSING_FUNCTIONS = 'Ошибка при обработке вложенных функций темы'
	CHECK_NESTED_FUNCTIONS = 'Ошибка при проверки на существование вложенных функций в теме'
	PROCESSING_TOPIC = 'Ошибка при обработке полученной темы и вызове функции'

	# Notifications
	VIEWING_NOTIFICATIONS = 'Ошибка при просмотре уведомлений'
	CLEAN_NOTIFICATIONS = 'Ошибка при очищении уведомлений'
	VIEWING_MESSAGES = 'Ошибка при просмотре соощений'
	CLEAN_MESSAGES = 'Ошибка при просмотре сообщений'
	
	# Contacts
	GET_CONTACTS = 'Ошибка при получении контактов из базы данных'
	UPDATE_CONTACT = 'Ошибка при обновлении контактов'
	GET_CONTACT_BY_CONTACT_ID = 'Ошибка при получении контакта по contact_id'
	NOT_FOUND_CONTACT_BY_BY = 'Не удалось найти контакт по id'
	GET_CONTACT_BY_TELEGRAM_ID = 'Ошибка при получении контакта по telegram_id'
	GET_CONTACT_BY_VK_ID = 'Ошибка при получении контакта по vk_id'

	# Telegram
	ADD_TELEGRAM_MESSAGE = 'Ошибка при добавлении сообщения из Телеграм в базу данных'
	GET_TELEGRAM_MESSAGES = 'Ошибка при получении сообщений Телеграм из базы данных'
	DELETE_TELEGRAM_MESSAGE = 'Ошибка при удалении сообщения из Телеграм в базе данных'
	DELETE_TELEGRAM_MESSAGES = 'Ошибка при удалении сообщений из Телеграм в базе данных'
	CONNECT_TELEGRAM = 'Ошибка при подключении к Телеграм'
	GET_NEW_TELEGRAM_MESSAGES = 'Ошибка при получении нового сообщения в Телеграм'
	PROCESSING_NEW_TELEGRAM_MESSAGE = 'Ошибка при обработке нового сообщения в Телеграм'
	SEND_TELEGRAM_MESSAGE = 'Ошибка при отправке сообщения в Телеграм'
	GET_USER_DATA_TELEGRAM_BY_ID = 'Ошибка при получении информации об аккаунте в Телеграм'

	# VK
	ADD_VK_MESSAGE = 'Ошибка при добавлении сообщения из ВКонтакте в базу данных'
	GET_VK_MESSAGES = 'Ошибка при получении сообщений ВКонтакте из базы данных'
	DELETE_VK_MESSAGE = 'Ошибка при удалении сообщения из ВКонтакте в базе данных'
	DELETE_VK_MESSAGES = 'Ошибка при удалении сообщений из ВКонтакте в базе данных'
	CONNECT_VK = 'Ошибка при подключении к ВКонтакте'
	GET_NEW_VK_MESSAGES = 'Ошибка при получении нового сообщения в ВКонтакте'
	PROCESSING_NEW_VK_MESSAGE = 'Ошибка при обработке нового сообщения в ВКонтакте'
	SEND_VK_MESSAGE = 'Ошибка при отправке сообщения в ВКонтакте'
	GET_USER_DATA_VK_BY_ID = 'Ошибка при получении информации об аккаунте в ВКонтакте'
	FAILED_GET_USER_DATA_VK_BY_ID = 'Не удалось получить информации об аккаунте в ВКонтакте'