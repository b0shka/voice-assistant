import asyncio
import vk_api
from telethon.sync import TelegramClient, events
from vk_api.longpoll import VkLongPoll, VkEventType
import sys
sys.path.append('/home/q/p/projects/voice-assistant/version_2.0')
from common.config import *
from common.errors import *
from database.database import Database


class Monitoring:

	def __init__(self):
		try:
			self.db = Database()

			self.client = TelegramClient(
				PATH_FILE_SESSION_TELEGRAM, 
				TELEGRAM_API_ID, 
				TELEGRAM_API_HASH
			)
			logger.info("Success connect telegram api")

			self.session = vk_api.VkApi(token=VK_TOKEN)
			self.longpoll = VkLongPoll(self.session)
			logger.info('Success connect vk api')
		except Exception as e:
			logger.error(e)


	async def check_telegram(self):
		try:
			logger.info('Start check new messages in Telegram')

			@self.client.on(events.NewMessage())
			async def handler(event):
				message = event.message.to_dict()
				from_id = message['from_id']['user_id']
				
				if from_id in [i[3] for i in self.contacts]:
					result = self.db.add_telegram_message(message['message'], int(from_id))
					if result == 0:
						logger.error(ERROR_ADD_TELEGRAM_MESSAGE)

			await self.client.start()
			await self.client.run_until_disconnected()
		except Exception as e:
			logger.error(e)


	async def check_vk(self):
		try:
			logger.info('Start check new messages in VK')
			
			for event in await self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
					if event.from_user and event.user_id in [i[4] for i in self.contacts]:
						result = self.db.add_vk_message(event.text, event.user_id)
						if result == 0:
							logger.error(ERROR_ADD_VK_MESSAGE)
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			self.contacts = self.db.get_contacts()
			if self.contacts == 0:
				logger.error(ERROR_GET_CONTACTS)

			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)

			loop.run_until_complete(self.check_telegram())
			#loop.run_until_complete(self.check_vk())
		except Exception as e:
			logger.error(e)


if __name__ == "__main__":
	monitoring = Monitoring()
	monitoring.start()