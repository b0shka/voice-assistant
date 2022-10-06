import asyncio
import threading
from database.database import Database
from functions.telegram.telegram import Telegram
from functions.vk.vk import VK
from functions.yandex.yandex import Yandex
from common.config import *


class Assistant:

	def __init__(self):
		try:
			self.db = Database()
			self.telegram = Telegram()
			self.vk = VK()
			self.yandex = Yandex()
		except Exception as e:
			logger.error(e)


	def start(self):
		try:
			pass
		except Exception as e:
			logger.error(e)


	def monitoring(self, loop):
		try:
			asyncio.set_event_loop(loop)
			loop.run_until_complete(self.telegram.check_new_messages())
		except Exception as e:
			logger.error(e)



if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	assistant = Assistant()
	monitoring = threading.Thread(target=assistant.monitoring, args=(loop, ))

	monitoring.start()
	assistant.start()