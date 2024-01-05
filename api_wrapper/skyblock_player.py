from api_wrapper import profile_info, skyblock_data


class SkyblockPlayer:
    def __init__(self, mc_name=None, uuid=None, profile_name=None, skyblock_api=None, hypixel_api=None, bazaar_api=None):
        """
        Represents a Skyblock Player

        :param mc_name: The player's in game name
        :param uuid: The player's UUID
        :param profile_name: The player's skyblock profile name
        :param skyblock_api: Skyblock data
        :param hypixel_api: Hypixel data
        :param bazaar_api: Bazaar data
        """

        # Data / Info
        self.uuid, self.mc_name = uuid, mc_name
        self.skyblock_data = skyblock_api
        self.hypixel_data = hypixel_api
        self.bazaar_data = bazaar_api

        # Skyblock
        if self.skyblock_data is not None:
            self.profiles = profile_info.get_profiles(self.skyblock_data)
            self.latest_profile_name, self.latest_profile_index = profile_info.get_latest_profile(self.skyblock_data, self.uuid)
            self.profile_name, self.profile_index = profile_info.get_profile_info(self.skyblock_data, profile_name, self.profiles, self.latest_profile_name, self.latest_profile_index)

            self.purse, self.bank = skyblock_data.get_money(self.skyblock_data, self.profile_index, self.uuid)
            self.slayer_info, self.total_slayer_xp = skyblock_data.get_slayer_data(self.skyblock_data, self.profile_index, self.uuid)
            self.rock_milestone, self.dolphin_milestone, self.next_rock_milestone, self.next_dolphin_milestone, self.rock_rarity, self.dolphin_rarity = skyblock_data.get_pet_milestones(self.skyblock_data, self.profile_index, self.uuid)
            self.currently_upgrading, self.coop_upgrades = skyblock_data.get_community_upgrades(self.skyblock_data, self.profile_index)
            self.skills_info, self.total_xp = skyblock_data.get_skills_data(self.skyblock_data, self.profile_index, self.uuid)
            self.jacob_medals, self.jacob_upgrades, self.jacob_info = skyblock_data.get_jacob_data(self.skyblock_data, self.profile_index, self.uuid)

        if self.skyblock_data:
            self.secrets, self.dungeon_class, self.cata_xp, self.cata_level, self.class_xp, self.dungeon_floor_info, self.dungeon_master_floor_info = skyblock_data.get_dungeons_data(self.skyblock_data, self.hypixel_data, self.profile_index, self.uuid)

        # Hypixel
        if self.hypixel_data is not None:
            self.linked_discord = skyblock_data.get_linked_discord(self.hypixel_data)

        # Bazaar
        if self.bazaar_data is not None:
            self.bazaar_info = skyblock_data.get_bazaar_info(self.bazaar_data)
