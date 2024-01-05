import discord
import logging
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from lib import common_functions
from constants.emojis import SKILL_EMOJIS, CATACOMBS_EMOJIS, SLAYER_EMOJIS, PROFILE_EMOJIS, CLASS_EMOJIS


class Weight(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['we'])
    @commands.guild_only()
    async def weight(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True)
        logging.info(f'COMMAND Weight\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')

        skill_weight = await common_functions.get_skill_weight(player.skills_info)
        dungeon_weight = await common_functions.get_dungeon_weight(player.cata_xp, player.cata_level, player.class_xp)
        slayer_weight = await common_functions.get_slayer_weight(player.slayer_info)

        total_weight = {'total': 0, 'overflow': 0, 'skill': 0, 'skill_overflow': 0, 'dungeon': 0, 'dungeon_overflow': 0, 'slayer': 0, 'slayer_overflow': 0}
        for key, value in skill_weight.items():
            total_weight['total'] += value['weight']
            total_weight['overflow'] += value['overflow']
            total_weight['skill'] += value['weight']
            total_weight['skill_overflow'] += value['overflow']

        for key, value in slayer_weight.items():
            total_weight['total'] += value['weight']
            total_weight['overflow'] += value['overflow']
            total_weight['slayer'] += value['weight']
            total_weight['slayer_overflow'] += value['overflow']

        for key, value in dungeon_weight.items():
            total_weight['total'] += value['weight']
            total_weight['overflow'] += value['overflow']
            total_weight['dungeon'] += value['weight']
            total_weight['dungeon_overflow'] += value['overflow']

        skill_weight_text = f"{SKILL_EMOJIS['experience_skill_combat']} Combat: **{skill_weight['Combat']['weight']}** {'+ **' + str(skill_weight['Combat']['overflow']) + '**' if skill_weight['Combat']['overflow'] != 0 else ''}\n" \
                            f"{SKILL_EMOJIS['experience_skill_mining']} Mining: **{skill_weight['Mining']['weight']}** {'+ **' + str(skill_weight['Mining']['overflow']) + '**' if skill_weight['Mining']['overflow'] != 0 else ''}\n" \
                            f"{SKILL_EMOJIS['experience_skill_foraging']} Foraging: **{skill_weight['Foraging']['weight']}** {'+ **' + str(skill_weight['Foraging']['overflow']) + '**' if skill_weight['Foraging']['overflow'] != 0 else ''}\n" \
                            f"{SKILL_EMOJIS['experience_skill_farming']} Farming: **{skill_weight['Farming']['weight']}** {'+ **' + str(skill_weight['Farming']['overflow']) + '**' if skill_weight['Farming']['overflow'] != 0 else ''}\n"
        skill_weight_text_two = f"{SKILL_EMOJIS['experience_skill_fishing']} Fishing: **{skill_weight['Fishing']['weight']}** {'+ **' + str(skill_weight['Fishing']['overflow']) + '**' if skill_weight['Fishing']['overflow'] != 0 else ''}\n" \
                                f"{SKILL_EMOJIS['experience_skill_taming']} Taming: **{skill_weight['Taming']['weight']}** {'+ **' + str(skill_weight['Taming']['overflow']) + '**' if skill_weight['Taming']['overflow'] != 0 else ''}\n" \
                                f"{SKILL_EMOJIS['experience_skill_alchemy']} Alchemy: **{skill_weight['Alchemy']['weight']}** {'+ **' + str(skill_weight['Alchemy']['overflow']) + '**' if skill_weight['Alchemy']['overflow'] != 0 else ''}\n" \
                                f"{SKILL_EMOJIS['experience_skill_enchanting']} Enchanting: **{skill_weight['Enchanting']['weight']}** {'+ **' + str(skill_weight['Enchanting']['overflow']) + '**' if skill_weight['Enchanting']['overflow'] != 0 else ''}\n"

        dungeon_weight_text = f"{CATACOMBS_EMOJIS['Floor 1']} Catacombs: **{dungeon_weight['catacomb']['weight']}** {'+ **' + str(dungeon_weight['catacomb']['overflow']) + '**' if dungeon_weight['catacomb']['overflow'] != 0 else ''}\n" \
                              f"{CLASS_EMOJIS['mage']} Mage: **{dungeon_weight['mage']['weight']}** {'+ **' + str(dungeon_weight['mage']['overflow']) + '**' if dungeon_weight['mage']['overflow'] != 0 else ''}\n" \
                              f"{CLASS_EMOJIS['berserk']} Berserk: **{dungeon_weight['berserk']['weight']}** {'+ **' + str(dungeon_weight['berserk']['overflow']) + '**' if dungeon_weight['berserk']['overflow'] != 0 else ''}\n" \
                              f"{CLASS_EMOJIS['archer']} Archer: **{dungeon_weight['archer']['weight']}** {'+ **' + str(dungeon_weight['archer']['overflow']) + '**' if dungeon_weight['archer']['overflow'] != 0 else ''}\n" \
                              f"{CLASS_EMOJIS['tank']} Tank: **{dungeon_weight['tank']['weight']}** {'+ **' + str(dungeon_weight['tank']['overflow']) + '**' if dungeon_weight['tank']['overflow'] != 0 else ''}\n" \
                              f"{CLASS_EMOJIS['healer']} Healer: **{dungeon_weight['healer']['weight']}** {'+ **' + str(dungeon_weight['healer']['overflow']) + '**' if dungeon_weight['healer']['overflow'] != 0 else ''}\n"

        slayer_weight_text = f"{SLAYER_EMOJIS['zombie']} Revenant: **{slayer_weight['Revenant']['weight']}** {'+ **' + str(slayer_weight['Revenant']['overflow']) + '**' if slayer_weight['Revenant']['overflow'] != 0 else ''}\n" \
                             f"{SLAYER_EMOJIS['spider']} Tarantula: **{slayer_weight['Tarantula']['weight']}** {'+ **' + str(slayer_weight['Tarantula']['overflow']) + '**' if slayer_weight['Tarantula']['overflow'] != 0 else ''}\n" \
                             f"{SLAYER_EMOJIS['wolf']} Sven: **{slayer_weight['Sven']['weight']}** {'+ **' + str(slayer_weight['Sven']['overflow']) + '**' if slayer_weight['Sven']['overflow'] != 0 else ''}\n" \
                             f"{SLAYER_EMOJIS['enderman']} Voidgloom: **{slayer_weight['Voidgloom']['weight']}** {'+ **' + str(slayer_weight['Voidgloom']['overflow']) + '**' if slayer_weight['Voidgloom']['overflow'] != 0 else ''}"

        embed = discord.Embed(description=f"Total Weight: **{total_weight['total'] + total_weight['overflow']}** with **{total_weight['overflow']}** being overflow!",
                              color=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        embed.set_footer(text='sb!weight <name> [profile]')
        embed.add_field(name=f"Skills: {total_weight['skill'] + total_weight['skill_overflow']}", value=f"{skill_weight_text}")
        embed.add_field(name='\u200b', value=f'\u200b')
        embed.add_field(name='\u200b', value=f'{skill_weight_text_two}')
        embed.add_field(name=f"Dungeons: {total_weight['dungeon'] + total_weight['dungeon_overflow']}", value=f'{dungeon_weight_text}')
        embed.add_field(name='\u200b', value=f'\u200b')
        embed.add_field(name=f"Slayers: {total_weight['slayer'] + total_weight['slayer_overflow']}", value=f'{slayer_weight_text}')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Weight(client))
