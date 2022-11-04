from domain.named_tuple.Message import Message


class DatabaseSQLite:
	'''Interface for worg with sqlite database'''

	def create_tables(self) -> None:
		raise NotImplementedError

	def get_contacts(self) -> list:
		raise NotImplementedError

	def add_telegram_message(self, message: Message) -> None:
		raise NotImplementedError

	def add_vk_message(self, message: Message) -> None:
		raise NotImplementedError