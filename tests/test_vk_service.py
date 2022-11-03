import sys
from unittest import TestCase, main
from environs import Env

sys.path.append('/home/q/p/projects/voice-assistant/version_2.0')
from app.services.vk.vk import VK
from common.exceptions.vk import CantGetUserData, ErrSendVKMessage
from domain.named_tuple.UserServiceData import VKUserData
from domain.enum_class.Errors import Errors


env = Env()
env.read_env('.env')

VK_USER_ID = env.int("VK_USER_ID")
VK_USER_FIRST_NAME = env.str("VK_USER_FIRST_NAME")
VK_USER_LAST_NAME = env.str("VK_USER_LAST_NAME")

vk = VK()


class TestVKService(TestCase):

	def test_get_user_data_by_id(self):
		self.assertEqual(
			vk.get_user_data_by_id(VK_USER_ID),
			VKUserData(
				id=VK_USER_ID, first_name=VK_USER_FIRST_NAME, last_name=VK_USER_LAST_NAME
			)
		)
		
		with self.assertRaises(CantGetUserData) as e:
			vk.get_user_data_by_id(0)
		self.assertEqual(Errors.FAILED_GET_USER_DATA_VK_BY_ID.value, e.exception.args[0])

	
	def test_send_message(self):
		self.assertEqual(
			vk.send_message(VK_USER_ID, 'test mesasge'),
			None
		)
		with self.assertRaises(ErrSendVKMessage) as e:
			vk.send_message(0, 'test mesasge')
		self.assertEqual(Errors.SEND_VK_MESSAGE.value, e.exception.args[0])


if __name__ == "__main__":
	main()