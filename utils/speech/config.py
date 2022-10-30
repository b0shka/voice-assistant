from speechkit import Session
from common.config import YANDEX_CLOUD_API_KEY


#session = Session.from_yandex_passport_oauth_token(
#	YANDEX_CLOUD_OAUTH_TOKEN, 
#	YANDEX_CLOUD_CATALOG_ID
#)
session = Session.from_api_key(
	YANDEX_CLOUD_API_KEY
)

FINITE = 'finite'
INTERMEDIATE = 'intermediate'