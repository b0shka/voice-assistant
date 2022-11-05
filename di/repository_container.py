import sqlite3
from dependency_injector import containers, providers
from common.config import PATH_FILE_DB
from repository.database_sqlite_impl import DatabaseSQLiteImpl

from domain.repository.database_sqlite import DatabaseSQLite


class RepositoryContainer(containers.DeclarativeContainer):

	db_connect = providers.Singleton(
		sqlite3.connect,
		PATH_FILE_DB,
		check_same_thread=False
	)

	db_impl = providers.Singleton(
		DatabaseSQLiteImpl,
		conn = db_connect
	)

	db = providers.Singleton(
		DatabaseSQLite
	)