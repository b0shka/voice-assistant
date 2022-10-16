import sqlite3
from common.config import *
from common.tables import *
from utils.logging import logger


class DatabaseSQLite:
	
	def __init__(self):
		try:
			self.db = sqlite3.connect(PATH_FILE_DB, check_same_thread=False)
			self.sql = self.db.cursor()
			logger.info('Success connect database')
		except Exception as e:
			logger.error(e)


	def create_tables(self):
		try:
			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_TELEGRAM_MESSAGES}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							text TEXT NOT NULL,
							from_id INTEGER NOT NULL,
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_VK_MESSAGES}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							text TEXT NOT NULL,
							from_id INTEGER NOT NULL,
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_YANDEX_MESSAGES}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							text TEXT NOT NULL,
							from_user VARCHAR(255) NOT NULL,
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_CONTACTS}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							name VARCHAR(255) NOT NULL,
							phone INTEGER NOT NULL,
							telegram_id INTEGER,
							vk_id INTEGER NOT NULL,
							email VARCHAR(255));""")

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_REQUESTS_ANSWERS}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							text TEXT NOT NULL,
							type VARCHAR(10) NOT NULL,
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")

			self.db.commit()
			logger.info(f'Create table if not exists {TABLE_TELEGRAM_MESSAGES}, {TABLE_VK_MESSAGES}, {TABLE_YANDEX_MESSAGES} in database')
		except Exception as e:
			logger.error(e)


	def get_contacts(self):
		try:
			self.sql.execute(f"SELECT * FROM {TABLE_CONTACTS};")
			contacts = self.sql.fetchall()
			return contacts
		except Exception as e:
			logger.error(e)
			return 0


	def add_telegram_message(self, message, from_id):
		try:
			self.sql.execute(f"INSERT INTO {TABLE_TELEGRAM_MESSAGES} (text, from_id) VALUES (?, ?);", (message, from_id))
			self.db.commit()

			logger.info(f"Добавлено новое сообщение из Telegram от пользователя {from_id}")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def add_vk_message(self, message, from_id):
		try:
			self.sql.execute(f"INSERT INTO {TABLE_VK_MESSAGES} (text, from_id) VALUES (?, ?);", (message, from_id))
			self.db.commit()

			logger.info(f"Добавлено новое сообщение из VK от пользователя {from_id}")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def get_telegram_messages(self):
		try:
			self.sql.execute(f"SELECT * FROM {TABLE_TELEGRAM_MESSAGES};")
			messages = self.sql.fetchall()
			return messages
		except Exception as e:
			logger.error(e)
			return 0


	def get_vk_messages(self):
		try:
			self.sql.execute(f"SELECT * FROM {TABLE_VK_MESSAGES};")
			messages = self.sql.fetchall()
			return messages
		except Exception as e:
			logger.error(e)
			return 0


	def delete_telegram_message(self, id):
		try:
			self.sql.execute(f"DELETE FROM {TABLE_TELEGRAM_MESSAGES} WHERE id = {id};")

			self.db.commit()
			logger.info("Удалено новое сообщение из Telegram")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def delete_vk_message(self, id):
		try:
			self.sql.execute(f"DELETE FROM {TABLE_VK_MESSAGES} WHERE id = {id};")

			self.db.commit()
			logger.info("Удалено новое сообщение из ВКонтакте")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def add_request_answer_assistant(self, text, type):
		try:
			self.sql.execute(f"INSERT INTO {TABLE_REQUESTS_ANSWERS} (text, type) VALUES (?, ?);", (text, type))
			self.db.commit()

			logger.info(f"Добавлена новая запись типа {type}")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def get_requests_answers(self):
		try:
			self.sql.execute(f"SELECT * FROM {TABLE_REQUESTS_ANSWERS};")
			requests_answers = self.sql.fetchall()
			return requests_answers
		except Exception as e:
			logger.error(e)
			return 0


	def delete_old_requests_answer(self, requests_answers):
		try:
			for i in requests_answers:
				self.sql.execute(f"DELETE FROM {TABLE_REQUESTS_ANSWERS} WHERE id = {i[0]};")

			self.db.commit()
			logger.info("Очищены старые запросы/ответы")
			return 1
		except Exception as e:
			logger.error(e)
			return 0