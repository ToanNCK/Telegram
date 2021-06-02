from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetMessagesViewsRequest
import json
import asyncio
from telethon.tl import functions, types
import traceback


logging.basicConfig(level=logging.WARNING)
with open('const.json', 'r', encoding='utf-8') as f:
    consts = json.loads(f.read())

folder_session = consts['folder_session']
read_mesage_consts = consts['read_mesage']

with open(consts['folder_configs'] + read_mesage_consts['config_read_message'] + consts['type_file'][2], 'r') as f:
    config = json.loads(f.read())

accounts = config['accounts']


async def main(client):
    channel = await client.get_entity(read_mesage_consts['entity_vip'])
    # pass your own args
    messages = await client.get_messages(channel, limit=read_mesage_consts['limit'])
    messagesViews = []
    # then if you want to get all the messages message
    for x in messages:
        # print(x.id)  # return message.text
        messagesViews.append(x.id)

    await client(GetMessagesViewsRequest(peer=channel, id=messagesViews, increment=True))


def read_message():
    print("Total account: " + str(len(accounts)))
    for account in accounts:
        api_id = account['api_id']
        api_hash = account['api_hash']
        phone = account['phone']
        if phone != consts['check_phone'][0] and phone != consts['check_phone'][1]:
            try:
                clientThis = TelegramClient(
                    folder_session + phone, api_id, api_hash)
                clientThis.connect()
                asyncio.get_event_loop().run_until_complete(main(clientThis))
                print('Read Message' + phone + ' success')
                clientThis.disconnect()
            except Exception as e:
                traceback.print_exc()
                clientThis.disconnect()
                continue


read_message()
