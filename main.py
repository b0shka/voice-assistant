import threading
from app.assistant import Assistant
from utils.logging import logger


def main():
	try:
		assistant = Assistant()
		monitoring = threading.Thread(target=assistant.monitoring)

		monitoring.start()
		assistant.start()
		#asyncio.run(assistant.start())
	except Exception as e:
		logger.error(e)


if __name__ == "__main__":
	main()