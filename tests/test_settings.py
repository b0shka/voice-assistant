import sys
from unittest import TestCase, main

sys.path.append('/home/q/p/projects/voice-assistant/version_2.0')
from domain.enum_class.Errors import Errors
from domain.named_tuple.Contact import Contact
from domain.named_tuple.Message import Message
from app.functions.settings import Settings
from common.exceptions.settings import *


settings = Settings()


class TestSettings(TestCase):

	def test_update_contacts(self):
		self.assertEqual(
			settings.update_contacts(isLauch=True),
			None
		)

	
	def test_convert_contacts(self):
		with self.assertRaises(ErrConvertContacts) as e:
			settings._convert_contacts([()])
		self.assertEqual(Errors.CONVERT_CONTACTS.value, e.exception.args[0])

		self.assertEqual(
			settings._convert_contacts([(1, 'Vanya', 'Ivanov', 1234567, 45873465, 4563456, 'email@gmail.com')]),
			[Contact(id=1, first_name='Vanya', last_name='Ivanov', phone=1234567, telegram_id=45873465, vk_id=4563456, email='email@gmail.com')]
		)

	
	def test_update_notifications(self):
		self.assertEqual(
			settings.update_notifications(isLauch=True),
			None
		)

	
	def test_update_vk_messages(self):
		self.assertEqual(
			settings._update_vk_messages(),
			None
		)


	def test_update_telegram_messages(self):
		self.assertEqual(
			settings._update_telegram_messages(),
			None
		)

	
	def test_convert_mesage(self):
		self.assertEqual(
			settings._convert_message([1, 'text', 1, 5465447, 'Vanya', 'Ivanov']),
			Message(text='text', contact_id=1, from_id=5465447, first_name='Vanya', last_name='Ivanov')
		)

		with self.assertRaises(ErrConvertMessage) as e:
			settings._convert_message([])
		self.assertEqual(Errors.CONVERT_MESSAGE.value, e.exception.args[0])

		with self.assertRaises(ErrConvertMessage) as e:
			settings._convert_message(['text', 1, 5465447, 'Vanya', 'Ivanov'])
		self.assertEqual(Errors.CONVERT_MESSAGE.value, e.exception.args[0])


if __name__ == "__main__":
	main()