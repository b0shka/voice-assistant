from app.functions.settings import Settings
from app.handlers.handler_command import processing_command
from utils.speech.yandex_recognition_streaming import listen


def launch() -> None:
	settings = Settings()
	settings.update_contacts(isLauch=True)
	settings.update_notifications(isLauch=True)


def start_listen() -> None:
	'''Начальная настройка и запуск прослушивания'''

	launch()
	
	for command in listen():
		processing_command(command)
