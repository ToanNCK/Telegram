from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
import json
import asyncio
from telethon.tl import functions, types
from telethon.tl.types import InputPeerUser


logging.basicConfig(level=logging.WARNING)
folder_session = 'session/'


async def send_bot(_client):
    spambot = await _client.get_entity('@SpamBot')
    await _client.send_message(spambot, '/start')
    messages = await _client.get_messages(spambot, limit=2)
    for x in messages:
        print(x.message)


def main(_config):
    with open('configs/' + _config + '.json', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())

    accounts = config['accounts']
    for account in accounts:
        api_id = account['api_id']
        api_hash = account['api_hash']
        phone = account['phone']
        print(phone)

        client = TelegramClient(folder_session + phone, api_id, api_hash)
        client.connect()

        if client.is_user_authorized():
            print('Login success: ' + phone)
            asyncio.get_event_loop().run_until_complete(send_bot(client))
        else:
            print('Login fail')

        client.disconnect()
    print('---------------- End ' + _config + ' !(O~0)! ----------------')


main('config_vn')
main('config_en')
