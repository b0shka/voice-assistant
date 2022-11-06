from common.states import states
from common.exceptions.contacts import CantFoundContact
from common.exceptions.notifications import ErrConvertMessage
from common.exceptions.database import *
from domain.repository.database_sqlite import DatabaseSQLite
from domain.named_tuple.Contact import Contact
from domain.named_tuple.Message import Message
from domain.enum_class.Services import Services
from domain.enum_class.Errors import Errors
from utils.speech.yandex_synthesis import synthesis_text
from app.functions.communications import say_error


class Notifications:

	def __init__(self, db: DatabaseSQLite) -> None:
		self.db = db


	def _get_contact_by_contact_id(self, id: int) -> Contact:
		for contact in states.CONTACTS:
			if contact.id == id:
				return contact
		else:
			raise CantFoundContact

		
	def update_notifications(self, isLauch: bool = False) -> None:
		'''Добавление уведомлений (если такие существуют) в глобальное состояние'''

		self._update_telegram_messages()
		self._update_vk_messages()
			
		if not isLauch:
			synthesis_text('Уведомления успешно обновлены')


	def _update_vk_messages(self) -> None:
		try:
			vk_messages = self.db.get_vk_messages()

			for message in vk_messages:
				states.NOTIFICATIONS.vk_messages.append(
					self._convert_message(message)
				)

		except (ErrGetVKMessages, ErrConvertMessage) as e:
			say_error(e)


	def _update_telegram_messages(self) -> None:
		try:
			telegram_messages = self.db.get_telegram_messages()

			for message in telegram_messages:
				states.NOTIFICATIONS.telegram_messages.append(
					self._convert_message(message)
				)

		except (ErrGetTelegramMessages, ErrConvertMessage) as e:
			say_error(e)


	def _convert_message(self, message: list) -> Message:
		try:
			return Message(
				text = message[1],
				contact_id = message[2],
				from_id = message[3],
				first_name = message[4],
				last_name = message[5]
			)

		except IndexError:
			raise ErrConvertMessage(Errors.CONVERT_MESSAGE.value)


	def viewing_notifications(self) -> None:
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


	def clean_notifications(self) -> None:
		states.NOTIFICATIONS.telegram_messages.clear()
		states.NOTIFICATIONS.vk_messages.clear()

		try:
			self.db.delete_telegram_messages()
			self.db.delete_vk_messages()
		except (ErrDeleteTelegramMessages, ErrDeleteVKMessages) as e:
			say_error(e)

		synthesis_text('Уведомления очищены')


	def viewing_messages(self, service: Services) -> None:
		###
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
					try:
						contact = self._get_contact_by_contact_id(message.contact_id)
					except CantFoundContact:
						synthesis_text(f'Сообщение от неизвестного контакта. {message.text}')
						
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


	def clean_messages(self, service: Services) -> None:
		match service:
			case Services.TELEGRAM:
				try:
					self.db.delete_telegram_messages()
				except ErrDeleteTelegramMessages as e:
					say_error(e)
				states.NOTIFICATIONS.telegram_messages.clear()
				synthesis_text('Новые сообщения в Телеграм очищены')

			case Services.VK:
				try:
					self.db.delete_vk_messages()
				except ErrDeleteVKMessages as e:
					say_error(e)
				states.NOTIFICATIONS.vk_messages.clear()
				synthesis_text('Новые сообщения в Вконтакте очищены')
