import time
import asyncio
import threading
from database.database import Database
from functions.telegram.telegram import Telegram
from functions.vk.vk import VK
from functions.yandex.yandex import Yandex
from functions.speech import synthesizer
from common.config import *


class Assistant:

	def __init__(self):
		try:
			self.db = Database()
			self.telegram = Telegram()
			self.vk = VK()
			#self.yandex = Yandex()

			self.contacts = self.db.get_contacts()
			self.telegram_messages = self.db.get_telegram_messages()
			self.vk_messages = self.db.get_vk_messages()
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			#asyncio.create_task(self.monitoring())

			while True:
				#await asyncio.sleep(0.5)
				text = input('Enter: ')
				if text == '1':
					synthesizer.say('привет')
				elif text == '2':
					synthesizer.say('все отлично')
				elif text == '3':
					break
		except Exception as e:
			logger.error(e)


	async def monitoring(self):
		try:
			while True:
				await asyncio.sleep(5)
				telegram_messages = self.db.get_telegram_messages()
				vk_messages = self.db.get_vk_messages()
				print(telegram_messages)
				print(vk_messages, end='\n\n')
		except Exception as e:
			logger.error(e)


if __name__ == "__main__":
	assistant = Assistant()
	#monitoring = threading.Thread(target=assistant.monitoring)

	#monitoring.start()
	assistant.start()
	#asyncio.run(assistant.start())