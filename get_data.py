from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, \
    UserStatusLastWeek
import json
from datetime import datetime, timedelta

logging.basicConfig(level=logging.WARNING)
with open('const.json', 'r', encoding='utf-8') as f:
    consts = json.loads(f.read())

get_data_consts = consts['get_data']


def get_group(phone, api_id, api_hash):
    folder_session = consts['folder_session']
    client = TelegramClient(folder_session + phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        print('Login fail, need to run init_session')
    else:
        get_data_group(client, phone)


def get_data_group(client, phone):
    print('getting data ' + phone)
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    query = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(query.chats)
    for chat in chats:
        try:
            if chat.megagroup is not None and chat.access_hash is not None:
                groups.append(chat)
        except:
            continue

    results = []
    for group in groups:
        try:
            tmp = {
                'group_id': str(group.id),
                'access_hash': str(group.access_hash),
                'title': str(group.title),
                'username': str(group.username),
                'participants_count': group.participants_count
            }
            results.append(tmp)

            if group.megagroup == True:
                get_data_user(client, group)
        except Exception as e:
            print(e)
            print('error save group')
    with open(get_data_consts['data_group'] + phone + consts['type_file'][2], 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def get_data_user(client, group):
    group_id = str(group.id)
    print(group_id)

    all_participants = client.get_participants(group, aggressive=True)
    results = []
    today = datetime.now()
    last_week = today + timedelta(days=-7)
    last_month = today + timedelta(days=-30)
    path_file = get_data_consts['data_user'] + \
        phone + "_" + group_id + consts['type_file'][2]

    for user in all_participants:
        # print(user)
        # print(type(user.status))
        try:
            if isinstance(user.status, UserStatusRecently):
                date_online_str = 'online'
            else:
                if isinstance(user.status, UserStatusLastMonth):
                    date_online = last_month
                if isinstance(user.status, UserStatusLastWeek):
                    date_online = last_week
                if isinstance(user.status, UserStatusOffline):
                    date_online = user.status.was_online

                date_online_str = date_online.strftime(consts['strftime'])

            tmp = {
                'user_id': str(user.id),
                'access_hash': str(user.access_hash),
                'username': str(user.username),
                'date_online': date_online_str,
            }
            results.append(tmp)
        except:
            print("Error get user")
    with open(path_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


with open(consts['folder_configs'] + get_data_consts['config_data'] + consts['type_file'][2], 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

accounts = config['accounts']

folder_session = consts['folder_session']

for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    if phone != consts['check_phone'][0] and phone != consts['check_phone'][1]:
        print(phone)
        get_group(phone, api_id, api_hash)
