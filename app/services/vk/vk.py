from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from utils.logging import logger
from common.states import states
from common.exceptions.messages import *
from common.exceptions.contacts import CantFoundContact
from common.exceptions.database import ErrAddVKMessage
from domain.enum_class.Errors import Errors
from domain.named_tuple.Message import Message
from domain.named_tuple.Contact import Contact
from domain.named_tuple.UserServiceData import VKUserData
from app.functions.messages import Messages
from app.functions.communications import say_error


class VK:

	def __init__(
		self, 
		session: VkApi, 
		longpoll: VkLongPoll, 
		messages: Messages
	) -> None:
		try:
			self.messages = messages
			self.session = session
			self.longpoll = longpoll

			logger.info('Успешное подключение к vk api')
		except Exception as e:
			logger.error(e)
			say_error(Errors.CONNECT_VK.value)


	def _get_contact_by_from_id(self, id: int) -> Contact:
		for contact in states.CONTACTS:
			if contact.vk_id == id:
				return contact
		else:
			raise CantFoundContact


	def check_new_messages(self) -> None:
		'''Мониторинг новых сообщений в ВКонтакте'''

		logger.info('Началась проверка на новые сообщения в ВКонтакте')

		try:
			for event in self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
					try:
						self.processing_new_message(event)
					except Exception as e:
						logger.error(e)
						say_error(Errors.PROCESSING_NEW_VK_MESSAGES.value)

		except Exception as e:
			logger.error(e)
			say_error(Errors.MONITORING_NEW_VK_MESSAGES.value)


	def processing_new_message(self, event: Event) -> None:
		if event.from_user:
			user_id = event.user_id
			text = event.text

			try:
				contact = self._get_contact_by_from_id(user_id)
				new_message = Message(
					text = text,
					from_id = user_id,
					contact_id = contact.id,
					first_name = contact.first_name,
					last_name = contact.last_name
				)

				try:
					self.messages.new_vk_message_from_contact(new_message, contact)
				except ErrAddVKMessage as e:
					say_error(e)

			except CantFoundContact:
				# сообщение не от контакта
				try:
					user = self._get_user_data_by_id(user_id)
				except CantGetUserData as e:
					say_error(e)
				else:
					new_message = Message(
						text = text, 
						from_id = user_id,
						first_name = user.first_name,
						last_name = user.last_name
					)

					try:
						self.messages.new_vk_message_from_user(new_message, user)
					except ErrAddVKMessage as e:
						say_error(e)

		elif event.from_chat:
			pass


	def send_message(self, user_id: int, message: str) -> None:
		try:
			self.session.method(
				"messages.send", 
				{
					"user_id": user_id, 
					"message": message,
					"random_id": 0
				}
			)
			logger.info(f"Сообщений успешно отправлено, пользователю: {user_id}")

		except Exception as e:
			logger.error(e)
			raise ErrSendVKMessage(Errors.SEND_VK_MESSAGE.value)


	def _get_user_data_by_id(self, user_id: int | str) -> VKUserData:
		try:
			user_data = self.session.method(
				"users.get",
				{"user_ids": user_id}
			)
			
			if user_data and user_data[0]:
				return VKUserData(
					id = user_data[0]["id"],
					first_name = user_data[0]["first_name"],
					last_name = user_data[0]["last_name"],
				)

		except Exception as e:
			logger.error(e)
			raise CantGetUserData(Errors.GET_USER_DATA_VK_BY_ID.value)
		else:
			raise CantGetUserData(Errors.FAILED_GET_USER_DATA_VK_BY_ID.value)