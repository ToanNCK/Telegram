from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, \
    UserStatusLastWeek, ChannelParticipantsSearch, InputPeerChannel
import json
from datetime import datetime, timedelta

logging.basicConfig(level=logging.WARNING)

from_date_active = datetime.now().strftime("%Y%m%d")
folder_session = 'session/'

print(from_date_active)

with open('configs/config_test.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

print(config)
accounts = config['accounts']
print("Total account: " + str(len(accounts)))
# date_online_from
from_date_active = (datetime.now() + timedelta(days=-3)).strftime("%Y%m%d")
# list client
clients = []
is_client_message = TelegramClient


def getChanel(client):
    queryKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    all_participants = []
    channel = 'olymp_trade_signals_free'

    for key in queryKey:
        offset = 0
        limit = 100
        while True:
            participants = client(GetParticipantsRequest(
                channel, ChannelParticipantsSearch(key), offset, limit,
                hash=0
            ))
            if not participants.users:
                break
            for user in participants.users:
                try:
                    if re.findall(r"\b[a-zA-Z]", user.first_name)[0].lower() == key:
                        all_participants.append(user)

                except:
                    pass

            offset += len(participants.users)
            print(offset)


for account in accounts:
    account['ban'] = True
    client = TelegramClient(
        folder_session + account['phone'], account['api_id'], account['api_hash'])
    client.connect()
    channel = client.get_entity('https://t.me/fx_phonix_biuld')
    t = InputPeerChannel(1485927933, 1938851854119564210)
    messages = client.get_messages(t, limit=None)
    print(messages)
    # getChanel(client)

with open('configs/config_test.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=4, ensure_ascii=False)
