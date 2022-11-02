from app.functions.settings import Settings
from app.handlers.handler_command import listen_command


def launch() -> None:
	settings = Settings()
	settings.update_contacts(isLauch=True)
	settings.update_notifications(isLauch=True)


def start_listen() -> None:
	'''Начальная настройка и запуск прослушивания'''

	launch()
	listen_command()