from domain.named_tuple.Message import Message


class DatabaseSQLite:
	'''Интерфейс класса для работы с базой данных SQLite'''

	def create_tables(self) -> None:
		...

	def get_contacts(self) -> list:
		...

	def add_telegram_message(self, message: Message) -> None:
		...

	def add_vk_message(self, message: Message) -> None:
		...

	def get_telegram_messages(self) -> list:
		...

	def get_vk_messages(self) -> list:
		...
	
	def delete_telegram_messages(self) -> None:
		...

	def delete_telegram_message_by_id(self, id: int) -> None:
		...

	def delete_vk_messages(self) -> None:
		...

	def delete_vk_message_by_id(sel, id: int) -> None:
		...