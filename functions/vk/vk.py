import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from common.config import *


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
			logger.info('Start check new messages in VK')

			for event in await self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
					print(event.text)
					print(event.from_user)
					print(event.peer_id)
					print(event.user_id)
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