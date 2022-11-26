

class ErrConnectDB(Exception):
	'''Ошибка при подключении в базе данных'''

class ErrCreateTables(Exception):
	'''Ошибка при создании таблиц в базе данных'''

class ErrGetContacts(Exception):
	'''Ошибка при получении контактов из базы данных'''


class ErrAddTelegramMessage(Exception):
	'''Ошибка при добавлении сообщения из Телеграм в базу данных'''

class ErrGetTelegramMessages(Exception):
	'''Ошибка при получении сообщений Телеграм из базы данных'''

class ErrDeleteTelegramMessage(Exception):
	'''Ошибка при удалении сообщения из Телеграм в базе данных'''

class ErrDeleteTelegramMessages(Exception):
	'''Ошибка при удалении сообщений из Телеграм в базе данных'''


class ErrAddVKMessage(Exception):
	'''Ошибка при добавлении сообщения из ВКонтакте в базу данных'''

class ErrGetVKMessages(Exception):
	'''Ошибка при получении сообщений ВКонтакте из базы данных'''

class ErrDeleteVKMessage(Exception):
	'''Ошибка при удалении сообщения из ВКонтакте в базе данных'''

class ErrDeleteVKMessages(Exception):
	'''Ошибка при удалении сообщений из ВКонтакте в базе данных'''