import sqlite3
from common.config import *
from domain.enum_class.Errors import Errors
from domain.enum_class.Tables import TablesDB
from domain.named_tuple.Message import Message
from utils.logging import logger


class DatabaseSQLite:
	
	def __init__(self) -> None | Errors:
		try:
			self._conn = sqlite3.connect(PATH_FILE_DB, check_same_thread=False)
			self._cursor = self._conn.cursor()

			logger.info('База данных успешно подключена')
		except Exception as e:
			logger.error(e)


	def create_tables(self) -> None | Errors:
		try:
			self._cursor.execute(f"""
				CREATE TABLE IF NOT EXISTS `{TablesDB.TELEGRAM_MESSAGES.value}` (
					id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					text TEXT NOT NULL,
					contact_id INTEGER NOT NULL,
					from_id INTEGER,
					first_name VARCHAR(255),
					last_name VARCHAR(255),
					time DATETIME DEFAULT CURRENT_TIMESTAMP
				);
			""")

			self._cursor.execute(f"""
				CREATE TABLE IF NOT EXISTS `{TablesDB.VK_MESSAGES.value}` (
					id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					text TEXT NOT NULL,
					contact_id INTEGER,
					from_id INTEGER,
					first_name VARCHAR(255),
					last_name VARCHAR(255),
					time DATETIME DEFAULT CURRENT_TIMESTAMP
				);
			""")

			self._cursor.execute(f"""
				CREATE TABLE IF NOT EXISTS `{TablesDB.CONTACTS.value}` (
					id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
					first_name VARCHAR(255) NOT NULL,
					last_name VARCHAR(255),
					phone INTEGER,
					telegram_id INTEGER,
					vk_id INTEGER,
					email VARCHAR(255)
				);
			""")

			self._conn.commit()
			logger.info(f'Успешно созданы таблицы в БД если их не было')

		except Exception as e:
			logger.error(e)
			return Errors.CREATE_TABLES


	def get_contacts(self) -> list | Errors:
		try:
			self._cursor.execute(f"SELECT * FROM {TablesDB.CONTACTS.value};")
			return self._cursor.fetchall()
		except Exception as e:
			logger.error(e)
			return Errors.GET_CONTACTS


	def add_telegram_message(self, message: Message) -> None | Errors:
		try:
			if message.contact_id:
				self._cursor.execute(
					f"""
						INSERT INTO {TablesDB.TELEGRAM_MESSAGES.value} (
							text, contact_id, first_name, last_name
						) VALUES (?, ?, ?, ?);
					""", 
					(message.text, message.contact_id, message.first_name, message.last_name)
				)
			else:
				self._cursor.execute(
					f"""
						INSERT INTO {TablesDB.TELEGRAM_MESSAGES.value} (
							text, from_id, first_name, last_name
						) VALUES (?, ?, ?, ?);
					""", 
					(message.text, message.from_id, message.first_name, message.last_name)
				)

			self._conn.commit()

			if message.contact_id:
				logger.info(f"Добавлено новое сообщение из Телеграм от контакта {message.contact_id}")
			else:
				logger.info(f"Добавлено новое сообщение из Телеграм от пользователя {message.first_name} {message.last_name}")

		except Exception as e:
			logger.error(e)
			return Errors.ADD_TELEGRAM_MESSAGE


	def add_vk_message(self, message: Message) -> None | Errors:
		try:
			if message.contact_id:
				self._cursor.execute(
					f"""
						INSERT INTO {TablesDB.VK_MESSAGES.value} (
							text, contact_id, first_name, last_name
						) VALUES (?, ?, ?, ?);
					""",
					(message.text, message.contact_id, message.first_name, message.last_name)
				)
			else:
				self._cursor.execute(
					f"""
						INSERT INTO {TablesDB.VK_MESSAGES.value} (
							text, from_id, first_name, last_name
						) VALUES (?, ?, ?, ?);
					""",
					(message.text, message.from_id, message.first_name, message.last_name)
				)

			self._conn.commit()

			if message.contact_id:
				logger.info(f"Добавлено новое сообщение из ВКонтакте от контакта {message.contact_id}")
			else:
				logger.info(f"Добавлено новое сообщение из ВКонтакте от пользователя {message.first_name} {message.last_name}")

		except Exception as e:
			logger.error(e)
			return Errors.ADD_VK_MESSAGE


	def get_telegram_messages(self) -> list | Errors:
		try:
			self._cursor.execute(f"SELECT * FROM {TablesDB.TELEGRAM_MESSAGES.value};")
			return self._cursor.fetchall()
		except Exception as e:
			logger.error(e)
			return Errors.GET_TELEGRAM_MESSAGES


	def get_vk_messages(self) -> list | Errors:
		try:
			self._cursor.execute(f"SELECT * FROM {TablesDB.VK_MESSAGES.value};")
			return self._cursor.fetchall()
		except Exception as e:
			logger.error(e)
			return Errors.GET_VK_MESSAGES


	def delete_telegram_messages(self) -> None | Errors:
		try:
			self._cursor.execute(f"DELETE FROM {TablesDB.TELEGRAM_MESSAGES.value};")

			self._conn.commit()
			logger.info("Удалены все сообщения из Телеграм")
		except Exception as e:
			logger.error(e)
			return Errors.DELETE_TELEGRAM_MESSAGES


	def delete_telegram_message_by_id(self, id: int) -> None | Errors:
		try:
			self._cursor.execute(f"DELETE FROM {TablesDB.TELEGRAM_MESSAGES.value} WHERE id = {id};")

			self._conn.commit()
			logger.info(f"Удалено сообщение из Телеграм по id: {id}")
		except Exception as e:
			logger.error(e)
			return Errors.DELETE_TELEGRAM_MESSAGE


	def delete_vk_messages(self) -> None | Errors:
		try:
			self._cursor.execute(f"DELETE FROM {TablesDB.VK_MESSAGES.value};")

			self._conn.commit()
			logger.info("Удалены все сообщения из ВКонтакте")
		except Exception as e:
			logger.error(e)
			return Errors.DELETE_VK_MESSAGES


	def delete_vk_message_by_id(self, id: int) -> None | Errors:
		try:
			self._cursor.execute(f"DELETE FROM {TablesDB.VK_MESSAGES.value} WHERE id = {id};")

			self._conn.commit()
			logger.info(f"Удалено новое сообщение из ВКонтакте по id: {id}")
		except Exception as e:
			logger.error(e)
			return Errors.DELETE_VK_MESSAGE
