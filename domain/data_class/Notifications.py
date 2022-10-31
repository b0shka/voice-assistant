from dataclasses import dataclass, field
from email.message import Message
from typing import List


@dataclass
class Notifications:
	telegram_messages: List[Message] = field(default_factory=list)
	vk_messages: List[Message] = field(default_factory=list)