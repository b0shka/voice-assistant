from handlers.list_requests.actions import *
from handlers.list_requests.functions import *
from handlers.list_requests.pronouns import *
from handlers.list_requests.functions_name import *
from handlers.list_requests.config import *
from handlers.list_requests.descriptions import *


COMMANDS = {
	EXIT_NAME: {
		FUNCTION: EXIT,
		ACTIONS: (),
		PRONOUNS: ()
	},
	NOTIFICATIONS_NAME: {
		FUNCTION: NOTIFICATIONS,
		ACTIONS: SHOW + WATCH,
		PRONOUNS: MY
	},

	SHOW_TELEGRAM_MESSAGES: {
		FUNCTION: (MESSAGES, TELEGRAM),
		ACTIONS: SHOW + WATCH + NEW,
		PRONOUNS: MY
	},
	CLEAN_TELEGRAM_MESSAGES: {
		FUNCTION: (MESSAGES, TELEGRAM),
		ACTIONS: REMOVE,
		PRONOUNS: MY
	},
	SEND_TELEGRAM_MESSAGES: {
		FUNCTION: (MESSAGES, TELEGRAM),
		ACTIONS: SEND + WRITE,
		PRONOUNS: MY
	},

	SHOW_VK_MESSAGES: {
		FUNCTION: (MESSAGES, VK),
		ACTIONS: SHOW + WATCH + NEW,
		PRONOUNS: MY
	},
	CLEAN_VK_MESSAGES: {
		FUNCTION: (MESSAGES, VK),
		ACTIONS: REMOVE,
		PRONOUNS: MY
	},
	SEND_VK_MESSAGES: {
		FUNCTION: (MESSAGES, VK),
		ACTIONS: SEND + WRITE,
		PRONOUNS: MY
	}
}