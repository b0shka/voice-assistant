from random import choice
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text


def nothing_found():
	try:
		not_found_answer = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
		synthesis_text(choice(not_found_answer))
	except Exception as e:
		logger.error(e)