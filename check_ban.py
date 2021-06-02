from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
import json
import asyncio
from telethon.tl import functions, types
from telethon.tl.types import InputPeerUser
import asyncio
import datetime


logging.basicConfig(level=logging.WARNING)
with open('const.json', 'r', encoding='utf-8') as f:
    consts = json.loads(f.read())

folder_session = consts['folder_session']
folder_configs = consts['folder_configs']


async def send_bot(_client, phone, consts):
    try:
        check_ban_configs = consts['check_ban']
        spambot = await _client.get_entity(check_ban_configs['spambot_entity'])
        await _client.send_message(spambot, check_ban_configs['spambot_send_message'])
        messages = await _client.get_messages(spambot, limit=check_ban_configs['spambot_limit'])
        print('Send bot success: ' + phone)
        return not messages[1].message == check_ban_configs['spambot_sucess_message']
    except Exception as e:
        print('Send bot error: ' + phone)
        print(str(e))
        return True


def main(_config, consts):
    with open('configs/' + _config + '.json', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())

    accounts = config['accounts']
    for account in accounts:
        api_id = account['api_id']
        api_hash = account['api_hash']
        phone = account['phone']
        client = TelegramClient(folder_session + phone, api_id, api_hash)
        client.connect()

        if client.is_user_authorized() and phone != consts['check_phone'][0] and phone != consts['check_phone'][1]:
            isBan = asyncio.get_event_loop().run_until_complete(
                send_bot(client, phone, consts))
            account['ban'] = isBan

        else:
            print('Login fail: ' + phone)

        client.disconnect()

    with open(folder_configs + _config + consts['type_file'][2], 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print('---------------- End ' + _config + ' !(O~0)! ----------------')


index_group = 0
dem = 0
for default_config in consts['default_config']:
    if datetime.datetime.now().strftime(consts['strftime']) == default_config['expire_time'] and default_config['index_group'] == index_group:
        el = [x for x in consts['default_config'] if x['index_group'] == index_group and datetime.datetime.now().strftime(consts['strftime']) == x['expire_time']]
        dem = dem + 1
        if dem == len([x for x in consts['default_config'] if x['index_group'] == index_group and datetime.datetime.now().strftime(consts['strftime']) == x['expire_time']]):
            index_group = index_group + 1
        main(default_config['input'], consts)
