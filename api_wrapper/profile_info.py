from api_wrapper.utils.errors import NoProfilesFound


def get_profiles(skyblock_data):
    """
    Get all skyblock profile names

    :param skyblock_data: Skyblock Data
    :return: List of profile names
    """
    if skyblock_data['profiles'] is not None:
        profile_names = [profile['cute_name'] for profile in skyblock_data['profiles']]
    else:
        raise NoProfilesFound
    return profile_names


def get_latest_profile(skyblock_data, uuid):
    """
    Get latest profile name and index number

    :param skyblock_data: Skyblock Data
    :param uuid: Player UUID
    :return: (str, int)
    :rtype: tuple[str, int]
    """
    timestamps = {x: skyblock_data['profiles'][x]['members'][uuid]['last_save'] for x in
                  range(len(skyblock_data['profiles'])) if "last_save" in skyblock_data['profiles'][x]['members'][uuid]}
    if timestamps:
        latest_profile_index = max(timestamps, key=timestamps.get)
        latest_profile_name = skyblock_data['profiles'][latest_profile_index]['cute_name']
        return latest_profile_name, latest_profile_index
    else:
        raise NoProfilesFound


def get_profile_info(skyblock_data, profile_name, profiles, latest_profile_name, latest_profile_index):
    """
    Gets profile name and index

    :param skyblock_data: Skyblock data
    :param profile_name: Skyblock profile name
    :param profiles: Player profiles
    :param latest_profile_name: Latest profile name
    :param latest_profile_index: Latest profile index
    """
    if profile_name is not None and profile_name.capitalize() in profiles:
        profile_index = None
        for x in range(len(skyblock_data['profiles'])):
            if skyblock_data['profiles'][x]['cute_name'] == profile_name.capitalize():
                profile_index = x
                break
        return profile_name.capitalize(), profile_index
    else:
        return latest_profile_name, latest_profile_index
