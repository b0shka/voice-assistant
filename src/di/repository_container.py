import sqlite3
from dependency_injector import containers, providers
from repository.database_sqlite_impl import DatabaseSQLiteImpl


class RepositoryContainer(containers.DeclarativeContainer):

	config = providers.Configuration()

	db_sql_connect = providers.Singleton(
		sqlite3.connect,
		config.repository.path_file_db,
		check_same_thread=False
	)

	db_sql = providers.Singleton(
		DatabaseSQLiteImpl,
		conn = db_sql_connect
	)