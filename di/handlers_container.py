from dependency_injector import containers, providers
from app.handlers.handler_command import HandlerCommand
from app.handlers.handler_topic import HandlerTopic


class HandlersContainer(containers.DeclarativeContainer):

	functions = providers.DependenciesContainer()

	handler_topic = providers.Singleton(
		HandlerTopic,
		notifications = functions.notifications,
		settings = functions.settings
	)

	handler_command = providers.Singleton(
		HandlerCommand,
		handler_topic = handler_topic
	)