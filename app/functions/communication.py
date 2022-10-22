from random import choice
from utils.logging import logger
from utils.speech.yandex_synthesis import synthesis_text


class Communication:

	def __init__(self):
		try:
			pass
		except Exception as e:
			logger.error(e)


	def exit(self):
		try:
			exit_answer = ('До скорой встречи', 'До свидания', 'Всего хорошего', 'Удачи', 'Всего доброго', 'Счастл+иво оставаться')
			synthesis_text(choice(exit_answer))
			return 0
		except Exception as e:
			logger.error(e)
			synthesis_text('Произошла ошибка при выходе')
			return -1


	def nothing_found(self):
		try:
			not_found_answer = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
			synthesis_text(choice(not_found_answer))
		except Exception as e:
			logger.error(e)