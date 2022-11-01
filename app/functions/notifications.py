from utils.logging import logger
from common.states import states
from domain.enum_class.Errors import Errors
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite
from domain.data_class.Contact import Contact
from domain.enum_class.Services import Services


class Notifications:

	def __init__(self) -> None:
		self.db = DatabaseSQLite()


	def say_error(self, error: Errors) -> None:
		synthesis_text(error.value)


	def get_contact_by_contact_id(self, id: int) -> Contact | Errors:
		try:
			for contact in states.CONTACTS:
				if contact.id == id:
					return contact

			return Errors.NOT_FOUND_CONTACT_BY_BY
		except Exception as e:
			logger.error(e)
			return Errors.GET_CONTACT_BY_CONTACT_ID


	def viewing_notifications(self) -> None:
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
			self.say_error(Errors.VIEWING_NOTIFICATIONS)
			logger.error(e)


	def clean_notifications(self) -> None:
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


	def viewing_messages(self, service: Services) -> None:
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
							case Errors.GET_CONTACT_BY_CONTACT_ID:
								self.say_error(contact)
								
							case Errors.NOT_FOUND_CONTACT_BY_BY:
								answer = f'Сообщение от неизвестного контакта {message.first_name}'
								if message.last_name:
									answer += f' {message.last_name}'
								
								answer += f'. {message.text}'
								synthesis_text(answer)

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
			self.say_error(Errors.VIEWING_MESSAGES)
			logger.error(e)


	def clean_messages(self, service: Services) -> None:
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
