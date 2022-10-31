from speechkit import Session
from common.config import YANDEX_CLOUD_API_KEY


session = Session.from_api_key(
	YANDEX_CLOUD_API_KEY
)