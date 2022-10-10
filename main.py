import time
import asyncio
import threading
from database.database import Database
from functions.telegram.telegram import Telegram
from functions.vk.vk import VK
from functions.yandex.yandex import Yandex
from functions.speech import synthesizer
from common.config import *
from common.errors import *


class Assistant:

	def __init__(self):
		try:
			self.db = Database()
			self.db.create_tables()
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
				req = input('')
				
				result = self.db.add_request_answer_assistant(req, 'request')
				if result == 0:
					logger.error(ERROR_ADD_REQUEST_ANSWER)
				
				if req == 'exit':
					break
				elif req == 'hello':
					answer = 'привет'
					synthesizer.say(answer)
					result = self.db.add_request_answer_assistant(answer, 'answer')
					if result == 0:
						logger.error(ERROR_ADD_REQUEST_ANSWER)
		except Exception as e:
			logger.error(e)


	def monitoring(self):
		try:
			while True:
				#await asyncio.sleep(5)

				telegram_messages = self.db.get_telegram_messages()
				if telegram_messages == 0:
					logger.error(ERROR_GET_TELEGRAM_MESSAGES)

				vk_messages = self.db.get_vk_messages()
				if vk_messages == 0:
					logger.error(ERROR_GET_VK_MESSAGES)

				if len(telegram_messages):
					print(f'У вас {len(telegram_messages)} сообщений в Telegram')

				if len(vk_messages):
					print(f'У вас {len(vk_messages)} сообщений в Вконтакте')

				time.sleep(5)
		except Exception as e:
			logger.error(e)


if __name__ == "__main__":
	assistant = Assistant()
	monitoring = threading.Thread(target=assistant.monitoring)

	monitoring.start()
	assistant.start()
	#asyncio.run(assistant.start())