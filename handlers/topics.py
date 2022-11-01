from handlers.config import *
from handlers.possible_words.actions import *
from handlers.possible_words.functions import *
from handlers.possible_words.pronouns import *
from handlers.possible_words.prepositions import *
from handlers.possible_words.descriptions import *
from handlers.functions_names import TopicsNames, FunctionsNames


#HIGH_PRIORITY_TOPICS = (FunctionsNames.EXIT_TOPIC)

TOPICS = {
	TopicsNames.EXIT_TOPIC: {
		FUNCTIONS: EXIT,
		NESTED_FUNCTIONS: None
	},
	
	TopicsNames.NOTIFICATIONS_TOPIC: {
		FUNCTIONS: NOTIFICATIONS,
		NESTED_FUNCTIONS: {
			FunctionsNames.SHOW_NOTIFICATIONS: {
				ACTIONS: SHOW + WATCH,
				ADDITIONALLY: MY
			},
			FunctionsNames.CLEAN_NOTIFICATIONS: {
				ACTIONS: REMOVE,
				ADDITIONALLY: ()
			},
			FunctionsNames.UPDATE_NOTIFICATIONS: {
				ACTIONS: UPDATE,
				ADDITIONALLY: ()
			}
		}
	},

	TopicsNames.TELEGRAM_MESSAGES_TOPIC: {
		FUNCTIONS: (MESSAGES, TELEGRAM),
		NESTED_FUNCTIONS: {
			FunctionsNames.SHOW_TELEGRAM_MESSAGES: {
				ACTIONS: SHOW + WATCH,
				ADDITIONALLY: MY
			},
			FunctionsNames.CLEAN_TELEGRAM_MESSAGES: {
				ACTIONS: REMOVE,
				ADDITIONALLY: ()
			},
			FunctionsNames.SEND_TELEGRAM_MESSAGES: {
				ACTIONS: SEND + WRITE + CREATE,
				ADDITIONALLY: ()
			}
		}
	},

	TopicsNames.VK_MESSAGES_TOPIC: {
		FUNCTIONS: (MESSAGES, VK),
		NESTED_FUNCTIONS: {
			FunctionsNames.SHOW_VK_MESSAGES: {
				ACTIONS: SHOW + WATCH,
				ADDITIONALLY: MY
			},
			FunctionsNames.CLEAN_VK_MESSAGES: {
				ACTIONS: REMOVE,
				ADDITIONALLY: ()
			},
			FunctionsNames.SEND_VK_MESSAGES: {
				ACTIONS: SEND + WRITE + CREATE,
				ADDITIONALLY: ()
			}
		}
	},

	TopicsNames.SOUND_TOPIC: {
		FUNCTIONS: SOUND,
		NESTED_FUNCTIONS: {
			FunctionsNames.SOUND_MUTE: {
				ACTIONS: DISABLE,
				ADDITIONALLY: WITHOUT
			},
			FunctionsNames.SOUND_TURN_ON: {
				ACTIONS: ENABLE,
				ADDITIONALLY: WITH
			}
		}
	},

	TopicsNames.CONTACTS_TOPIC: {
		FUNCTIONS: CONTACTS,
		NESTED_FUNCTIONS: {
			FunctionsNames.SHOW_CONTACTS: {
				ACTIONS: SHOW + WATCH,
				ADDITIONALLY: MY
			},
			FunctionsNames.UPDATE_CONTACTS: {
				ACTIONS: UPDATE,
				ADDITIONALLY: ()
			},
			FunctionsNames.ADD_CONTACT: {
				ACTIONS: ADD + CREATE,
				ADDITIONALLY: ()
			},
			FunctionsNames.DELETE_CONTACT: {
				ACTIONS: REMOVE,
				ADDITIONALLY: ()
			}
		}
	}
}