from random import choice
from common.states import states
from domain.enum_class.Errors import Errors
from domain.enum_class.ActionsAssistant import ActionsAssistant
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text


def say_error(error: Errors) -> None:
	logger.error(error.value)
	synthesis_text(error.value)


def exit() -> ActionsAssistant:
	exit_answer = ('До скорой встречи', 'До свидания', 'Всего хорошего', 'Удачи', 'Всего доброго', 'Счастл+иво оставаться')
	synthesis_text(choice(exit_answer))
	return ActionsAssistant.EXIT


def nothing_found() -> None:
	not_found_answer = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
	synthesis_text(choice(not_found_answer))


def waiting_select_action() -> None:
	synthesis_text('Какое действие вы хотите выполнить?')


def action_not_found_in_topic() -> None:
	synthesis_text('В этой теме нет такого действия')
	states.WAITING_RESPONSE = False
