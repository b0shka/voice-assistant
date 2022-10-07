from telethon.sync import TelegramClient, events
from common.config import *


client = TelegramClient(
			PATH_FILE_SESSION_TELEGRAM, 
			TELEGRAM_API_ID, 
			TELEGRAM_API_HASH
		)

@client.on(events.NewMessage())
async def handler(event):
	message = event.message.to_dict()
	print(message)

client.start()
client.run_until_disconnected()