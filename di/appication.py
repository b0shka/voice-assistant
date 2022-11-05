from dependency_injector import containers, providers
from app.assistant import Assistant
from app.monitoring import Monitoring
from di.repository_container import RepositoryContainer
from di.functions_container import FunctionsContainer
from di.services_container import ServicesContainer
from di.handlers_container import HandlersContainer


class Application(containers.DeclarativeContainer):

	config = providers.Configuration()

	repository = providers.Container(
		RepositoryContainer,
		config = config
	)

	functions = providers.Container(
		FunctionsContainer,
		repository = repository
	)

	handlers = providers.Container(
		HandlersContainer,
		functions = functions
	)

	services = providers.Container(
		ServicesContainer,
		functions = functions,
		config = config
	)

	assistant = providers.Singleton(
		Assistant,
		settings = functions.settings,
		handler_command = handlers.handler_command
	)

	monitoring = providers.Singleton(
		Monitoring,
		vk = services.vk,
		telegram = services.telegram
	)
