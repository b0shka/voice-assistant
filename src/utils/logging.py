import os
import logging


if not os.path.exists('logs'):
	os.mkdir('logs')

logging.basicConfig(filename="logs/info.log", format = u'[%(levelname)s][%(asctime)s] %(funcName)s:%(lineno)s: %(message)s', level='INFO')
logger = logging.getLogger()