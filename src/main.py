import threading
from utils.logging import logger
from di.appication import Application
from domain.enum_class.Errors import Errors
from app.functions.communications import say_error


def main() -> None:
	try:
		assistant = container.assistant()
		monitoring = container.monitoring()
		monitoring_thread = threading.Thread(target=monitoring.start)

		monitoring_thread.start()
		assistant.start_listen()

	except Exception as e:
		logger.error(e)
		say_error(Errors.UNDEFIND.value)


if __name__ == "__main__":
	container = Application()
	#container.wire(modules=[__name__])
	container.config.repository.path_file_db.from_env("PATH_FILE_DB")
	container.config.services.path_file_session_telegram.from_env("PATH_FILE_SESSION_TELEGRAM")
	container.config.services.telegram_api_id.from_env("TELEGRAM_API_ID")
	container.config.services.telegram_api_hash.from_env("TELEGRAM_API_HASH")
	container.config.services.vk_token.from_env("VK_TOKEN")
	
	main()
