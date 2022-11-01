import threading
from domain.enum_class.Errors import Errors
from app.assistant import start_listen
#from app.monitoring import Monitoring
from app.functions.communications import say_error
from utils.logging import logger


def main():
	try:
		#monitoring = Monitoring()
		#monitoring_thread = threading.Thread(target=monitoring.start)

		#monitoring_thread.start()
		start_listen()

	except Exception as e:
		say_error(Errors.UNDEFIND)
		logger.error(e)


if __name__ == "__main__":
	main()