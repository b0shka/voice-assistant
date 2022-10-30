from utils.logging import logger
from common.states import states
from common.errors import *
from common.notifications import *
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite


class Notifications:

	def __init__(self):
		self.db = DatabaseSQLite()


	def get_contact_by_id(self, id):
		try:
			if not id:
				return 0

			for contact in states.get_contacts():
				if contact[0] == id:
					return contact

			return 0
		except Exception as e:
			logger.error(e)
			return -1


	def viewing_notifications(self):
		try:
			notifications = states.get_notifications()

			count_telegram_messages = str(len(notifications[TELEGRAM_MESSAGES_NOTIFICATION]))
			if int(count_telegram_messages):
				if count_telegram_messages[-1] == '1':
					answer = 'У вас одно новое сообщение в Телеграм'
				elif count_telegram_messages[-1] in ('2', '3', '4'):
					answer = f'У вас {count_telegram_messages} новых сообщения в Телеграм'
				else:
					answer = f'У вас {count_telegram_messages} новых сообщений в Телеграм'

				synthesis_text(answer)

			count_vk_messages = str(len(notifications[VK_MESSAGES_NOTIFICATION]))
			if int(count_vk_messages):
				if count_vk_messages[-1] == '1':
					answer = 'У вас одно новое сообщение в Вконтакте'
				elif count_vk_messages[-1] in ('2', '3', '4'):
					answer = f'У вас {count_vk_messages} новых сообщения в Вконтакте'
				else:
					answer = f'У вас {count_vk_messages} новых сообщений в Вконтакте'

				synthesis_text(answer)

			if not int(count_telegram_messages) and not int(count_vk_messages):
				answer = 'У вас пока нет уведомлений'
				synthesis_text(answer)

		except Exception as e:
			logger.error(e)


	def clean_notifications(self):
		try:
			states.clean_notifications(TELEGRAM_MESSAGES_NOTIFICATION)
			states.clean_notifications(VK_MESSAGES_NOTIFICATION)

			result = self.db.delete_telegram_messages()
			if not result:
				logger.error(ERROR_DELETE_TELEGRAM_MESSAGES)

			result = self.db.delete_vk_messages()
			if not result:
				logger.error(ERROR_DELETE_VK_MESSAGES)

			synthesis_text('Уведомления очищены')
		except Exception as e:
			logger.error(e)


	def viewing_messages(self, service):
		try:
			messages = states.get_notifications_by_type(service)

			if len(messages):
				for message in messages:
					if message.first_name:
						answer = ''

						if message.contact_id:
							answer = f'Сообщение от контакта {message.first_name}'
						else:
							answer = f'Сообщение от пользователя {message.first_name}'

						if message.last_name:
							answer += f' {message.last_name}'
						
						answer += f'. {message.message}'
						synthesis_text(answer)
						
					else:
						match self.get_contact_by_id(message.contact_id):
							case 0:
								answer = f'Сообщение от неизвестного пользователя {message.first_name}'
								if message.last_name:
									answer += f' {message.last_name}'
								
								answer += f'. {message.message}'
								synthesis_text(answer)

							case -1:
								logger.error(ERROR_GET_CONTACT_BY_CONTACT_ID)

							case contact if type(contact) == tuple:
								answer = f'Сообщение от контакта {contact[1]}'
								if contact[2]:
									answer += f' {contact[2]}'
								
								answer += f'. {message.message}'
								synthesis_text(answer)
			else:
				if service == TELEGRAM_MESSAGES_NOTIFICATION:
					synthesis_text('У вас нет новых сообщений в Телеграм')
				elif service == VK_MESSAGES_NOTIFICATION:
					synthesis_text('У вас нет новых сообщений в Вконтакте')

		except Exception as e:
			logger.error(e)


	def clean_messages(self, service):
		try:
			states.clean_notifications(service)
			result = None

			if service == TELEGRAM_MESSAGES_NOTIFICATION:
				result = self.db.delete_telegram_messages()
			elif service == VK_MESSAGES_NOTIFICATION:
				result = self.db.delete_vk_messages()

			if not result:
				logger.error(ERROR_DELETE_TELEGRAM_MESSAGES)

			if service == TELEGRAM_MESSAGES_NOTIFICATION:
				synthesis_text('Новые сообщения в Телеграм очищены')
			elif service == VK_MESSAGES_NOTIFICATION:
				synthesis_text('Новые сообщения в Вконтакте очищены')

		except Exception as e:
			logger.error(e)