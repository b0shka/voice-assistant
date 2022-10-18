import vk_api
import asyncio
import threading
from telethon.sync import TelegramClient, events
from vk_api.longpoll import VkLongPoll, VkEventType
from common.config import *
from common.errors import *
from common.states import states
from database.database_sqlite import DatabaseSQLite
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text


class Monitoring:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()

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
					if not states.get_mute_state():
						synthesis_text('У вас новое сообщение в Телеграм')

					states.change_notifications(
						'telegram_messages', 
						{
							'message': message['message'],
							'from_id': int(from_id)
						}
					)

					result = self.db.add_telegram_message(message['message'], int(from_id))
					if result == 0:
						logger.error(ERROR_ADD_TELEGRAM_MESSAGE)

			await self.client.start()
			await self.client.run_until_disconnected()

		except Exception as e:
			logger.error(e)


	def check_vk(self):
		try:
			logger.info('Start check new messages in VK')
			
			for event in self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
					if event.from_user and event.user_id in [i[4] for i in self.contacts]:
						if not states.get_mute_state():
							synthesis_text('У вас новое сообщение в Вконтакте')

						states.change_notifications('vk_messages', {
							'message': event.text,
							'from_id': event.user_id
						})

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

			check_vk = threading.Thread(target=self.check_vk)
			check_vk.start()

			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			loop.run_until_complete(self.check_telegram())
			#loop.run_until_complete(self.check_vk())
			#asyncio.create_task(self.check_vk())

		except Exception as e:
			logger.error(e)