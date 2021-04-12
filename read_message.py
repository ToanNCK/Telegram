from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetMessagesViewsRequest
import json
import asyncio
from telethon.tl import functions, types

with open('config_message.json', 'r') as f:
    config = json.loads(f.read())

logging.basicConfig(level=logging.WARNING)

accounts = config['accounts_auto']

folder_session = 'session/'
clients = []
for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    print(phone)

    client = TelegramClient(folder_session + phone, api_id, api_hash)
    client.start()
    # clients.append(client)

    if client.is_user_authorized():
        print('Login success')
    else:
        print('Login fail')


async def main():
    channel = await client.get_entity('Fx Phonix VIP')
    # pass your own args
    messages = await client.get_messages(channel, limit=5)
    messagesViews = []
    # then if you want to get all the messages message
    for x in messages:
        # print(x.id)  # return message.text
        messagesViews.append(x.id)

    await client(GetMessagesViewsRequest(peer=channel,id=messagesViews,increment=True))
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

client.disconnect()
