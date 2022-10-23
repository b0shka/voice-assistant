import sqlite3
from common.config import *
from common.errors import *
from database.tables import *
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
							contact_id INTEGER NOT NULL,
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_VK_MESSAGES}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							text TEXT NOT NULL,
							contact_id INTEGER,
							from_id INTEGER,
							from_name VARCHAR(255),
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_YANDEX_MESSAGES}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							text TEXT NOT NULL,
							contact_id INTEGER,
							from_email VARCHAR(255),
							from_name VARCHAR(255),
							time DATETIME DEFAULT CURRENT_TIMESTAMP);""")

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_CONTACTS}` (
							id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
							first_name VARCHAR(255) NOT NULL,
							last_name VARCHAR(255) NOT NULL,
							phone INTEGER NOT NULL,
							telegram_id INTEGER NOT NULL,
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
			return self.sql.fetchall()
		except Exception as e:
			logger.error(e)
			return 0


	def add_telegram_message(self, message, contact_id):
		try:
			self.sql.execute(f"INSERT INTO {TABLE_TELEGRAM_MESSAGES} (text, contact_id) VALUES (?, ?);", (message, contact_id))
			self.db.commit()

			logger.info(f"Добавлено новое сообщение из Telegram от контакта {contact_id}")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def add_vk_message(self, message, contact_id=None, from_id=None, from_name=None):
		try:
			if contact_id:
				self.sql.execute(f"INSERT INTO {TABLE_VK_MESSAGES} (text, contact_id) VALUES (?, ?);", (message, contact_id))
			else:
				self.sql.execute(f"INSERT INTO {TABLE_VK_MESSAGES} (text, from_id, from_name) VALUES (?, ?);", (message, from_id, from_name))

			self.db.commit()

			if contact_id:
				logger.info(f"Добавлено новое сообщение из VK от контакта {contact_id}")
			else:
				logger.info(f"Добавлено новое сообщение из VK от пользователя {from_name}")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def get_telegram_messages(self):
		try:
			self.sql.execute(f"SELECT * FROM {TABLE_TELEGRAM_MESSAGES};")
			return self.sql.fetchall()
		except Exception as e:
			logger.error(e)
			return 0


	def get_vk_messages(self):
		try:
			self.sql.execute(f"SELECT * FROM {TABLE_VK_MESSAGES};")
			return self.sql.fetchall()
		except Exception as e:
			logger.error(e)
			return 0


	def delete_telegram_messages(self):
		try:
			self.sql.execute(f"DELETE FROM {TABLE_TELEGRAM_MESSAGES};")

			self.db.commit()
			logger.info("Удалены все сообщения из Telegram")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def delete_telegram_message_by_id(self, id):
		try:
			self.sql.execute(f"DELETE FROM {TABLE_TELEGRAM_MESSAGES} WHERE id = {id};")

			self.db.commit()
			logger.info("Удалено новое сообщение из Telegram")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def delete_vk_messages(self):
		try:
			self.sql.execute(f"DELETE FROM {TABLE_VK_MESSAGES};")

			self.db.commit()
			logger.info("Удалены все сообщения из ВКонтакте")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def delete_vk_message_by_id(self, id):
		try:
			self.sql.execute(f"DELETE FROM {TABLE_VK_MESSAGES} WHERE id = {id};")

			self.db.commit()
			logger.info("Удалено новое сообщение из ВКонтакте")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def add_request_answer(self, text, type):
		try:
			self.sql.execute(f"INSERT INTO {TABLE_REQUESTS_ANSWERS} (text, type) VALUES (?, ?);", (text, type))
			self.db.commit()
			logger.info(f"Добавлена новая запись типа {type}")

			last_requests_answers = self.get_requests_answers()
			if len(last_requests_answers) > 10:
				requests_answer = last_requests_answers[::-1]
				result = self.delete_old_requests_answer(requests_answer[10:])
				if result == 0:
					logger.error(ERROR_CLEAN_OLD_REQUESTS_ANSWERS)

			logger.info("Очищены стратые запросы/ответы ассистента")
			return 1
		except Exception as e:
			logger.error(e)
			return 0


	def get_requests_answers(self):
		try:
			self.sql.execute(f"SELECT * FROM {TABLE_REQUESTS_ANSWERS};")
			return self.sql.fetchall()
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