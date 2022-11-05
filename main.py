import threading
from domain.enum_class.Errors import Errors
from app.functions.communications import say_error
from utils.logging import logger
from di.appication import Application


def main() -> None:
	try:
		container = Application()
		#container.wire(modules=[__name__])

		assistant = container.assistant()
		monitoring = container.monitoring()
		monitoring_thread = threading.Thread(target=monitoring.start)

		monitoring_thread.start()
		assistant.start_listen()

	except Exception as e:
		say_error(Errors.UNDEFIND)
		logger.error(e)


if __name__ == "__main__":
	main()