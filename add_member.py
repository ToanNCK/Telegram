import logging
from telethon import sync, TelegramClient, events
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError
from datetime import timedelta
import time
import traceback
import datetime
import os
import json
import asyncio

logging.basicConfig(level=logging.WARNING)

root_path = os.path.dirname(os.path.abspath(__file__)) + "/"
print(root_path)
with open('const.json', 'r', encoding='utf-8') as f:
    consts = json.loads(f.read())

start_time = datetime.datetime.now()
folder_session = consts['folder_session']
folder_log = consts['folder_log']
folder_configs = consts['folder_configs']


def get_group_by_id(groups, group_id):
    for group in groups:
        if (group_id == int(group['group_id'])):
            return group
    return None


def disconnect_remove_client(is_client, is_current_client, is_filter_clients):
    if check_phone(is_current_client['phone']):
        print("remove client: " + is_current_client['phone'])
        is_client.disconnect()
    is_filter_clients.remove(is_current_client)


def check_phone(is_phone):
    if is_phone not in consts['check_phone']:
        return True
    else:
        return False


async def client_message(client_ms, input_peer_channels):
    for input_peer_channel in input_peer_channels:
        channel = InputPeerChannel(input_peer_channel['id'], input_peer_channel['access_hash'])
        messages = await client_ms.get_messages(channel, limit=None)
        messagesClear = []
        for x in messages:
            if (x.peer_id.channel_id in consts['check_phone_id']) and x.message == None:
                messagesClear.append(x)

        await client_ms.delete_messages(channel, messagesClear)


def add_member(input_config, output_config):
    with open(folder_configs + input_config, 'r', encoding='utf-8') as f:
        config = json.loads(f.read())

    accounts = config['accounts']
    print("Total account: " + str(len(accounts)))
    # group target
    group_target_id = config['group_target']
    # group source
    group_source_id = config['group_source']
    # date_online_from
    from_date_active = (start_time + timedelta(days=-consts['day_active'])
                        ).strftime(consts['strftime'])
    # list client
    clients = []
    is_client_message = TelegramClient
    for account in accounts:
        api_id = account['api_id']
        api_hash = account['api_hash']
        phone = account['phone']

        if not account['ban']:
            client = TelegramClient(folder_session + phone, api_id, api_hash)
            client.connect()
            if client.is_user_authorized():
                print(phone + ' login success')
                clients.append({
                    'phone': phone,
                    'client': client
                })

                if not check_phone(phone):
                    is_client_message = client

            else:
                print(phone + ' login fail')

    filter_clients = []
    log_clients = ""
    for my_client in clients:
        phone = my_client['phone']
        if check_phone(phone):
            path_group = root_path + '/data/group/' + \
                phone + consts['type_file'][2]
            if os.path.isfile(path_group):

                with open(path_group, 'r', encoding='utf-8') as f:
                    groups = json.loads(f.read())

                current_target_group = get_group_by_id(groups, group_target_id)

                if current_target_group:
                    group_access_hash = int(
                        current_target_group['access_hash'])
                    target_group_entity = InputPeerChannel(
                        group_target_id, group_access_hash)

                    path_group_user = root_path + '/data/user/' + \
                        phone + "_" + str(group_source_id) + \
                        consts['type_file'][2]
                    if os.path.isfile(path_group_user):
                        # add target_group_entity key value
                        my_client['target_group_entity'] = target_group_entity
                        with open(path_group_user, encoding='utf-8') as f:
                            my_client['users'] = json.loads(f.read())

                        filter_clients.append(my_client)
                    else:
                        print('This account with phone ' +
                              str(phone) + ' is not in source group')
                else:
                    print('This account with phone ' +
                          str(phone) + ' is not in target group')
            else:
                print(
                    'This account with phone do not have data. Please run get_data or init_session')

    # run
    previous_count = 0
    count_add = 0

    try:
        with open(root_path + folder_log + output_config + consts['type_file'][1]) as f:
            previous_count = int(f.read())
    except Exception as e:
        pass

    print('From index: ' + str(previous_count))
    total_client = len(filter_clients)

    total_user = filter_clients[0]['users'].__len__()

    i = 0
    while i < total_user:

        # previous run
        if i < previous_count:
            i += 1
            continue

        # count_add if added 35 user
        if count_add % (consts['count_add_sleep'] * total_client) == (consts['count_add_sleep'] * total_client - 1):
            print('sleep 15 minute')
            time.sleep(15 * 60)

        total_client = filter_clients.__len__()
        print("remain client: " + str(total_client))
        if total_client == 0:
            with open(root_path + folder_log + output_config + consts['type_file'][1], 'w') as g:
                g.write(str(i))
                g.close()

            print('END: accounts is empty')
            break

        if count_add > consts['count_add_max']:
            with open(root_path + folder_log + output_config + consts['type_file'][1], 'w') as g:
                g.write(str(i))
                g.close()

            print('END: add max ' +
                  str(consts['count_add_max']) + ' member in dayli')
            break

        current_index = count_add % total_client
        print("current_index: " + str(current_index))
        current_client = filter_clients[current_index]
        client = current_client['client']
        user = current_client['users'][i]
        # disconnect_remove_client if added 20 user
        if count_add % (consts['disconnect_remove_client'] * total_client) == (consts['disconnect_remove_client'] * total_client - 1):
            print('END: Done add ' +
                  str(consts['disconnect_remove_client']) + ' member!')
            disconnect_remove_client(client, current_client, filter_clients)
            break

        if user['date_online'] != 'online' and user['date_online'] < from_date_active:
            i += 1
            print('User ' + user['user_id'] + ' has time active: ' +
                  user['date_online'] + ' is overdue')
            continue

        target_group_entity = current_client['target_group_entity']

        try:
            print('add member: ' + user['user_id'])
            user_to_add = InputPeerUser(
                int(user['user_id']), int(user['access_hash']))
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print('Add member ' + user['user_id'] + ' success')
            count_add += 1
            print('sleep: ' + str(120 / total_client))
            time.sleep(120 / total_client)

            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(client_message(is_client_message, consts['input_peer_channel']))
            # print('delete message Add member' + user['user_id'] + ' success')

        except PeerFloodError as e:
            print("Error Fooling cmnr")
            traceback.print_exc()
            disconnect_remove_client(client, current_client, filter_clients)
            # not increate i
            continue
        except UserPrivacyRestrictedError:
            print("Error Privacy")
        except Exception as e:
            if str(e) in consts['error_continue']:
                i += 1
                continue
            log_clients += str(e) + "\nError other " + \
                current_client['phone'] + "\n"
            print("Error other: ")
            traceback.print_exc()
            disconnect_remove_client(client, current_client, filter_clients)
            continue
            # break

        i += 1

    with open(root_path + folder_log + output_config + consts['type_file'][0], 'w') as l:
        l.write(log_clients)
        l.close()

    with open(root_path + folder_log + output_config + consts['type_file'][1], 'w') as g:
        g.write(str(i))
        g.close()
    print("disconnect")
    for cli in clients:
        cli['client'].disconnect()
    end_time = datetime.datetime.now()
    print("total: " + str(count_add))
    print("total time: " + str(end_time - start_time))


index_group = 0
dem = 0
for default_config in consts['default_config']:
    if start_time.strftime(consts['strftime']) == default_config['expire_time'] and default_config['index_group'] == index_group:
        els = [x for x in consts['default_config'] if x['index_group'] == index_group]
        default_config['expire_time'] = (start_time + timedelta(days=+int(len(els) / 2))).strftime(consts['strftime'])
        dem = dem + 1
        if dem == len([x for x in consts['default_config'] if x['index_group'] == index_group and datetime.datetime.now().strftime(consts['strftime']) == x['expire_time']]):
            index_group = index_group + 1
        print(default_config['expire_time'])
        add_member(default_config['input'] + consts['type_file'][2], default_config['output'])
        exec(open("clear_message.py").read())
# Ghi lại file const sau khi chạy xong
with open('const.json', 'w', encoding='utf-8') as f:
    json.dump(consts, f, indent=4, ensure_ascii=False)

# # 15 acc
# add_member('config_en_1.json', 'current_count_en_1')
# # 10 acc
# add_member('config_vn.json', 'current_count_vn')
