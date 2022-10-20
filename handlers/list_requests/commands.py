from list_requests.actions import *
from list_requests.functions import *
from list_requests.pronouns import *
from list_requests.functions_name import *


COMMANDS = {
	NOTIFICATIONS_NAME: {
		'function': NOTIFICATIONS,
		'actions': SHOW + WATCH,
		'pronouns': MY
	}
}