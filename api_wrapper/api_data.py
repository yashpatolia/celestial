import logging
from constants.bot_config import API_KEY
from api_wrapper.utils.errors import InvalidIGN, SkyblockAPIError, HypixelAPIError, BazaarAPIError, AuctionHouseAPIError
from api_wrapper.utils.helpers import get_json

logger = logging.getLogger('api')


# Mojang Data
async def get_mojang_data(name: str = None, uuid: str = None):
    """
    Gets Minecraft IGN and UUID from api.mojang.com

    :param name: Player name (IGN)
    :param uuid: Player UUID
    :returns: tuple(str, str) (UUID, IGN)
    :rtype: tuple[str, str]
    """
    try:
        if name is not None:
            logger.info(f'GET https://api.mojang.com/users/profiles/minecraft/{name}')
            mojang_data = await get_json(f'https://api.mojang.com/users/profiles/minecraft/{name}')
            return mojang_data['id'], mojang_data['name']
        if uuid is not None:
            logger.info(f'GET https://api.mojang.com/user/profiles/{uuid}/names')
            mojang_data = await get_json(f'https://api.mojang.com/user/profiles/{uuid}/names')
            return uuid, mojang_data[-1]['name']
    except Exception as e:
        raise InvalidIGN(e)


# Skyblock Data
async def get_skyblock_data(uuid: str):
    """
    Gets Hypixel skyblock data from api.hypixel.net

    :param uuid: Player UUID
    :returns: Skyblock Data
    :rtype: dict
    """
    try:
        logger.info(f'GET https://api.hypixel.net/skyblock/profiles?key=API_KEY&uuid={uuid}')
        skyblock_data = await get_json(f'https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}')
        return skyblock_data
    except Exception as e:
        raise SkyblockAPIError(e)


# Hypixel Data
async def get_hypixel_data(uuid: str):
    """
    Gets Hypixel data from api.hypixel.net

    :param uuid: Player UUID
    :returns: Hypixel Data, Linked Discord
    :rtype: tuple[str, str]
    """
    try:
        logger.info(f'GET https://api.hypixel.net/player?key=API_KEY&uuid={uuid}')
        hypixel_data = await get_json(f'https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}')
        return hypixel_data
    except Exception as e:
        raise HypixelAPIError(e)


# Bazaar Data
async def get_bazaar_data():
    """
    Gets bazaar data from sky.lea.moe

    :returns: Bazaar Data
    :rtype: dict
    """
    try:
        logger.info('GET https://sky.lea.moe/api/bazaar')
        bazaar_data = await get_json('https://sky.lea.moe/api/bazaar')
        return bazaar_data
    except Exception as e:
        raise BazaarAPIError(e)


# Auction House Data
async def get_auction_house_data(page=1):
    """
    Gets auction house data from api.hypixel.net

    :returns: Auction House Data
    :rtype: dict
    """
    try:
        logger.info(f'GET https://api.hypixel.net/skyblock/auctions?page={page}')
        auction_house_data = await get_json(f'https://api.hypixel.net/skyblock/auctions?page={page}')
        return auction_house_data
    except Exception as e:
        raise AuctionHouseAPIError(e)


# Leaderboard Data
async def get_leaderboard_data(leaderboard_id, page=1, name=None):
    """
    Gets leaderboard data from sky.lea.moe

    :param leaderboard_id: Leaderboard ID
    :param page: Page number for pagination
    :param name: Find a player
    :return: Leaderboard data
    :rtype: dict
    """
    if name is None:
        logger.info(f'GET https://sky.lea.moe/api/v2/leaderboard/{leaderboard_id}?page={page}')
        leaderboard_data = await get_json(f'https://sky.lea.moe/api/v2/leaderboard/{leaderboard_id}?page={page}')
    else:
        logger.info(f'GET https://sky.lea.moe/api/v2/leaderboard/{leaderboard_id}?find={name}')
        try:
            leaderboard_data = await get_json(f'https://sky.lea.moe/api/v2/leaderboard/{leaderboard_id}?find={name}')
        except Exception as e:
            raise InvalidIGN(e)
    return leaderboard_data


# Leaderboards
async def get_leaderboards():
    """
    Gets all skyblock leaderboards from sky.lea.moe

    :return: Leaderboards
    :rtype: dict
    """
    logger.info(f'GET https://sky.lea.moe/api/v2/leaderboards')
    data = await get_json('https://sky.lea.moe/api/v2/leaderboards')
    skyblock_leaderboards = {}
    for item in data:
        skyblock_leaderboards[item['name']] = item['key']
    return skyblock_leaderboards
