from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from common.exceptions.vk import *
from domain.enum_class.Errors import Errors
from domain.named_tuple.UserServiceData import VKUserData
from utils.logging import logger
from app.functions.messages import Messages


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
			raise ErrConnectVK(Errors.CONNECT_VK.value)


	def check_new_messages(self) -> None:
		try:
			logger.info('Началась проверка на новые сообщения в ВКонтакте')

			for event in self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
					self.messages.new_vk_message(event)
					
		except Exception as e:
			logger.error(e)
			raise ErrGetNewVKMessages(Errors.GET_NEW_VK_MESSAGES.value)


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


	def get_user_data_by_id(self, user_id: int | str) -> VKUserData:
		try:
			user_data = self.session.method(
				"users.get",
				{"user_ids": user_id}
			)
		except Exception as e:
			logger.error(e)
			raise CantGetUserData(Errors.GET_USER_DATA_VK_BY_ID.value)
		else:
			if user_data and user_data[0]:
				return VKUserData(
					id = user_data[0]["id"],
					first_name = user_data[0]["first_name"],
					last_name = user_data[0]["last_name"],
				)
			raise CantGetUserData(Errors.FAILED_GET_USER_DATA_VK_BY_ID.value)