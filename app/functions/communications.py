from random import choice
from common.states import states
from domain.enum_class.ActionsAssistant import ActionsAssistant
from utils.speech.yandex_synthesis import synthesis_text
from database.database_sqlite import DatabaseSQLite


class Communications:

	def __init__(self) -> None:
		self.db = DatabaseSQLite()


	def exit(self) -> ActionsAssistant:
		exit_answer = ('До скорой встречи', 'До свидания', 'Всего хорошего', 'Удачи', 'Всего доброго', 'Счастл+иво оставаться')
		synthesis_text(choice(exit_answer))
		return ActionsAssistant.EXIT


	def nothing_found(self) -> None:
		not_found_answer = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
		synthesis_text(choice(not_found_answer))


	def waiting_select_action(self) -> None:
		synthesis_text('Какое действие вы хотите выполнить?')

	
	def action_not_found_in_topic(self) -> None:
		synthesis_text('В этой теме нет такого действия')
		states.WAITING_RESPONSE = False
