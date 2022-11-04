import sqlite3
from dependency_injector import containers, providers
from common.config import PATH_FILE_DB
from app.functions.notifications import Notifications
from app.functions.messages import Message
from app.functions.settings import Settings
from app.handlers.handler_command import HandlerCommand
from app.handlers.handler_topic import HandlerTopic
from data.database_sqlite_impl import DatabaseSQLiteImpl


class FunctionsContainer(containers.DeclarativeContainer):

	db_connect = providers.Singleton(
		sqlite3.connect,
		PATH_FILE_DB,
		check_same_thread=False
	)

	db = providers.Singleton(
		DatabaseSQLiteImpl,
		conn = db_connect
	)
	
	notifications = providers.Singleton(
		Notifications,
		db = db
	)

	messages = providers.Singleton(
		Message,
		db = db
	)

	settings = providers.Singleton(
		Settings,
		db = db
	)

	handler_topic = providers.Singleton(
		HandlerTopic,
		notifications = notifications,
		settings = settings
	)

	handler_command = providers.Singleton(
		HandlerCommand,
		handler_topic = handler_topic
	)