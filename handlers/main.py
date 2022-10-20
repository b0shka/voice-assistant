import pymorphy2
from list_requests.commands import COMMANDS


command = 'просмотреть мои уведомления'
list_command = command.split()
morph = pymorphy2.MorphAnalyzer()
topics = {}

for i in list_command:
	if i != '':
		p = morph.parse(i.replace("\u200b", ""))[0]
		normal_form = p.normal_form

		for i in COMMANDS.keys():
			if normal_form in COMMANDS[i]['function']:
				if i not in topics.keys():
					topics[i] = 1
				else:
					topics[i] += 1

			if normal_form in COMMANDS[i]['actions']:
				if i not in topics.keys():
					topics[i] = 1
				else:
					topics[i] += 1

			if normal_form in COMMANDS[i]['pronouns']:
				if i not in topics.keys():
					topics[i] = 1
				else:
					topics[i] += 1

print(topics)