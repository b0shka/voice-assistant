import asyncio
import threading
from utils.logging import logger
from services.vk.vk import VK
from services.telegram.telegram import Telegram


class Monitoring:

	def __init__(self):
		try:
			self.vk = VK()
			self.telegram = Telegram()
		except Exception as e:
			logger.error(e)


	def start(self):
		'''
			Начало мониторинга сторонних сервисов (Телеграм, ВКонтакте)
		'''
		try:
			check_vk = threading.Thread(target=self.vk.check_new_messages)
			check_vk.start()

			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			loop.run_until_complete(self.telegram.check_new_messages())
			#asyncio.create_task(self.check_vk())

		except Exception as e:
			logger.error(e)