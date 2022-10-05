import sqlite3
from common.config import *
from common.tables import *


class Database:
	
	def __init__(self):
		try:
			self.db = sqlite3.connect(PATH_FILE_DB)
			self.sql = self.db.cursor()
			self.create_tables()
			logger.info('Success initializate database')
		except Exception as e:
			logger.error(e)


	def create_tables(self):
		try:
			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_TASKS}` (
							id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
							task TEXT,
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")
			self.db.commit()
			logger.info(f'Создана таблица {TABLE_TASKS} в БД')
		except Exception as e:
			logger.error(e)