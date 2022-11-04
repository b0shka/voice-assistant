import threading
from dependency_injector.wiring import Provide, inject
from domain.enum_class.Errors import Errors
from app.assistant import Assistant
#from app.monitoring import Monitoring
from app.functions.communications import say_error
from app.functions.settings import Settings
from app.handlers.handler_command import HandlerCommand
from utils.logging import logger
from di.functions_container import FunctionsContainer


@inject
def main(
	settings: Settings = Provide[FunctionsContainer.settings],
	handler_command: HandlerCommand = Provide[FunctionsContainer.handler_command]
) -> None:
	try:
		assistant = Assistant(settings, handler_command)
		#monitoring = Monitoring()
		#monitoring_thread = threading.Thread(target=monitoring.start)

		#monitoring_thread.start()
		assistant.start_listen()

	except Exception as e:
		say_error(Errors.UNDEFIND)
		logger.error(e)


if __name__ == "__main__":
	container = FunctionsContainer()
	container.wire(modules=[__name__])

	main()