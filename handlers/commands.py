from handlers.config import *
from handlers.possible_words.actions import *
from handlers.possible_words.functions import *
from handlers.possible_words.pronouns import *
from handlers.possible_words.prepositions import *
from handlers.possible_words.descriptions import *
from handlers.functions_name import FunctionsName


TOPICS = {
	FunctionsName.EXIT_TOPIC: {
		FUNCTIONS: EXIT,
		NESTED_FUNCTIONS: None
	},
	
	FunctionsName.NOTIFICATIONS_TOPIC: {
		FUNCTIONS: NOTIFICATIONS,
		NESTED_FUNCTIONS: {
			FunctionsName.SHOW_NOTIFICATIONS: {
				ACTIONS: SHOW + WATCH,
				ADDITIONALLY: MY
			},
			FunctionsName.CLEAN_NOTIFICATIONS: {
				ACTIONS: REMOVE,
				ADDITIONALLY: ()
			}
		}
	},

	FunctionsName.TELEGRAM_MESSAGES_TOPIC: {
		FUNCTIONS: (MESSAGES, TELEGRAM),
		NESTED_FUNCTIONS: {
			FunctionsName.SHOW_TELEGRAM_MESSAGES: {
				ACTIONS: SHOW + WATCH,
				ADDITIONALLY: MY
			},
			FunctionsName.CLEAN_TELEGRAM_MESSAGES: {
				ACTIONS: REMOVE,
				ADDITIONALLY: ()
			},
			FunctionsName.SEND_TELEGRAM_MESSAGES: {
				ACTIONS: SEND + WRITE + CREATE,
				ADDITIONALLY: ()
			}
		}
	},

	FunctionsName.VK_MESSAGES_TOPIC: {
		FUNCTIONS: (MESSAGES, VK),
		NESTED_FUNCTIONS: {
			FunctionsName.SHOW_VK_MESSAGES: {
				ACTIONS: SHOW + WATCH,
				ADDITIONALLY: MY
			},
			FunctionsName.CLEAN_VK_MESSAGES: {
				ACTIONS: REMOVE,
				ADDITIONALLY: ()
			},
			FunctionsName.SEND_VK_MESSAGES: {
				ACTIONS: SEND + WRITE + CREATE,
				ADDITIONALLY: ()
			}
		}
	},

	FunctionsName.SOUND_TOPIC: {
		FUNCTIONS: SOUND,
		NESTED_FUNCTIONS: {
			FunctionsName.SOUND_MUTE: {
				ACTIONS: DISABLE,
				ADDITIONALLY: WITHOUT
			},
			FunctionsName.SOUND_TURN_ON: {
				ACTIONS: ENABLE,
				ADDITIONALLY: WITH
			}
		}
	},

	FunctionsName.CONTACTS_TOPIC: {
		FUNCTIONS: CONTACTS,
		NESTED_FUNCTIONS: {
			FunctionsName.UPDATE_CONTACTS: {
				ACTIONS: UPDATE,
				ADDITIONALLY: ()
			},
			FunctionsName.SHOW_CONTACTS: {
				ACTIONS: SHOW + WATCH,
				ADDITIONALLY: MY
			},
			FunctionsName.ADD_CONTACT: {
				ACTIONS: ADD + CREATE,
				ADDITIONALLY: ()
			},
			FunctionsName.DELETE_CONTACT: {
				ACTIONS: REMOVE,
				ADDITIONALLY: ()
			}
		}
	}
}