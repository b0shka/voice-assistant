import threading
from app.assistant import Assistant
from app.monitoring import Monitoring
from utils.logging import logger


def main():
	try:
		assistant = Assistant()
		monitoring = Monitoring()
		monitoring_thread = threading.Thread(target=monitoring.start)

		monitoring_thread.start()
		assistant.start()
	except Exception as e:
		logger.error(e)


if __name__ == "__main__":
	main()