from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
import json
import asyncio
from telethon.tl import functions, types

with open('configs/config_message.json', 'r') as f:
    config = json.loads(f.read())

logging.basicConfig(level=logging.WARNING)

accounts = config['accounts']

folder_session = 'session/'

for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    print(phone)

    client = TelegramClient(folder_session + phone, api_id, api_hash)
    client.start()

    if client.is_user_authorized():
        print('Login success')
    else:
        print('Login fail')


async def main(param_link_souces):
    # channel = await client.get_entity('Fx Phonix')
    for param_link_souce in param_link_souces:
        channel = await client.get_entity(param_link_souce)
        # pass your own args
        messages = await client.get_messages(channel, limit=None)
        messagesClear = []
        # then if you want to get all the messages message
        for x in messages:
            if (x.peer_id.channel_id == 1493876353 or x.peer_id.channel_id == 1462433287) and x.message == None:
                # print(x.message == None)  # return message.text
                messagesClear.append(x)

        await client.delete_messages(channel, messagesClear)
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main(['https://t.me/fx_phonix','https://t.me/fx_phonix_free']))

client.disconnect()
