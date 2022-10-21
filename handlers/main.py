import pymorphy2
from list_requests.commands import COMMANDS
from list_requests.config import *


command = 'просмотреть мои уведомления и выйти'
list_command = command.split()
morph = pymorphy2.MorphAnalyzer()
topics = {}

for i in list_command:
	if i != '':
		p = morph.parse(i.replace("\u200b", ""))[0]
		normal_form = p.normal_form

		for i in COMMANDS.keys():
			if i not in topics.keys():
				topics[i] = {
					FUNCTION: 0,
					ACTIONS: 0,
					PRONOUNS: 0
				}

			if normal_form in COMMANDS[i][FUNCTION]:
				topics[i][FUNCTION] += 1

			if normal_form in COMMANDS[i][ACTIONS]:
				topics[i][ACTIONS] += 1

			if normal_form in COMMANDS[i][PRONOUNS]:
				topics[i][PRONOUNS] += 1

print(topics)