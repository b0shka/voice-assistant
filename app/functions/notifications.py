from utils.logging import logger
from common.states import states
from common.errors import *
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite
from domain.data_class.Contact import Contact
from domain.enum_class.Services import Services


class Notifications:

	def __init__(self):
		self.db = DatabaseSQLite()


	def get_contact_by_id(self, id: int) -> Contact | int:
		try:
			if not id:
				return 0

			for contact in states.CONTACTS:
				if contact.id == id:
					return contact

			return 0
		except Exception as e:
			logger.error(e)
			return -1


	def viewing_notifications(self):
		try:
			count_telegram_messages = str(len(states.NOTIFICATIONS.telegram_messages))
			if int(count_telegram_messages):
				if count_telegram_messages[-1] == '1':
					answer = 'У вас одно новое сообщение в Телеграм'
				elif count_telegram_messages[-1] in ('2', '3', '4'):
					answer = f'У вас {count_telegram_messages} новых сообщения в Телеграм'
				else:
					answer = f'У вас {count_telegram_messages} новых сообщений в Телеграм'

				synthesis_text(answer)

			count_vk_messages = str(len(states.NOTIFICATIONS.vk_messages))
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
			states.NOTIFICATIONS.telegram_messages.clear()
			states.NOTIFICATIONS.vk_messages.clear()

			result = self.db.delete_telegram_messages()
			if not result:
				logger.error(ERROR_DELETE_TELEGRAM_MESSAGES)

			result = self.db.delete_vk_messages()
			if not result:
				logger.error(ERROR_DELETE_VK_MESSAGES)

			synthesis_text('Уведомления очищены')
		except Exception as e:
			logger.error(e)


	def viewing_messages(self, service: Services):
		try:
			messages = None

			match service:
				case Services.TELEGRAM:
					messages = states.NOTIFICATIONS.telegram_messages

				case Services.VK:
					messages = states.NOTIFICATIONS.vk_messages

			if len(messages):
				for message in messages:
					###
					if message.first_name:
						answer = ''

						if message.contact_id:
							answer = f'Сообщение от контакта {message.first_name}'
						else:
							answer = f'Сообщение от пользователя {message.first_name}'

						if message.last_name:
							answer += f' {message.last_name}'
						
						answer += f'. {message.text}'
						synthesis_text(answer)
						
					else:
						match self.get_contact_by_id(message.contact_id):
							case 0:
								pass
								#answer = f'Сообщение от пользователя {message.first_name}'
								#if message.last_name:
								#	answer += f' {message.last_name}'
								
								#answer += f'. {message.text}'
								#synthesis_text(answer)

							case -1:
								logger.error(ERROR_GET_CONTACT_BY_CONTACT_ID)

							case contact if type(contact) == Contact:
								###
								answer = f'Сообщение от контакта {contact.first_name}'
								if contact.last_name:
									answer += f' {contact.last_name}'
								
								answer += f'. {message.text}'
								synthesis_text(answer)

			else:
				match service:
					case Services.TELEGRAM:
						synthesis_text('У вас нет новых сообщений в Телеграм')
					case Services.VK:
						synthesis_text('У вас нет новых сообщений в Вконтакте')

		except Exception as e:
			logger.error(e)


	def clean_messages(self, service: Services):
		try:
			match service:
				case Services.TELEGRAM:
					states.NOTIFICATIONS.telegram_messages.clear()
				case Services.VK:
					states.NOTIFICATIONS.vk_messages.clear()
			result = None

			match service:
				case Services.TELEGRAM:
					result = self.db.delete_telegram_messages()
				case Services.VK:
					result = self.db.delete_vk_messages()

			if not result:
				logger.error(ERROR_DELETE_TELEGRAM_MESSAGES)

			match service:
				case Services.TELEGRAM:
					synthesis_text('Новые сообщения в Телеграм очищены')
				case Services.VK:
					synthesis_text('Новые сообщения в Вконтакте очищены')

		except Exception as e:
			logger.error(e)