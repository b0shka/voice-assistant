from dataclasses import dataclass


@dataclass
class Contact:
	id: int
	first_name: str
	last_name: str | None
	phone: int | None
	telegram_id: int | None
	vk_id: int | None
	email: str | None