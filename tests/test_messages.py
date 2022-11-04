import sys
from unittest import TestCase, main

sys.path.append('/home/q/p/projects/voice-assistant/version_2.0')
from domain.enum_class.Services import Services
from app.functions.messages import Messages
from app.assistant import configure_assistant
from common.exceptions.messages import CantFoundContact


messages = Messages()
configure_assistant()


class TestMessages(TestCase):

	def test_get_contact_by_from_id(self):
		self.assertRaises(
			CantFoundContact,
			messages.get_contact_by_from_id,
			0, Services.VK
		)
		self.assertRaises(
			CantFoundContact,
			messages.get_contact_by_from_id,
			'invalid id', Services.TELEGRAM
		)


	def test_new_telegram_message(self):
		self.assertEqual(
			messages.new_telegram_message(
				{
					'from_id': {'user_id': 0},
					'message': 'test message'
				}
			),
			None
		)
		self.assertEqual(
			messages.new_telegram_message(
				{
					'from_id': {'invalid_key': 0},
					'message': 'test message'
				}
			),
			None
		)
		self.assertEqual(
			messages.new_telegram_message(
				{
					'from_id': {'user_id': 'invalid_id'},
					'message': 'test message'
				}
			),
			None
		)


if __name__ == "__main__":
	main()