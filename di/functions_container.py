from dependency_injector import containers, providers
from app.functions.notifications import Notifications
from app.functions.messages import Messages
from app.functions.contacts import Contacts


class FunctionsContainer(containers.DeclarativeContainer):

	repository = providers.DependenciesContainer()
	
	notifications = providers.Singleton(
		Notifications,
		db = repository.db_sql
	)

	messages = providers.Singleton(
		Messages,
		db = repository.db_sql
	)

	contacts = providers.Singleton(
		Contacts,
		db = repository.db_sql
	)