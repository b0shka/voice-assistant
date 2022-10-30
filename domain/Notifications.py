from dataclasses import dataclass


@dataclass
class Notifications:
	telegram_messages: list = []
	vk_messages: list = []