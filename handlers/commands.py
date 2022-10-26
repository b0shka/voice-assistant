from handlers.config import *
from handlers.functions_name import FunctionsName
from handlers.possible_words.actions import *
from handlers.possible_words.functions import *
from handlers.possible_words.pronouns import *
from handlers.possible_words.prepositions import *
from handlers.possible_words.descriptions import *


ALL_FUNCTIONS = {
	FunctionsName.NOTIFICATIONS_TOPIC: FunctionsName.NOTIFICATIONS_FUNCTIONS,
	FunctionsName.TELEGRAM_MESSAGES_TOPIC: FunctionsName.TELEGRAM_MESSAGES_FUNCTIONS,
	FunctionsName.VK_MESSAGES_TOPIC: FunctionsName.VK_MESSAGES_FUNCTIONS,
	FunctionsName.SOUND_TOPIC: FunctionsName.SOUND_FUNCTIONS
}

COMMANDS = {
	FunctionsName.EXIT_TOPIC: {
		FUNCTIONS: EXIT,
		ACTIONS: (),
		ADDITIONALLY: ()
	},

	FunctionsName.SHOW_NOTIFICATIONS: {
		FUNCTIONS: NOTIFICATIONS,
		ACTIONS: SHOW + WATCH,
		ADDITIONALLY: MY
	},
	FunctionsName.CLEAN_NOTIFICATIONS: {
		FUNCTIONS: NOTIFICATIONS,
		ACTIONS: REMOVE,
		ADDITIONALLY: ()
	},

	FunctionsName.SHOW_TELEGRAM_MESSAGES: {
		FUNCTIONS: (MESSAGES, TELEGRAM),
		ACTIONS: SHOW + WATCH,
		ADDITIONALLY: MY
	},
	FunctionsName.CLEAN_TELEGRAM_MESSAGES: {
		FUNCTIONS: (MESSAGES, TELEGRAM),
		ACTIONS: REMOVE,
		ADDITIONALLY: ()
	},
	FunctionsName.SEND_TELEGRAM_MESSAGES: {
		FUNCTIONS: (MESSAGES, TELEGRAM),
		ACTIONS: SEND + WRITE + CREATE,
		ADDITIONALLY: ()
	},

	FunctionsName.SHOW_VK_MESSAGES: {
		FUNCTIONS: (MESSAGES, VK),
		ACTIONS: SHOW + WATCH,
		ADDITIONALLY: MY
	},
	FunctionsName.CLEAN_VK_MESSAGES: {
		FUNCTIONS: (MESSAGES, VK),
		ACTIONS: REMOVE,
		ADDITIONALLY: ()
	},
	FunctionsName.SEND_VK_MESSAGES: {
		FUNCTIONS: (MESSAGES, VK),
		ACTIONS: SEND + WRITE + CREATE,
		ADDITIONALLY: ()
	},

	FunctionsName.UPDATE_CONTACTS: {
		FUNCTIONS: CONTACTS,
		ACTIONS: UPDATE,
		ADDITIONALLY: ()
	},

	FunctionsName.SOUND_MUTE: {
		FUNCTIONS: SOUND,
		ACTIONS: DISABLE,
		ADDITIONALLY: WITHOUT
	},
	FunctionsName.SOUND_TURN_ON: {
		FUNCTIONS: SOUND,
		ACTIONS: ENABLE,
		ADDITIONALLY: WITH
	}
}