

class FunctionsName:

	def __init__(self):
		print("################# HELLO #######################")

	EXIT_TOPIC = 'exit'

	NOTIFICATIONS_TOPIC = 'notifications'
	SHOW_NOTIFICATIONS = 'show_notifications'
	CLEAN_NOTIFICATIONS = 'clean_notifications'
	NOTIFICATIONS_FUNCTIONS = (SHOW_NOTIFICATIONS, CLEAN_NOTIFICATIONS)

	TELEGRAM_MESSAGES_TOPIC = 'telegram_messages'
	SHOW_TELEGRAM_MESSAGES = 'show_telegram_messages'
	CLEAN_TELEGRAM_MESSAGES = 'clean_telegram_messages'
	SEND_TELEGRAM_MESSAGES = 'send_telegram_messages'
	TELEGRAM_MESSAGES_FUNCTIONS = (SHOW_TELEGRAM_MESSAGES, CLEAN_TELEGRAM_MESSAGES, SEND_TELEGRAM_MESSAGES)

	VK_MESSAGES_TOPIC = 'vk_messages'
	SHOW_VK_MESSAGES = 'show_vk_messages'
	CLEAN_VK_MESSAGES = 'clean_vk_messages'
	SEND_VK_MESSAGES = 'send_vk_messages'
	VK_MESSAGES_FUNCTIONS = (SHOW_VK_MESSAGES, CLEAN_VK_MESSAGES, SEND_VK_MESSAGES)