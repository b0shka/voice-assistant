from utils.logging import logger
from common.states import states
from domain.enum_class.Errors import Errors
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite
from domain.data_class.Contact import Contact
from domain.enum_class.Services import Services


class Notifications:

	def __init__(self):
		self.db = DatabaseSQLite()


	def say_error(self, error: Errors) -> None:
		synthesis_text(error.value)


	def get_contact_by_contact_id(self, id: int) -> Contact | Errors | int:
		try:
			###
			if not id:
				return 0

			for contact in states.CONTACTS:
				if contact.id == id:
					return contact

			return 0
		except Exception as e:
			logger.error(e)
			return Errors.GET_CONTACT_BY_CONTACT_ID


	def viewing_notifications(self):
		try:
			count_telegram_messages = len(states.NOTIFICATIONS.telegram_messages)
			if int(count_telegram_messages):
				match str(count_telegram_messages)[-1]:
					case '1':
						answer = 'У вас одно новое сообщение в Телеграм'
					case '2' | '3' | '4':
						answer = f'У вас {count_telegram_messages} новых сообщения в Телеграм'
					case _:
						answer = f'У вас {count_telegram_messages} новых сообщений в Телеграм'

				synthesis_text(answer)

			count_vk_messages = len(states.NOTIFICATIONS.vk_messages)
			if int(count_vk_messages):
				match str(count_vk_messages)[-1]:
					case '1':
						answer = 'У вас одно новое сообщение в Вконтакте'
					case '2' | '3' | '4':
						answer = f'У вас {count_vk_messages} новых сообщения в Вконтакте'
					case _:
						answer = f'У вас {count_vk_messages} новых сообщений в Вконтакте'

				synthesis_text(answer)

			if not count_telegram_messages and not count_vk_messages:
				synthesis_text('У вас пока нет уведомлений')

		except Exception as e:
			self.say_error(Errors.VIEWING_NOTIFICATIONS)
			logger.error(e)


	def clean_notifications(self):
		try:
			states.NOTIFICATIONS.telegram_messages.clear()
			states.NOTIFICATIONS.vk_messages.clear()

			error = self.db.delete_telegram_messages()
			if isinstance(error, Errors):
				self.say_error(error)

			error = self.db.delete_vk_messages()
			if isinstance(error, Errors):
				self.say_error(error)

			synthesis_text('Уведомления очищены')

		except Exception as e:
			self.say_error(Errors.CLEAN_NOTIFICATIONS)
			logger.error(e)


	def viewing_messages(self, service: Services):
		try:
			match service:
				case Services.TELEGRAM:
					messages = states.NOTIFICATIONS.telegram_messages
				case Services.VK:
					messages = states.NOTIFICATIONS.vk_messages

			if len(messages):
				for message in messages:
					###
					if message.first_name:
						if message.contact_id:
							answer = f'Сообщение от контакта {message.first_name}'
						else:
							answer = f'Сообщение от пользователя {message.first_name}'

						if message.last_name:
							answer += f' {message.last_name}'
						
						answer += f'. {message.text}'
						synthesis_text(answer)
						
					else:
						match self.get_contact_by_contact_id(message.contact_id):
							case 0:
								pass
								#answer = f'Сообщение от пользователя {message.first_name}'
								#if message.last_name:
								#	answer += f' {message.last_name}'
								
								#answer += f'. {message.text}'
								#synthesis_text(answer)

							case contact if isinstance(contact, Errors):
								self.say_error(contact)

							case contact if isinstance(contact, Contact):
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
			self.say_error(Errors.VIEWING_MESSAGES)
			logger.error(e)


	def clean_messages(self, service: Services):
		try:
			match service:
				case Services.TELEGRAM:
					error = self.db.delete_telegram_messages()
					if isinstance(error, Errors):
						self.say_error(error)
					else:
						states.NOTIFICATIONS.telegram_messages.clear()
						synthesis_text('Новые сообщения в Телеграм очищены')

				case Services.VK:
					error = self.db.delete_vk_messages()
					if isinstance(error, Errors):
						self.say_error(error)
					else:
						states.NOTIFICATIONS.vk_messages.clear()
						synthesis_text('Новые сообщения в Вконтакте очищены')

		except Exception as e:
			self.say_error(Errors.CLEAN_MESSAGES)
			logger.error(e)
