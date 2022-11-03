import sys
from unittest import TestCase, main

sys.path.append('/home/q/p/projects/voice-assistant/version_2.0')
from domain.named_tuple.Contact import Contact
from app.functions.notifications import Notifications
from app.assistant import launch
from common.exceptions.messages import CantFoundContact


notifications = Notifications()
launch()


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


if __name__ == "__main__":
	main()