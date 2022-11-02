

class ErrConnectVK(Exception):
	'''Ошибка при подключении к ВКонтакте'''

class ErrGetNewVKMessages(Exception):
	'''Ошибка при получении нового сообщения в ВКонтакте'''

class ErrSendVKMessage(Exception):
	'''Ошибка при отправке сообщения в ВКонтакте'''

class CantGetUserData(Exception):
	'''Не удалось получить информации об аккаунте в ВКонтакте'''

class ErrGetUserData(Exception):
	'''Ошибка при получении информации об аккаунте в ВКонтакте'''