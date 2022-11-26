from app.functions.contacts import Contacts
from app.functions.notifications import Notifications
from app.handlers.handler_command import HandlerCommand
from utils.speech.yandex_recognition_streaming import listen


class Assistant:

	def __init__(
		self, 
		contacts: Contacts,
		notifications: Notifications,
		handler_command: HandlerCommand
	):
		self.contacts = contacts
		self.notifications = notifications
		self.handler_command = handler_command

		self.configure_assistant()


	def configure_assistant(self) -> None:
		'''Начальная настройка ассистента'''

		self.contacts.update_contacts(isLauch=True)
		self.notifications.update_notifications(isLauch=True)


	def start_listen(self) -> None:
		'''Запуск прослушивания микрофона'''
		
		for command in listen():
			self.handler_command.processing_command(command)
