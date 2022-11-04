from app.functions.settings import Settings
from app.handlers.handler_command import HandlerCommand
from utils.speech.yandex_recognition_streaming import listen



class Assistant:

	def __init__(
		self, 
		settings: Settings,
		handler_command: HandlerCommand
	):
		self.settings = settings
		self.handler_command = handler_command


	def configure_assistant(self) -> None:
		self.settings.update_contacts(isLauch=True)
		self.settings.update_notifications(isLauch=True)


	def start_listen(self) -> None:
		'''Начальная настройка и запуск прослушивания'''

		self.configure_assistant()
		
		for command in listen():
			self.handler_command.processing_command(command)
