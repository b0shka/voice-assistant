import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from common.config import *
from utils.logging import logger
from app.functions.messages import Messages


class VK:

	def __init__(self):
		try:
			self.session = vk_api.VkApi(token=VK_TOKEN)
			self.longpoll = VkLongPoll(self.session)
			logger.info('Success connect vk api')

			self.messages = Messages()
		except Exception as e:
			logger.error(e)


	def check_new_messages(self):
		try:
			logger.info('Start check new messages in VK')

			for event in self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
					self.messages.new_vk_message(event)
					
		except Exception as e:
			logger.error(e)


	def send_message(self, user_id: str, message: str):
		try:
			self.session.method(
				"messages.send", 
				{
					"user_id": user_id, 
					"message": message,
					"random_id": 0
				}
			)
			logger.info(f"Success send messages to {user_id}")
		except Exception as e:
			logger.error(e)


	def get_user_data_by_id(self, user_id: str):
		try:
			user_data = self.session.method(
				"users.get",
				{
					"user_ids": user_id
				}
			)

			if user_data[0]:
				return user_data[0]
			else:
				return 0
		except Exception as e:
			logger.error(e)
			return -1