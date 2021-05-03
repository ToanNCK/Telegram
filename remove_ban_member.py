from telethon import TelegramClient, connection, functions, types
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, \
    UserStatusLastWeek, ChatBannedRights, InputPeerUser
import json
from datetime import datetime, timedelta

logging.basicConfig(level=logging.WARNING)
folder_session = 'session/'
phone = '+84567327859'
api_id = 2641186
api_hash = 'e4ebf70b5b8535b794c3032dd7ecf9db'


def get_group():
    client = TelegramClient(folder_session + phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        print('Login fail, need to run init_session')
    else:
        get_data_group(client)


def get_data_group(client):
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
                remove_member(client, group)
                get_data_user(client, group)
        except Exception as e:
            print(e)
            print('error save group')
    with open('data_remove/group/' + phone + '.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def get_data_user(client, group):
    group_id = str(group.id)
    print(group_id)

    all_participants = client.get_participants(group, aggressive=True)
    results = []
    today = datetime.now()
    last_week = today + timedelta(days=-7)
    last_month = today + timedelta(days=-30)
    path_file = 'data_remove/user/' + phone + "_" + group_id + '.json'

    for user in all_participants:
        # print(user)
        # print(type(user.status))
        try:
            if isinstance(user.status, UserStatusRecently):
                continue
            else:
                if isinstance(user.status, UserStatusLastMonth):
                    date_online = last_month
                if isinstance(user.status, UserStatusLastWeek):
                    date_online = last_week
                if isinstance(user.status, UserStatusOffline):
                    continue
                date_online_str = date_online.strftime("%Y%m%d")

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


def remove_member(client, group):
    dem = 0
    channel = client.get_entity(group.username)
    with open('data_remove/user/' + phone + "_" + str(group.id) + '.json', 'r', encoding='utf-8') as f:
        users = json.loads(f.read())
    for user in users:
        user_to_ban = InputPeerUser(
            int(user['user_id']), int(user['access_hash']))
        client(EditBannedRequest(
            channel, user_to_ban, ChatBannedRights(
                until_date=None,
                view_messages=True
            )
        ))
        dem += 1
        if dem >= 150:
            break
    # delete 150 member nghỉ 15 phút


get_group()
