import logging
from telethon import sync, TelegramClient, events
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
import time
import traceback
import datetime
import os
import json
import asyncio

logging.basicConfig(level=logging.WARNING)
folder_session = 'session/'

# Thêm user vào channel vip
async def client_channel_phonix_vip(client_channel):
    await client_channel(ImportChatInviteRequest('3skfIIp18dU1MmQ1'))

# Thêm user vào group free
async def client_channel_phonix_free(client_channel):
    channel = await client_channel.get_entity('t.me/fx_phonix')
    await client_channel(JoinChannelRequest(channel))

# Thêm user vào group souces
async def client_channel_souces(client_channel, link_souces):
    channel = await client_channel.get_entity(link_souces)
    await client_channel(JoinChannelRequest(channel))


async def main(param_client, param_link_souces):
    #task1 = asyncio.create_task(client_channel_phonix_vip(param_client))
    #task2 = asyncio.create_task(client_channel_phonix_free(param_client))
    print(f"started at {time.strftime('%X')}")
    #await task1
    #await task2
    for param_link_souce in param_link_souces:
        task3 = asyncio.create_task(client_channel_souces(param_client, param_link_souce))
        await task3
    #time.sleep(600)
    print(f"finished at {time.strftime('%X')}")


def add_member_channel(config_json, client_link_souces):
    with open(config_json, 'r', encoding='utf-8') as f:
        config = json.loads(f.read())
    accounts = config['accounts']
    print("Total account: " + str(len(accounts)))
    for account in accounts:
        api_id = account['api_id']
        api_hash = account['api_hash']
        phone = account['phone']
        if phone != "+84585771080":
            try:
                client = TelegramClient(folder_session + phone, api_id, api_hash)
                client.connect()
                asyncio.get_event_loop().run_until_complete(main(client, client_link_souces))
                print('Add member' + phone +' success')
                client.disconnect()
            except Exception as e:
                print(e)
                traceback.print_exc()
                client.disconnect()
                continue


# add_member_channel('config_en.json', ['t.me/GermanCoin_GCXChat', 'https://t.me/cointiger_en', 'https://t.me/olymptrade_live'])
# add_member_channel('config_vn.json', ['t.me/SkyGroupFreeSignals'])

#add_member_channel('config.json', ['t.me/GermanCoin_GCXChat', 'https://t.me/cointiger_en', 'https://t.me/olymptrade_live'])

add_member_channel('config.json', ['https://t.me/VFITeamgroup','https://t.me/ForexTraders_VN', 'https://t.me/vietnamtraders', 'https://t.me/SkyGroupFreeSignals', 'https://t.me/wintowinvision'])
