import asyncio
import threading
from common.config import *
from common.errors import *
from common.states import states
from common.notifications import *
from database.database_sqlite import DatabaseSQLite
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text
from domain.Message import Message
from services.vk.vk import VK
from services.telegram.telegram import Telegram


class Monitoring:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
			self.contacts = self.db.get_contacts()

			self.vk = VK()
			self.telegram = Telegram()

		except Exception as e:
			logger.error(e)


	def get_contact_by_from_id(self, id, service):
		try:
			for contact in self.contacts:
				if service == TELEGRAM_MESSAGES_NOTIFICATION:
					if contact[4] == id:
						return contact

				elif service == VK_MESSAGES_NOTIFICATION:
					if contact[5] == id:
						return contact

			return 0
		except Exception as e:
			logger.error(e)
			return -1


	async def check_telegram(self):
		try:

			for message in await self.telegram.check_new_messages():
				from_id = int(message['from_id']['user_id'])
			
				match self.get_contact_by_from_id(from_id, TELEGRAM_MESSAGES_NOTIFICATION):
					case 0:
						pass 
						# сообщение не от контакта или от канала/чата
					case -1:
						logger.error(ERROR_GET_CONTACT_BY_TELEGRAM_ID)
					case contact if type(contact) == tuple:
						if not states.get_mute_state():
							answer = f'У вас новое сообщение в Телеграм от контакта {contact[1]}'
							if contact[2]:
								answer += f' {contact[2]}'
							synthesis_text(answer)

						states.change_notifications(
							TELEGRAM_MESSAGES_NOTIFICATION, 
							Message(
								message = message['message'],
								contact_id = contact[0],
								first_name = contact[1],
								last_name = contact[2]
							)
						)

						result = self.db.add_telegram_message(
							message = message['message'], 
							contact_id = contact[0]
						)
						if result == 0:
							logger.error(ERROR_ADD_TELEGRAM_MESSAGE)
					
				#if from_id in [i[3] for i in self.contacts]:

		except Exception as e:
			logger.error(e)


	def check_vk(self):
		try:
			for event in self.vk.check_new_messages():
				if event.from_user:
					match self.get_contact_by_from_id(event.user_id, VK_MESSAGES_NOTIFICATION):
						case 0:
							match self.vk.get_user_data_by_id(event.user_id):
								case 0:
									logger.error(FAILED_GET_USER_DATA_BY_ID)
								case -1:
									logger.error(ERROR_GET_USER_DATA_BY_ID)

								case user if type(user) == map:
									print(user)
						case -1:
							logger.error(ERROR_GET_CONTACT_BY_VK_ID)

						case contact if type(contact) == tuple:
							if not states.get_mute_state():
								answer = f'У вас новое сообщение в Вконтакте от контакта {contact[1]}'
								if contact[2]:
									answer += f' {contact[2]}'
								synthesis_text(answer)

							states.change_notifications(
								VK_MESSAGES_NOTIFICATION, 
								Message(
									message = event.text,
									contact_id = contact[0],
									first_name = contact[1],
									last_name = contact[2]
								)
							)

							result = self.db.add_vk_message(
								message = event.text, 
								contact_id = contact[0]
							)
							if result == 0:
								logger.error(ERROR_ADD_VK_MESSAGE)

				elif event.from_chat:
					print('новое сообщение из чата')

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