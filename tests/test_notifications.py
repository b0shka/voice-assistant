import sys
from unittest import TestCase, main

sys.path.append('/home/q/p/projects/voice-assistant/version_2.0')
from domain.enum_class.Errors import Errors
from domain.named_tuple.Contact import Contact
from domain.named_tuple.Message import Message
from app.functions.notifications import Notifications
from app.assistant import configure_assistant
from common.exceptions.notifications import *
from common.exceptions.messages import CantFoundContact


notifications = Notifications()
configure_assistant()


class TestNotifications(TestCase):
	
	def test_get_contact_by_contact_id(self):
		self.assertEqual(
			type(notifications.get_contact_by_contact_id(1)),
			Contact
		)
		self.assertRaises(
			CantFoundContact,
			notifications.get_contact_by_contact_id,
			-1
		)


	def test_update_notifications(self):
		self.assertEqual(
			notifications.update_notifications(isLauch=True),
			None
		)

	
	def test_update_vk_messages(self):
		self.assertEqual(
			notifications._update_vk_messages(),
			None
		)


	def test_update_telegram_messages(self):
		self.assertEqual(
			notifications._update_telegram_messages(),
			None
		)

	
	def test_convert_mesage(self):
		self.assertEqual(
			notifications._convert_message([1, 'text', 1, 5465447, 'Vanya', 'Ivanov']),
			Message(text='text', contact_id=1, from_id=5465447, first_name='Vanya', last_name='Ivanov')
		)

		with self.assertRaises(ErrConvertMessage) as e:
			notifications._convert_message([])
		self.assertEqual(Errors.CONVERT_MESSAGE.value, e.exception.args[0])

		with self.assertRaises(ErrConvertMessage) as e:
			notifications._convert_message(['text', 1, 5465447, 'Vanya', 'Ivanov'])
		self.assertEqual(Errors.CONVERT_MESSAGE.value, e.exception.args[0])



if __name__ == "__main__":
	main()