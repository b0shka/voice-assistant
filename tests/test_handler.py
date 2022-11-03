import sys
from unittest import TestCase, main

sys.path.append('/home/q/p/projects/voice-assistant/version_2.0')
from domain.enum_class.TopicsNames import TopicsNames
from domain.enum_class.FunctionsNames import FunctionsNames
from domain.named_tuple.Topic import Topic
from app.handlers.handler_topic import determinate_topic, check_nested_functions


class TestHandlers(TestCase):

	def test_determinate_topic(self):
		self.assertEqual(
			determinate_topic('мои уведомления'),
			Topic(topic=TopicsNames.NOTIFICATIONS_TOPIC, functions=FunctionsNames.SHOW_NOTIFICATIONS)
		)
		self.assertEqual(
			determinate_topic('очистить мои уведомления'),
			Topic(topic=TopicsNames.NOTIFICATIONS_TOPIC, functions=FunctionsNames.CLEAN_NOTIFICATIONS)
		)
		self.assertEqual(
			determinate_topic('уведомления'),
			Topic(topic=TopicsNames.NOTIFICATIONS_TOPIC, functions=None)
		)
		self.assertEqual(
			determinate_topic('посмотреть уведомления', TopicsNames.NOTIFICATIONS_TOPIC),
			Topic(topic=TopicsNames.NOTIFICATIONS_TOPIC, functions=FunctionsNames.SHOW_NOTIFICATIONS)
		)

		self.assertEqual(
			determinate_topic('сообщения в телеграм'),
			Topic(topic=TopicsNames.TELEGRAM_MESSAGES_TOPIC, functions=None)
		)
		self.assertEqual(
			determinate_topic('очистить сообщения в телеграм'),
			Topic(topic=TopicsNames.TELEGRAM_MESSAGES_TOPIC, functions=FunctionsNames.CLEAN_TELEGRAM_MESSAGES)
		)
		self.assertEqual(
			determinate_topic('написать сообщение в телеграм'),
			Topic(topic=TopicsNames.TELEGRAM_MESSAGES_TOPIC, functions=FunctionsNames.SEND_TELEGRAM_MESSAGES)
		)

		self.assertEqual(
			determinate_topic('обновить контакты'),
			Topic(topic=TopicsNames.CONTACTS_TOPIC, functions=FunctionsNames.UPDATE_CONTACTS)
		)
		self.assertEqual(
			determinate_topic('контакты'),
			Topic(topic=TopicsNames.CONTACTS_TOPIC, functions=None)
		)

		self.assertEqual(
			determinate_topic('посмотреть сообщения в вк'),
			Topic(topic=TopicsNames.VK_MESSAGES_TOPIC, functions=FunctionsNames.SHOW_VK_MESSAGES)
		)

		self.assertEqual(
			determinate_topic('выйти'),
			Topic(topic=TopicsNames.EXIT_TOPIC, functions=None)
		)
		self.assertEqual(
			determinate_topic('неизвестная команда'),
			Topic(topic=None, functions=None)
		)


	def test_check_nested_functions(self):
		self.assertEqual(
			check_nested_functions(
				TopicsNames.NOTIFICATIONS_TOPIC
			),
			True
		)
		self.assertEqual(
			check_nested_functions(
				TopicsNames.CONTACTS_TOPIC
			),
			True
		)
		self.assertEqual(
			check_nested_functions(
				TopicsNames.TELEGRAM_MESSAGES_TOPIC
			),
			True
		)
		self.assertEqual(
			check_nested_functions(
				TopicsNames.VK_MESSAGES_TOPIC
			),
			True
		)
		self.assertEqual(
			check_nested_functions(
				TopicsNames.EXIT_TOPIC
			),
			False
		)
		self.assertEqual(
			check_nested_functions(
				TopicsNames.SOUND_TOPIC
			),
			True
		)


if __name__ == "__main__":
	main()