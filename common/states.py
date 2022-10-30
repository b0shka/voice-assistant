from common.notifications import *


class States:

	def __init__(self):
		self.SYNTHESIS_WORK = False # Статус работы синтеза речи, для предотвращения коолизий
		self.WAITING_RESPONSE = False # Статус ожидания ответа на не полную команду
		self.TOPIC = None # Текущая тема разговора
		self.MUTE = False
		self.CONTACTS = ()
		self.WAITING_RESULT_RECOGNITION = True # Ожидание конечного результата распознавания голоса
		self.ACTION_WITHOUT_FUNCTION = False # Статус вызова комманды с действие, но без функции, которое должно основываться на текущей теме разговора

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


	def get_waiting_result_recognition(self):
		return self.WAITING_RESULT_RECOGNITION

	def change_waiting_result_recognition(self, status):
		self.WAITING_RESULT_RECOGNITION = status


	def get_action_without_function_state(self):
		return self.ACTION_WITHOUT_FUNCTION

	def change_action_without_function_state(self, state):
		self.ACTION_WITHOUT_FUNCTION = state


states = States()