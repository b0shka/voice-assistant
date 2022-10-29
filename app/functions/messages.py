from common.config import *
from common.errors import *
from common.notifications import *
from common.states import states
from domain.Message import Message
from utils.logging import logger
from database.database_sqlite import DatabaseSQLite
from utils.speech.yandex_synthesis import synthesis_text


class Messages:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
		except Exception as e:
			logger.error(e)


	def get_contact_by_from_id(self, id, service):
		try:
			for contact in states.get_contacts():
				if service == TELEGRAM_MESSAGES_NOTIFICATION:
					if contact[4] == id:
						return contact
				
				elif service == VK_MESSAGES_NOTIFICATION:
					if contact[5] == id:
						return contact

			return 0
		except Exception as e:
			logger.error(e)
			return -1


	def telegram_message(self, message):
		'''
			Обработка полученного нового сообщения из Телеграм
		'''
		try:
			# тут будет ошибка, если сообщение отправлено не от человека, а от канала или чата
			from_id = int(message['from_id']['user_id'])
			
			match self.get_contact_by_from_id(from_id):
				case -1:
					logger.error(ERROR_GET_CONTACT_BY_TELEGRAM_ID)

				case 0:
					pass 
					# сообщение не от контакта или от канала/чата

				case contact if type(contact) == tuple:
					if not states.get_mute_state():
						answer = f'У вас новое сообщение в Телеграм от контакта {contact[1]}'
						if contact[2]:
							answer += f' {contact[2]}'
						synthesis_text(answer)

					states.change_notifications(
						TELEGRAM_MESSAGES_NOTIFICATION, 
						Message(
							message = message['message'],
							contact_id = contact[0],
							first_name = contact[1],
							last_name = contact[2]
						)
					)

					result = self.db.add_telegram_message(
						message = message['message'], 
						contact_id = contact[0],
						first_name = contact[1],
						last_name = contact[2]
					)
					if result == 0:
						logger.error(ERROR_ADD_TELEGRAM_MESSAGE)
		except Exception as e:
			logger.error(e)


	def vk_message(self, event):
		'''
			Обработка полученного нового сообщения из ВКонтакте
		'''
		try:
			if event.from_user:
				match self.get_contact_by_from_id(event.user_id):
					case -1:
						logger.error(ERROR_GET_CONTACT_BY_VK_ID)

					case 0:
						match self.get_user_data_by_id(event.user_id):
							case 0:
								logger.error(FAILED_GET_USER_DATA_BY_ID)
							case -1:
								logger.error(ERROR_GET_USER_DATA_BY_ID)

							case user if type(user) == dict:
								print(user)
								if not states.get_mute_state():
									answer = f'У вас новое сообщение в Вконтакте от пользователя {user["first_name"]}'
									if user["last_name"]:
										answer += f' {user["last_name"]}'
									synthesis_text(answer)

								states.change_notifications(
									VK_MESSAGES_NOTIFICATION, 
									Message(
										message = event.text,
										first_name = user['first_name'],
										last_name = user['last_name']
									)
								)

								result = self.db.add_vk_message(
									message = event.text, 
									from_id = event.user_id,
									first_name = user['first_name'],
									last_name = user['last_name']
								)
								if result == 0:
									logger.error(ERROR_ADD_VK_MESSAGE)

					case contact if type(contact) == tuple:
						if not states.get_mute_state():
							answer = f'У вас новое сообщение в Вконтакте от контакта {contact[1]}'
							if contact[2]:
								answer += f' {contact[2]}'
							synthesis_text(answer)

						states.change_notifications(
							VK_MESSAGES_NOTIFICATION, 
							Message(
								message = event.text,
								contact_id = contact[0],
								first_name = contact[1],
								last_name = contact[2]
							)
						)

						result = self.db.add_vk_message(
							message = event.text, 
							contact_id = contact[0],
							first_name = contact[1],
							last_name = contact[2]
						)
						if result == 0:
							logger.error(ERROR_ADD_VK_MESSAGE)

			elif event.from_chat:
				print('новое сообщение из чата')

		except Exception as e:
			logger.error(e)