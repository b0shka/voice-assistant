import logging
import os


if not os.path.exists('info'):
	os.mkdir('info')

logging.basicConfig(filename="info/info.log", format = u'[%(levelname)s][%(asctime)s] %(funcName)s:%(lineno)s: %(message)s', level='INFO')
logger = logging.getLogger()

#TOKEN_VK = os.getenv("TOKEN_VK")
PATH_FILE_DB = '/home/q/p/projects/voice-assistant/version_2.0/settings/server.db'