from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from telethon.sync import TelegramClient
from dependency_injector import containers, providers
from app.services.telegram.telegram import Telegram
from app.services.vk.vk import VK


class ServicesContainer(containers.DeclarativeContainer):

	config = providers.Configuration()
	functions = providers.DependenciesContainer()

	telegram_client = providers.Singleton(
		TelegramClient,
		config.services.path_file_session_telegram, 
		config.services.telegram_api_id, 
		config.services.telegram_api_hash
	)

	vk_session = providers.Singleton(
		VkApi,
		token = config.services.vk_token
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