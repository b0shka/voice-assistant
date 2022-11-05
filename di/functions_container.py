from dependency_injector import containers, providers
from app.functions.notifications import Notifications
from app.functions.messages import Messages
from app.functions.settings import Settings


class FunctionsContainer(containers.DeclarativeContainer):

	repository = providers.DependenciesContainer()
	
	notifications = providers.Singleton(
		Notifications,
		db = repository.db_impl
	)

	messages = providers.Singleton(
		Messages,
		db = repository.db_impl
	)

	settings = providers.Singleton(
		Settings,
		db = repository.db_impl
	)