from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetMessagesViewsRequest
import json
import asyncio
from telethon.tl import functions, types
import traceback

with open('configs/config_read_message.json', 'r') as f:
    config = json.loads(f.read())

logging.basicConfig(level=logging.WARNING)

accounts = config['accounts']

folder_session = 'session/'

async def main(client):
    channel = await client.get_entity('Fx Phonix VIP')
    # pass your own args
    messages = await client.get_messages(channel, limit=20)
    messagesViews = []
    # then if you want to get all the messages message
    for x in messages:
        # print(x.id)  # return message.text
        messagesViews.append(x.id)

    await client(GetMessagesViewsRequest(peer=channel,id=messagesViews,increment=True))
            

def read_message():
    print("Total account: " + str(len(accounts)))
    for account in accounts:
        api_id = account['api_id']
        api_hash = account['api_hash']
        phone = account['phone']
        if phone != "+84585771080" and phone != "+84567327859":
            try:
                clientThis = TelegramClient(folder_session + phone, api_id, api_hash)
                clientThis.connect()
                asyncio.get_event_loop().run_until_complete(main(clientThis))
                print('Read Message' + phone +' success')
                clientThis.disconnect()
            except Exception as e:
                traceback.print_exc()
                clientThis.disconnect()
                continue


read_message()

