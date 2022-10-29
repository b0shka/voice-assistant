from common.notifications import *


class States:

	def __init__(self):
		self.SYNTHESIS_WORK = False
		self.WAITING_RESPONSE = False
		self.TOPIC = None
		self.MUTE = False
		self.CONTACTS = ()

		self.NOTIFICATIONS = {
			TELEGRAM_MESSAGES_NOTIFICATION: [],
			VK_MESSAGES_NOTIFICATION: []
		}


	def get_synthesis_work_state(self):
		return self.SYNTHESIS_WORK


	def change_synthesis_work_state(self, state):
		self.SYNTHESIS_WORK = state


	def get_waiting_response_state(self):
		return self.WAITING_RESPONSE


	def change_waiting_response_state(self, state):
		self.WAITING_RESPONSE = state

	
	def get_topic(self):
		return self.TOPIC


	def change_topic(self, topic):
		self.TOPIC = topic


	def get_mute_state(self):
		return self.MUTE


	def change_mute_state(self, state):
		self.MUTE = state


	def get_notifications(self):
		return self.NOTIFICATIONS


	def get_notifications_by_type(self, type):
		return self.NOTIFICATIONS[type]


	def change_notifications(self, type, data):
		self.NOTIFICATIONS[type].append(data)

	
	def clean_notifications(self, type):
		self.NOTIFICATIONS[type] = []


	def get_contacts(self):
		return self.CONTACTS

	
	def update_contacts(self, contacts):
		self.CONTACTS = contacts


states = States()