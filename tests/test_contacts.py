import sys
from unittest import TestCase, main

sys.path.append('/home/q/p/projects/voice-assistant/version_2.0')
from domain.enum_class.Errors import Errors
from domain.named_tuple.Contact import Contact
from app.functions.contacts import Contacts
from common.exceptions.contacts import *


contacts = Contacts()


class TestSettings(TestCase):

	def test_update_contacts(self):
		self.assertEqual(
			contacts.update_contacts(isLauch=True),
			None
		)

	
	def test_convert_contacts(self):
		with self.assertRaises(ErrConvertContacts) as e:
			contacts._convert_contacts([()])
		self.assertEqual(Errors.CONVERT_CONTACTS.value, e.exception.args[0])

		self.assertEqual(
			contacts._convert_contacts([(1, 'Vanya', 'Ivanov', 1234567, 45873465, 4563456, 'email@gmail.com')]),
			[Contact(id=1, first_name='Vanya', last_name='Ivanov', phone=1234567, telegram_id=45873465, vk_id=4563456, email='email@gmail.com')]
		)


if __name__ == "__main__":
	main()