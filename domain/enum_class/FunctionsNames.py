from enum import Enum


class FunctionsNames(Enum):
	SHOW_NOTIFICATIONS = 'show_notifications'
	CLEAN_NOTIFICATIONS = 'clean_notifications'
	UPDATE_NOTIFICATIONS = 'update_notifications'

	SHOW_TELEGRAM_MESSAGES = 'show_telegram_messages'
	CLEAN_TELEGRAM_MESSAGES = 'clean_telegram_messages'
	SEND_TELEGRAM_MESSAGES = 'send_telegram_messages'

	SHOW_VK_MESSAGES = 'show_vk_messages'
	CLEAN_VK_MESSAGES = 'clean_vk_messages'
	SEND_VK_MESSAGES = 'send_vk_messages'
	
	SOUND_MUTE = 'sound_mute'
	SOUND_TURN_ON = 'sound_turn_on'

	UPDATE_CONTACTS = 'update_contacts'
	SHOW_CONTACTS = 'show_contacts'
	ADD_CONTACT = 'add_contact'
	DELETE_CONTACT = 'delete_contact'