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


	def get_contact_by_contact_id(self, id: int) -> Contact | Errors:
		try:
			for contact in states.CONTACTS:
				if contact.id == id:
					return contact

			return Errors.NOT_FOUND_CONTACT_BY_BY
		except Exception as e:
			logger.error(e)
			return Errors.GET_CONTACT_BY_CONTACT_ID


	def viewing_notifications(self):
		try:
			empty_notifications = True

			for service in Services:
				match service:
					case Services.TELEGRAM:
						count_messages = len(states.NOTIFICATIONS.telegram_messages)
						service_name = 'Телеграм'
					case Services.VK:
						count_messages = len(states.NOTIFICATIONS.vk_messages)
						service_name = 'ВКонтакте'

				if count_messages:
					match str(count_messages)[-1]:
						case '1':
							answer = f'У вас одно новое сообщение в {service_name}'
						case '2' | '3' | '4':
							answer = f'У вас {count_messages} новых сообщения в {service_name}'
						case _:
							answer = f'У вас {count_messages} новых сообщений в {service_name}'

					empty_notifications = False
					synthesis_text(answer)

			if empty_notifications:
				synthesis_text('У вас пока нет уведомлений')

		except Exception as e:
			synthesis_text(Errors.VIEWING_NOTIFICATIONS.value)
			logger.error(e)


	def clean_notifications(self):
		try:
			states.NOTIFICATIONS.telegram_messages.clear()
			states.NOTIFICATIONS.vk_messages.clear()

			error = self.db.delete_telegram_messages()
			if isinstance(error, Errors):
				synthesis_text(error.value)

			error = self.db.delete_vk_messages()
			if isinstance(error, Errors):
				synthesis_text(error.value)

			synthesis_text('Уведомления очищены')

		except Exception as e:
			synthesis_text(Errors.CLEAN_NOTIFICATIONS.value)
			logger.error(e)


	def viewing_messages(self, service: Services):
		try:
			match service:
				case Services.TELEGRAM:
					messages = states.NOTIFICATIONS.telegram_messages
				case Services.VK:
					messages = states.NOTIFICATIONS.vk_messages

			for message in messages:
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
					if message.contact_id:
						contact = self.get_contact_by_contact_id(message.contact_id)
						
						match contact:
							case Errors.NOT_FOUND_CONTACT_BY_BY:
								answer = f'Сообщение от неизвестного контакта {message.first_name}'
								if message.last_name:
									answer += f' {message.last_name}'
								
								answer += f'. {message.text}'
								synthesis_text(answer)

							case Errors.GET_CONTACT_BY_CONTACT_ID:
								synthesis_text(contact.value)

							case contact if isinstance(contact, Contact):
								answer = f'Сообщение от контакта {contact.first_name}'
								if contact.last_name:
									answer += f' {contact.last_name}'

								answer += f'. {message.text}'
								synthesis_text(answer)

					else:
						pass # get by from_id with vk api

			if not len(messages):
				match service:
					case Services.TELEGRAM:
						synthesis_text('У вас нет новых сообщений в Телеграм')
					case Services.VK:
						synthesis_text('У вас нет новых сообщений в Вконтакте')

		except Exception as e:
			synthesis_text(Errors.VIEWING_MESSAGES.value)
			logger.error(e)


	def clean_messages(self, service: Services):
		try:
			match service:
				case Services.TELEGRAM:
					error = self.db.delete_telegram_messages()
					if isinstance(error, Errors):
						synthesis_text(error.value)
					else:
						states.NOTIFICATIONS.telegram_messages.clear()
						synthesis_text('Новые сообщения в Телеграм очищены')

				case Services.VK:
					error = self.db.delete_vk_messages()
					if isinstance(error, Errors):
						synthesis_text(error.value)
					else:
						states.NOTIFICATIONS.vk_messages.clear()
						synthesis_text('Новые сообщения в Вконтакте очищены')

		except Exception as e:
			synthesis_text(Errors.CLEAN_MESSAGES.value)
			logger.error(e)
