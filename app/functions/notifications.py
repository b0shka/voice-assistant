from utils.logging import logger
from common.states import states
from common.errors import *
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite


class Notifications:

	def __init__(self):
		try:
			self.db = DatabaseSQLite()
		except Exception as e:
			logger.error(e)


	def waiting_select_action(self):
		synthesis_text('Какое действие вы хотите выполнить?')


	def viewing_notifications(self):
		try:
			notifications = states.get_notifications()

			count_telegram_messages = str(len(notifications['telegram_messages']))
			if int(count_telegram_messages):
				if count_telegram_messages[-1] == '1':
					answer = 'У вас одно новое сообщение в Телеграм'
				elif count_telegram_messages[-1] in ('2', '3', '4'):
					answer = f'У вас {count_telegram_messages} новых сообщения в Телеграм'
				else:
					answer = f'У вас {count_telegram_messages} новых сообщений в Телеграм'

				synthesis_text(answer)

			count_vk_messages = str(len(notifications['vk_messages']))
			if int(count_vk_messages):
				if count_vk_messages[-1] == '1':
					answer = 'У вас одно новое сообщение в Вконтакте'
				elif count_vk_messages[-1] in ('2', '3', '4'):
					answer = f'У вас {count_vk_messages} новых сообщения в Вконтакте'
				else:
					answer = f'У вас {count_vk_messages} новых сообщений в Вконтакте'

				synthesis_text(answer)

			if not int(count_telegram_messages) and not int(count_vk_messages):
				answer = 'У вас пока нет уведомлений'
				synthesis_text(answer)

		except Exception as e:
			logger.error(e)


	def viewing_telegram_messages(self):
		try:
			telegram_messages = states.get_notifications_type('telegram_messages')

			if len(telegram_messages):
				for message in telegram_messages:
					print(message)
			else:
				synthesis_text('У вас нет новых сообщений в Телеграм')
		except Exception as e:
			logger.error(e)


	def viewing_vk_messages(self):
		try:
			vk_messages = states.get_notifications_type('vk_messages')

			if len(vk_messages):
				for message in vk_messages:
					print(message)
			else:
				synthesis_text('У вас нет новых сообщений в Вконтакте')
		except Exception as e:
			logger.error(e)


	def clean_all_notifications(self):
		try:
			states.clean_notifications('telegram_messages')
			states.clean_notifications('vk_messages')

			result = self.db.delete_telegram_messages()
			if not result:
				logger.error(ERROR_DELETE_TELEGRAM_MESSAGES)

			result = self.db.delete_vk_messages()
			if not result:
				logger.error(ERROR_DELETE_VK_MESSAGES)

			synthesis_text('Уведомления очищены')
		except Exception as e:
			logger.error(e)


	def clean_telegram_messages(self):
		try:
			states.clean_notifications('telegram_messages')

			result = self.db.delete_telegram_messages()
			if not result:
				logger.error(ERROR_DELETE_TELEGRAM_MESSAGES)

			synthesis_text('Новые сообщения в Телеграм очищены')
		except Exception as e:
			logger.error(e)


	def clean_vk_messages(self):
		try:
			states.clean_notifications('vk_messages')

			result = self.db.delete_vk_messages()
			if not result:
				logger.error(ERROR_DELETE_VK_MESSAGES)

			synthesis_text('Новые сообщения в Вконтакте очищены')
		except Exception as e:
			logger.error(e)