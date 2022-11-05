import asyncio
import threading
from utils.logging import logger
from app.services.vk.vk import VK
from app.services.telegram.telegram import Telegram


class Monitoring:

	def __init__(self, vk: VK, telegram: Telegram) -> None:
		self.vk = vk
		self.telegram = telegram


	def start(self) -> None:
		'''Начало мониторинга сторонних сервисов (Телеграм, ВКонтакте)'''
		try:
			check_vk = threading.Thread(target=self.vk.check_new_messages)
			check_vk.start()

			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			loop.run_until_complete(self.telegram.check_new_messages())
			#asyncio.create_task(self.check_vk())

		except Exception as e:
			logger.error(e)