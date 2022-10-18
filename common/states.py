from xmlrpc.client import Boolean



class States:

	def __init__(self):
		self.SYNTHESIS_WORK = False
		self.ASSISTANT_WORK = True
		self.WAITING_RESPONSE = False
		self.MUTE = False
		self.NOTIFICATIONS = {
			'telegram_messages': [],
			'vk_messages': []
		}


	def get_synthesis_work_state(self):
		return self.SYNTHESIS_WORK


	def change_synthesis_work_state(self, state):
		self.SYNTHESIS_WORK = state
		

	def get_assistant_work_state(self):
		return self.ASSISTANT_WORK


	def change_assistant_work_state(self, state):
		self.ASSISTANT_WORK = state


	def get_waiting_response_state(self):
		return self.WAITING_RESPONSE


	def change_waiting_response_state(self, state):
		self.WAITING_RESPONSE = state


	def get_mute_state(self):
		return self.MUTE


	def change_mute_state(self, state):
		self.MUTE = state


	def get_notifications(self):
		return self.NOTIFICATIONS


	def change_notifications(self, type, data):
		self.NOTIFICATIONS[type].append(data)


states = States()