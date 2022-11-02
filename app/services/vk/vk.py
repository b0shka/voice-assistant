import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from common.config import *
from common.exceptions.vk import *
from domain.enum_class.Errors import Errors
from utils.logging import logger
from app.functions.messages import Messages


class VK:

	def __init__(self) -> None:
		try:
			self.messages = Messages()
			self.session = vk_api.VkApi(token=VK_TOKEN)
			self.longpoll = VkLongPoll(self.session)

			logger.info('Успешное подключение к vk api')
		except Exception as e:
			logger.error(e)
			raise ErrConnectVK(Errors.CONNECT_VK)


	def check_new_messages(self) -> None:
		try:
			logger.info('Началась проверка на новые сообщения в ВКонтакте')

			for event in self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
					self.messages.new_vk_message(event)
					
		except Exception as e:
			logger.error(e)
			raise ErrGetNewVKMessages(Errors.GET_NEW_VK_MESSAGES)


	def send_message(self, user_id: str, message: str) -> None:
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
			raise ErrSendVKMessage(Errors.SEND_VK_MESSAGE)


	def get_user_data_by_id(self, user_id: str) -> dict:
		try:
			user_data = self.session.method(
				"users.get",
				{"user_ids": user_id}
			)

			if user_data[0]:
				return user_data[0]
			raise CantGetUserData(Errors.FAILED_GET_USER_DATA_VK_BY_ID)

		except Exception as e:
			logger.error(e)
			raise ErrGetUserData(Errors.GET_USER_DATA_VK_BY_ID)