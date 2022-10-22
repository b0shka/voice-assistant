from telethon.sync import TelegramClient


API_ID = 0 # api id of your application created on the site my.telegram.org
API_HASH = "api_hash" # api hash of your application created on the site my.telegram.org
NAME_SESSION = 'telegram' # the path to the .session file

client = TelegramClient(NAME_SESSION, API_ID, API_HASH)
client.start()
