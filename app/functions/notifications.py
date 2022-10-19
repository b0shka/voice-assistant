from utils.logging import logger
from common.states import states
from utils.speech.yandex_synthesis import synthesis_text


def completion_notifications(telegram_messages, vk_messages):
	try:
		for message in telegram_messages:
			states.change_notifications(
				'telegram_messages',
				{
					'message': message[1],
					'from_id': message[2]
				}
			)

		for message in vk_messages:
			states.change_notifications(
				'vk_messages',
				{
					'message': message[1],
					'from_id': message[2]
				}
			)
	except Exception as e:
		logger.error(e)


def viewing_notifications():
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
	except Exception as e:
		logger.error(e)


def clean_all_notifications():
	try:
		states.clean_notifications('telegram_messages')
		states.clean_notifications('vk_messages')

		synthesis_text('Уведомления очищены')
	except Exception as e:
		logger.error(e)


def clean_telegram_messages():
	try:
		states.clean_notifications('telegram_messages')
		synthesis_text('Новые сообщения в Телеграм очищены')
	except Exception as e:
		logger.error(e)


def clean_vk_messages():
	try:
		states.clean_notifications('vk_messages')
		synthesis_text('Новые сообщения в Вконтакте очищены')
	except Exception as e:
		logger.error(e)