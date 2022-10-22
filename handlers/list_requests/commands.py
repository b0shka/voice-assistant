from handlers.list_requests.actions import *
from handlers.list_requests.functions import *
from handlers.list_requests.pronouns import *
from handlers.list_requests.functions_name import FunctionsName
from handlers.list_requests.config import *
from handlers.list_requests.descriptions import *


ALL_FUNCTIONS = {
	FunctionsName.NOTIFICATIONS_TOPIC: FunctionsName.NOTIFICATIONS_FUNCTIONS,
	FunctionsName.TELEGRAM_MESSAGES_TOPIC: FunctionsName.TELEGRAM_MESSAGES_FUNCTIONS,
	FunctionsName.VK_MESSAGES_TOPIC: FunctionsName.VK_MESSAGES_FUNCTIONS
}

COMMANDS = {
	FunctionsName.EXIT_TOPIC: {
		FUNCTIONS: EXIT,
		ACTIONS: (),
		PRONOUNS: ()
	},
	FunctionsName.SHOW_NOTIFICATIONS: {
		FUNCTIONS: NOTIFICATIONS,
		ACTIONS: SHOW + WATCH,
		PRONOUNS: MY
	},
	FunctionsName.CLEAN_NOTIFICATIONS: {
		FUNCTIONS: NOTIFICATIONS,
		ACTIONS: REMOVE,
		PRONOUNS: ()
	},

	FunctionsName.SHOW_TELEGRAM_MESSAGES: {
		FUNCTIONS: (MESSAGES, TELEGRAM),
		ACTIONS: SHOW + WATCH,
		PRONOUNS: MY
	},
	FunctionsName.CLEAN_TELEGRAM_MESSAGES: {
		FUNCTIONS: (MESSAGES, TELEGRAM),
		ACTIONS: REMOVE,
		PRONOUNS: ()
	},
	FunctionsName.SEND_TELEGRAM_MESSAGES: {
		FUNCTIONS: (MESSAGES, TELEGRAM),
		ACTIONS: SEND + WRITE + CREATE,
		PRONOUNS: ()
	},

	FunctionsName.SHOW_VK_MESSAGES: {
		FUNCTIONS: (MESSAGES, VK),
		ACTIONS: SHOW + WATCH,
		PRONOUNS: MY
	},
	FunctionsName.CLEAN_VK_MESSAGES: {
		FUNCTIONS: (MESSAGES, VK),
		ACTIONS: REMOVE,
		PRONOUNS: ()
	},
	FunctionsName.SEND_VK_MESSAGES: {
		FUNCTIONS: (MESSAGES, VK),
		ACTIONS: SEND + WRITE + CREATE,
		PRONOUNS: ()
	}
}