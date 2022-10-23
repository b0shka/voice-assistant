import vk_api
from vk_api.longpoll import VkLongPoll
from common.config import *
from utils.logging import logger


class VK:

	def __init__(self):
		try:
			self.session = vk_api.VkApi(token=VK_TOKEN)
			self.longpoll = VkLongPoll(self.session)
			logger.info('Success connect vk api')
		except Exception as e:
			logger.error(e)


	async def check_new_messages(self):
		try:
			pass
		except Exception as e:
			logger.error(e)


	def send_message(self, user_id, message):
		try:
			self.session.method(
				"messages.send", 
				{
					"user_id": user_id, 
					"message": message,
					"random_id": 0
				}
			)
		except Exception as e:
			logger.error(e)