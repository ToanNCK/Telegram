from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, \
    UserStatusLastWeek
import json
from datetime import datetime, timedelta

logging.basicConfig(level=logging.WARNING)

from_date_active = datetime.now().strftime("%Y%m%d")


print(from_date_active)

with open('configs/config_test.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

print(config)
accounts = config['accounts']
print("Total account: " + str(len(accounts)))
# group target
group_target_id = config['group_target']
# group source
group_source_id = config['group_source']
# date_online_from
from_date_active = (datetime.now() + timedelta(days=-3)).strftime("%Y%m%d")
# list client
clients = []
is_client_message = TelegramClient
for account in accounts:
    account['ban'] = True

with open('configs/config_test.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


