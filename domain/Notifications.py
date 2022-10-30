from dataclasses import dataclass
from email.message import Message
from typing import List


@dataclass
class Notifications:
	telegram_messages: List[Message] = []
	vk_messages: List[Message] = []