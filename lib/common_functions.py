import math
from pyjarowinkler import distance
from api_wrapper.api_data import get_mojang_data, get_skyblock_data, get_hypixel_data, get_bazaar_data, get_leaderboard_data
from api_wrapper.skyblock_player import SkyblockPlayer
from constants.skyblock import *

from base64 import b64decode as one
from gzip import decompress as two
from io import BytesIO as three
from struct import unpack


async def get_skyblock_player(mc_name=None, uuid=None, profile_name=None, call_skyblock_data=False, call_hypixel_data=False, call_bazaar_data=False, call_leaderboard_data=False, leaderboard_id=None, page=1, leaderboard_player_name=None):
    """
    Calls all APIs asynchronously

    :param mc_name: Player UUID
    :param uuid: Player UUID
    :param profile_name: Skyblock profile name
    :param call_skyblock_data: Call Skyblock API (True / False)
    :param call_hypixel_data: Call Hypixel API (True / False)
    :param call_bazaar_data: Call Bazaar API (True / False)
    :param call_leaderboard_data: Call Leaderboard API (True / False)
    :param leaderboard_id: Leaderboard ID
    :param page: For leaderboard pagination
    :param leaderboard_player_name: Leaderboard Player Name
    :returns: tuple(player_obj, leaderboard_data)
    :rtype: tuple[obj, dict]
    """
    skyblock_data = None
    hypixel_data = None
    bazaar_data = None
    leaderboard_data = None

    if mc_name or uuid is not None:
        uuid, mc_name = await get_mojang_data(mc_name, uuid)

    if call_skyblock_data:
        skyblock_data = await get_skyblock_data(uuid)

    if call_hypixel_data:
        hypixel_data = await get_hypixel_data(uuid)

    if call_bazaar_data:
        bazaar_data = await get_bazaar_data()

    if call_leaderboard_data:
        leaderboard_data = await get_leaderboard_data(leaderboard_id, page, leaderboard_player_name)

    player = SkyblockPlayer(mc_name=mc_name, uuid=uuid, profile_name=profile_name, skyblock_api=skyblock_data, hypixel_api=hypixel_data, bazaar_api=bazaar_data)

    return player, leaderboard_data


async def get_suffix(num, precise=False):
    value = 0
    if 0 <= num <= 999 and precise is False:
        value = num
    elif 0 <= num <= 999 and precise is True:
        value = str(round(num, 1))
    elif 1000 <= num <= 999999:
        num /= 1000
        value = str(round(num, 1)) + 'K'
    elif 1000000 <= num <= 999999999:
        num /= 1000000
        value = str(round(num, 1)) + 'M'
    elif 1000000000 <= num <= 999999999999:
        num /= 1000000000
        value = str(round(num, 1)) + 'B'
    elif 1000000000000 <= num <= 999999999999999:
        num /= 1000000000000
        value = str(round(num, 1)) + 'T'
    return value


def decode_inventory_data_json(raw, *, backpack=False, index_empty=False):
    """
    Takes a raw string representing inventory data.
    Returns a json object with the inventory's contents.
    """
    if backpack:
        raw = three(two(raw))
    else:
        raw = three(two(one(raw)))  # Unzip raw string from the api

    def read(type, length):
        if type in 'chil':
            return int.from_bytes(raw.read(length), byteorder='big')
        if type == 's':
            return raw.read(length).decode('utf-8')
        return unpack(f'>{type}', raw.read(length))[0]

    def parse_list():
        subtype = read('c', 1)
        payload = []
        for _ in range(read('i', 4)):
            parse_next_tag(payload, subtype)
        return payload

    def parse_compound():
        payload = {}
        while parse_next_tag(payload) != 0:  # Parse tags until we find an endcap (type == 0)
            pass  # Nothing needs to happen here
        return payload

    payloads = {
        1: lambda: read('c', 1),  # Byte
        2: lambda: read('h', 2),  # Short
        3: lambda: read('i', 4),  # Int
        4: lambda: read('l', 8),  # Long
        5: lambda: read('f', 4),  # Float
        6: lambda: read('d', 8),  # Double
        7: lambda: raw.read(read('i', 4)),  # Byte Array
        8: lambda: read('s', read('h', 2)),  # String
        9: parse_list,  # List
        10: parse_compound,  # Compound
        11: lambda: [read('i', 4) for _ in range(read('i', 4))],  # Int Array
        12: lambda: [read('l', 8) for _ in range(read('i', 4))]  # Long Array
    }

    def parse_next_tag(dictionary, tag_id=None):
        name = None
        if tag_id is None:  # Are we inside a list?
            tag_id = read('c', 1)
            if tag_id == 0:  # Is this the end of a compound?
                return 0
            name = read('s', read('h', 2))

        payload = payloads[tag_id]()
        if isinstance(dictionary, dict):
            dictionary[name] = payload
        else:
            dictionary.append(payload)

    raw.read(3)  # Remove file header (we ignore footer)
    root = {}
    parse_next_tag(root)

    items = []
    for i, x in enumerate(root['i']):
        if x and 'tag' in x and 'ExtraAttributes' in x['tag']:
            items.append(x)
        elif index_empty:
            items.append(None)

    return items


# String Matching Algorithm
async def get_matches(query, products, single=True):
    closeness = {}
    query_list = query.split(' ')
    if query_list[0].lower() in ['e', 'enc', 'ench']:
        query_list[0] = 'enchanted'
    print(query_list)

    for item in products:
        item_list = item.lower().split(' ')
        temp_closeness = 0
        temp_list = []
        temp_min = 0

        # Word Matching
        for query_item in query_list:
            for product_item in item_list:
                if query_item.lower() == product_item.lower() and query_item.lower() not in temp_list:
                    temp_closeness += 5
                    temp_list.append(query_item.lower())
                elif query_item.lower() in product_item.lower():
                    temp_min -= 0.25
                    temp_closeness += (2 * len(query_item))
                elif product_item.lower() in query_item.lower():
                    temp_min -= 0.25
                    if len(product_item) > 3:
                        temp_closeness += (2 * len(query_item))
                else:
                    temp_min -= 0.5
                    temp_closeness += distance.get_jaro_distance(query_item, product_item, winkler=True, scaling=0.1)

        # Matching Prefix
        loop_amount = min(len(query_list), len(item_list))
        for i in range(loop_amount):
            if query_list[i][0].lower() == item_list[i][0].lower():
                temp_closeness += 5

        # Length Matching
        min_value = min(len(query_list), len(item_list))
        max_value = max(len(query_list), len(item_list))
        temp_closeness += (-0.5 * (max_value - min_value))

        temp_closeness += temp_min
        closeness[item] = temp_closeness

    sorted_list = sorted(closeness, key=closeness.get, reverse=True)
    if single is True:
        return sorted_list[0]
    else:
        return sorted_list


async def get_skill_level(skill_xp, runecrafting=False):
    if runecrafting is True:
        skill_level = [key for key, value in RUNECRAFTING_XP_TABLE.items() if skill_xp >= value][-1]
    else:
        skill_level = [key for key, value in SKILL_XP_TABLE.items() if skill_xp >= value][-1]
    return skill_level


async def get_class_level(class_xp):
    class_level = [key for key, value in DUNGEON_XP_TABLE.items() if class_xp >= value][-1]
    return class_level


async def get_progress(class_level, class_xp):
    progress = (class_xp - DUNGEON_XP_TABLE[class_level]) / DUNGEON_XP_TABLE[class_level + 1]
    return progress


async def dungeon_time(time: int):
    if time == 0:
        return 'None'
    seconds = math.floor((time / 1000) % 60)
    minutes = math.floor((time / (1000 * 60)) % 60)
    hours = math.floor((time / (1000 * 60 * 60)) % 24)
    days = math.floor((time / (1000 * 60 * 60 * 24)) % 7)
    time_taken = f"{seconds} seconds"
    if minutes >= 1:
        time_taken = f"{minutes}m {seconds}s"
    if hours >= 1:
        time_taken = f"{hours}h {minutes}m"
    if days >= 1:
        time_taken = f"{days}d {hours}h"
    return time_taken


async def shorten_num(num):
    if 1000000 <= num <= 999999999:
        num /= 1000000
        value = str(round(num, 2)) + 'M'
    elif 1000000000 <= num <= 999999999999:
        num /= 1000000000
        value = str(round(num, 2)) + 'B'
    elif 1000000000000 <= num <= 999999999999999:
        num /= 1000000000000
        value = str(round(num, 2)) + 'T'
    else:
        value = f"{round(num):,}"
    return value


async def get_skill_weight(skills_info):
    skill_weight = {}
    for key, value in skills_info.items():
        if key not in BLACKLISTED_SKILLS:
            skill_level = min(await get_skill_level(value['xp']), SKILLS_TEMPLATE[key]['max_level'])
            if skill_level < SKILLS_TEMPLATE[key]['max_level']:
                skill_level = skill_level + (value['xp'] - SKILL_XP_TABLE[skill_level]) / (SKILL_INDIVIDUAL_XP_TABLE[skill_level + 1])

            base = math.pow(skill_level * 10, 0.5 + SKILL_WEIGHT_VALUES[key]['exponent'] + skill_level / 100) / 1250

            if value['xp'] <= SKILL_XP_TABLE[SKILLS_TEMPLATE[key]['max_level']]:
                skill_weight[value['name']] = {'weight': round(base), 'overflow': 0}
            else:
                overflow = math.pow((value['xp'] - SKILL_XP_TABLE[SKILLS_TEMPLATE[key]['max_level']]) / SKILL_WEIGHT_VALUES[key]['divider'], 0.968)
                skill_weight[value['name']] = {'weight': round(base), 'overflow': round(overflow)}
    return skill_weight


async def get_slayer_weight(slayer_info):
    slayer_weight = {}
    for key, value in slayer_info.items():
        divider = SLAYER_WEIGHT_VALUES[key]['divider']
        modifier = SLAYER_WEIGHT_VALUES[key]['modifier']

        if value['xp'] <= 1000000:
            slayer_weight[value['name']] = {'weight': (round(value['xp'] / divider) if value['xp'] > 0 else 0), 'overflow': 0}

        if value['xp'] > 1000000:
            base = 1000000 / divider
            remaining = value['xp'] - 1000000

            overflow = 0
            while remaining > 0:
                left = min(remaining, 1000000)
                overflow += math.pow(left / (divider * (1.5 + modifier)), 0.942)
                remaining -= left
                modifier += modifier

            slayer_weight[value['name']] = {'weight': round(base), 'overflow': round(overflow)}
    return slayer_weight


async def get_dungeon_weight(cata_xp, cata_level, class_xp):
    dungeon_weight = {}
    if cata_level != 50:
        cata_level = cata_level + ((cata_xp - DUNGEON_XP_TABLE[cata_level]) / DUNGEON_INDIVIDUAL_XP_TABLE[cata_level + 1])

    base = math.pow(cata_level, 4.5) * DUNGEON_WEIGHT_VALUES['catacomb']
    if cata_xp <= DUNGEON_XP_TABLE[50]:
        dungeon_weight['catacomb'] = {'weight': round(base), 'overflow': 0}
    else:
        dungeon_weight['catacomb'] = {'weight': round(base), 'overflow': round(math.pow((cata_xp - DUNGEON_XP_TABLE[50]) / ((4 * DUNGEON_XP_TABLE[50]) / base), 0.968))}

    for key, value in class_xp.items():
        class_level = await get_class_level(value)
        if class_level != 50:
            class_level += await get_progress(await get_class_level(value), value)
        base = math.pow(class_level, 4.5) * DUNGEON_WEIGHT_VALUES[key]
        if value <= DUNGEON_XP_TABLE[50]:
            dungeon_weight[key] = {'weight': round(base), 'overflow': 0}
        else:
            dungeon_weight[key] = {'weight': round(base), 'overflow': round(
                math.pow((value - DUNGEON_XP_TABLE[50]) / (4 * DUNGEON_XP_TABLE[50] / base), 0.968))}
    return dungeon_weight
