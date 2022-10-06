import sqlite3
from common.config import *
from common.tables import *


class Database:
	
	def __init__(self):
		try:
			self.db = sqlite3.connect(PATH_FILE_DB)
			self.sql = self.db.cursor()
			logger.info('Success initializate database')
			self.create_tables()
		except Exception as e:
			logger.error(e)


	def create_tables(self):
		try:
			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_MESSAGES}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							task TEXT,
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")
			self.db.commit()
			logger.info(f'Create table if not exists {TABLE_MESSAGES} in database')
		except Exception as e:
			logger.error(e)