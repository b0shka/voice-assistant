from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from telethon.sync import TelegramClient
from dependency_injector import containers, providers
from common.config import *
from app.services.telegram.telegram import Telegram
from app.services.vk.vk import VK


class ServicesContainer(containers.DeclarativeContainer):

	functions = providers.DependenciesContainer()

	telegram_client = providers.Singleton(
		TelegramClient,
		PATH_FILE_SESSION_TELEGRAM, 
		TELEGRAM_API_ID, 
		TELEGRAM_API_HASH
	)

	vk_session = providers.Singleton(
		VkApi,
		token = VK_TOKEN
	)

	vk_longpoll = providers.Singleton(
		VkLongPoll,
		vk_session
	)

	telegram = providers.Singleton(
		Telegram,
		client = telegram_client,
		messages = functions.messages
	)

	vk = providers.Singleton(
		VK,
		session = vk_session,
		longpoll = vk_longpoll,
		messages = functions.messages
	)