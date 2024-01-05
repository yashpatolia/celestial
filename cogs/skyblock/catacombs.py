import discord
import logging
import asyncio
from discord.ext import commands
from datetime import datetime
from lib.common_functions import get_skyblock_player
from lib import common_functions
from constants.skyblock import DUNGEON_XP_TABLE, DUNGEON_INDIVIDUAL_XP_TABLE
from constants.emojis import PROFILE_EMOJIS, CATACOMBS_EMOJIS, CLASS_EMOJIS


class Dungeon(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['dungeons', 'cata', 'catacombs', 'catacomb'])
    @commands.guild_only()
    async def dungeon(self, ctx, mc_name=None, profile=None):
        player, leaderboard_data = await get_skyblock_player(mc_name=mc_name, profile_name=profile, call_skyblock_data=True, call_hypixel_data=True)
        logging.info(f'COMMAND Catacombs\n'
                     f'GUILD ({ctx.guild.name}, {ctx.guild.id})\n'
                     f'DISCORD ({ctx.author}, {ctx.author.id})\n'
                     f'MINECRAFT ({player.mc_name}, {player.uuid})')

        catacombs_choices = [f"{CLASS_EMOJIS['tank']}", f"{CATACOMBS_EMOJIS['Floor 1']}", f"{CATACOMBS_EMOJIS['Master 1']}"]

        if player.cata_level != 50:
            catacombs_level_text = f'Cata Level: **{player.cata_level}** (**{round(player.cata_xp - DUNGEON_XP_TABLE[player.cata_level]):,}** / {DUNGEON_INDIVIDUAL_XP_TABLE[player.cata_level + 1]:,}) **{round(((player.cata_xp - DUNGEON_XP_TABLE[player.cata_level]) / DUNGEON_INDIVIDUAL_XP_TABLE[player.cata_level + 1]) * 100, 2)}**%'
        else:
            catacombs_level_text = f'Cata Level: **{player.cata_level}**'

        class_levels_text = ''
        for key, value in player.class_xp.items():
            class_level = await common_functions.get_class_level(value)
            if class_level != 50:
                class_progress = await common_functions.get_progress(class_level, value)
                class_levels_text += f"{CLASS_EMOJIS[key]} {key.capitalize()}: **{round(class_level + class_progress, 2)}**\n"
            else:
                class_levels_text += f"{CLASS_EMOJIS[key]} {key.capitalize()}: **{class_level}**\n"

        # Class Info
        class_embed = discord.Embed(description=f'Secrets: **{player.secrets:,}**\n'
                                                f'Class: {CLASS_EMOJIS[player.dungeon_class.lower()]} **{player.dungeon_class}**\n'
                                                f"{catacombs_level_text}",
                                                color=discord.Colour.gold(), timestamp=datetime.utcnow())
        class_embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        class_embed.set_footer(text='sb!cata <name> [profile]')

        for key, value in player.class_xp.items():
            class_level = await common_functions.get_class_level(value)
            class_level_with_progress = 50
            if class_level != 50:
                progress_start = value - DUNGEON_XP_TABLE[class_level]
                progress_end = DUNGEON_INDIVIDUAL_XP_TABLE[class_level + 1]
                class_level_with_progress = class_level + (progress_start / progress_end)

                class_levels_text = f"Total XP: **{await common_functions.shorten_num(value)}**\n" \
                                    f"XP: (**{await common_functions.shorten_num(progress_start)}** / {await common_functions.shorten_num(progress_end)})\n" \
                                    f"Progress: **{((value - DUNGEON_XP_TABLE[class_level]) / DUNGEON_INDIVIDUAL_XP_TABLE[class_level + 1]) * 100:.2f}**%"
            else:
                class_levels_text = f"Total XP: **{await common_functions.shorten_num(value)}**\n" \
                                    f"XP: **MAXED**"
            class_embed.add_field(name=f'{CLASS_EMOJIS[key]} {key.capitalize()} {class_level_with_progress:.2f}', value=f"{class_levels_text}")
        class_embed.add_field(name='\u200b', value='\u200b')

        # Normal Catacombs
        normal_embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.utcnow())
        normal_embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        normal_embed.set_footer(text='sb!cata <name> [profile]')

        for _, dungeon_floor_value in player.dungeon_floor_info.items():
            normal_embed.add_field(name=f"{CATACOMBS_EMOJIS[dungeon_floor_value['name']]} {dungeon_floor_value['name']}", value=f"Completions: **{int(dungeon_floor_value['completions'])}**\n"
                                        f"Fastest S: **{await common_functions.dungeon_time(dungeon_floor_value['fastest_time_s'])}**\n"
                                        f"Fastest S+: **{await common_functions.dungeon_time(dungeon_floor_value['fastest_time_s_plus'])}**\n")
        normal_embed.add_field(name='\u200b', value='\u200b')

        # Master Catacombs
        master_embed = discord.Embed(color=discord.Colour.gold(), timestamp=datetime.utcnow())
        master_embed.set_author(name=f'{player.mc_name} [{PROFILE_EMOJIS[player.profile_name.lower()]}{player.profile_name}]')
        master_embed.set_footer(text='sb!cata <name> [profile]')

        for _, dungeon_floor_value in player.dungeon_master_floor_info.items():
            master_embed.add_field(name=f"{CATACOMBS_EMOJIS[dungeon_floor_value['name']]} {dungeon_floor_value['name']}", value=f"Completions: **{int(dungeon_floor_value['completions'])}**\n"
                                        f"Fastest S: **{await common_functions.dungeon_time(dungeon_floor_value['fastest_time_s'])}**\n"
                                        f"Fastest S+: **{await common_functions.dungeon_time(dungeon_floor_value['fastest_time_s_plus'])}**\n")

        catacombs_output = await ctx.send(embed=class_embed)

        for reaction in catacombs_choices:
            await catacombs_output.add_reaction(reaction)

        run = True
        while run:
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in catacombs_choices and reaction.message.id == catacombs_output.id

            try:
                reaction = await self.client.wait_for('reaction_add', timeout=120, check=check)
            except asyncio.TimeoutError:
                for reaction in catacombs_choices:
                    await catacombs_output.clear_reaction(reaction)
                run = False
            else:
                if str(reaction[0]) == f"{catacombs_choices[0]}":
                    await catacombs_output.remove_reaction(str(reaction[0]), ctx.author)
                    await catacombs_output.edit(embed=class_embed)
                elif str(reaction[0]) == f"{catacombs_choices[1]}":
                    await catacombs_output.remove_reaction(str(reaction[0]), ctx.author)
                    await catacombs_output.edit(embed=normal_embed)
                elif str(reaction[0]) == f"{catacombs_choices[2]}":
                    await catacombs_output.remove_reaction(str(reaction[0]), ctx.author)
                    await catacombs_output.edit(embed=master_embed)


def setup(client):
    client.add_cog(Dungeon(client))
