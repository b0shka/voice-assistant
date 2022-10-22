from random import choice
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text
from common.states import states


def exit():
	try:
		exit_answer = ('До скорой встречи', 'Пока - пока', 'До свидания', 'Всего хорошего', 'Удачи', 'Вчего доброго', 'Счастливо')
		synthesis_text(choice(exit_answer))
		states.change_assistant_work_state(False)
		return 0
	except Exception as e:
		logger.error(e)
		synthesis_text('Произошла ошибка при выходе')
		return -1


def nothing_found():
	try:
		not_found_answer = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
		synthesis_text(choice(not_found_answer))
	except Exception as e:
		logger.error(e)