from common.config import *
from common.states import states
from domain.named_tuple.Contact import Contact
from domain.named_tuple.Message import Message
from domain.enum_class.Errors import Errors
from domain.enum_class.Services import Services
from data.database_sqlite import DatabaseSQLite
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text
from common.exceptions.messages import CantFoundContact
from app.functions.communications import say_error


class Messages:

	def __init__(self) -> None:
		self.db = DatabaseSQLite()


	def get_contact_by_from_id(self, id: int, service: Services) -> Contact:
		for contact in states.CONTACTS:
			if service == Services.TELEGRAM:
				if contact.telegram_id == id:
					return contact
			
			elif service == Services.VK:
				if contact.vk_id == id:
					return contact
		else:
			raise CantFoundContact


	def new_telegram_message(self, message: dict) -> None:
		'''Обработка полученного нового сообщения из Телеграм'''

		try:
			# тут будет ошибка, если сообщение отправлено не от человека, а от канала или чата
			from_id = int(message['from_id']['user_id'])
			contact = self.get_contact_by_from_id(from_id, Services.TELEGRAM)
			
			if not states.MUTE:
				answer = f'У вас новое сообщение в Телеграм от контакта {contact.first_name}'
				if contact.last_name:
					answer += f' {contact.last_name}'
				synthesis_text(answer)

			new_message = Message(
				text = message['message'],
				contact_id = contact.id,
				first_name = contact.first_name,
				last_name = contact.last_name
			)

			states.NOTIFICATIONS.telegram_messages.append(new_message)
			self.db.add_telegram_message(new_message)

		except CantFoundContact:
			# сообщение не от контакта
			pass

		except Exception as e:
			say_error(Errors.PROCESSING_NEW_TELEGRAM_MESSAGE)
			logger.error(e)


	def new_vk_message(self, event) -> None:
		'''Обработка полученного нового сообщения из ВКонтакте'''

		try:
			if event.from_user:
				contact = self.get_contact_by_from_id(event.user_id, Services.VK)

				if not states.MUTE:
					answer = f'У вас новое сообщение в Вконтакте от контакта {contact.first_name}'
					if contact.last_name:
						answer += f' {contact.last_name}'
					synthesis_text(answer)

				new_message = Message(
					text = event.text,
					contact_id = contact.id,
					first_name = contact.first_name,
					last_name = contact.last_name
				)

				states.NOTIFICATIONS.vk_messages.append(new_message)
				self.db.add_vk_message(new_message)

			elif event.from_chat:
				synthesis_text('У вас новое сообщение в беседе')

		except CantFoundContact:
			pass
			#match self.get_user_data_by_id(event.user_id):
			#	case contact if isinstance(contact, Errors):
			#		synthesis_text(contact.value)

			#	case user if isinstance(user, dict):
			#		print(user)
			#		if not states.get_mute_state():
			#			answer = f'У вас новое сообщение в Вконтакте от пользователя {user["first_name"]}'
			#			if user["last_name"]:
			#				answer += f' {user["last_name"]}'
			#			synthesis_text(answer)

			#		new_message = Message(
			#			text = event.text, 
			#			from_id = event.user_id,
			#			first_name = user['first_name'],
			#			last_name = user['last_name']
			#		)

			#		states.change_notifications(
			#			VK_MESSAGES_NOTIFICATION, 
			#			new_message
			#		)

			#		self.db.add_vk_message(new_message)

		except Exception as e:
			say_error(Errors.PROCESSING_NEW_VK_MESSAGE)
			logger.error(e)
